#!/usr/bin/env python3
"""Batch-publish ClawHub skills and plugins with dual-token scheduling."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ACCOUNTS_FILE = REPO_ROOT / "example" / "accounts"
DEFAULT_STATE_FILE = REPO_ROOT / "targets" / "clawhub-publish-state.json"
DEFAULT_SKILL_ROOT = REPO_ROOT / "clawhub-release"
DEFAULT_PLUGIN_ROOT = REPO_ROOT / "clawhub-plugin-release" / "plugins"
DEFAULT_CONFIG_ROOT = REPO_ROOT / ".tmp-clawhub-auth"

RATE_LIMIT_PATTERNS = (
    re.compile(r"\b429\b"),
    re.compile(r"rate\s*limit", re.IGNORECASE),
    re.compile(r"too\s+many\s+requests", re.IGNORECASE),
    re.compile(r"quota", re.IGNORECASE),
)
NOT_FOUND_PATTERNS = (
    re.compile(r"not\s+found", re.IGNORECASE),
    re.compile(r"\b404\b"),
)
TRANSIENT_PROBE_PATTERNS = (
    re.compile(r"timed?\s*out", re.IGNORECASE),
    re.compile(r"fetch\s+failed", re.IGNORECASE),
    re.compile(r"temporary", re.IGNORECASE),
    re.compile(r"network", re.IGNORECASE),
)
TOKEN_KEYS = ("clawhub_ApI_token", "clawhub_ApI_token2")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def normalize_key(raw: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", raw.lower())


def titleize_slug(slug: str) -> str:
    words = slug.replace("_", "-").split("-")
    titled: list[str] = []
    for word in words:
        lower = word.lower()
        if not lower:
            continue
        if lower == "aisa":
            titled.append("AIsa")
        elif lower in {"llm", "api"}:
            titled.append(lower.upper())
        elif lower == "x":
            titled.append("X")
        else:
            titled.append(word.capitalize())
    return " ".join(titled) if titled else slug


def load_frontmatter(skill_path: Path) -> dict[str, Any]:
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    _, raw_yaml, _body = parts
    data = yaml.safe_load(raw_yaml) or {}
    return data if isinstance(data, dict) else {}


def run_command(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    cwd: Path = REPO_ROOT,
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        args,
        cwd=str(cwd),
        env=merged_env,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def parse_accounts_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        separator = "=" if "=" in line else ":" if ":" in line else None
        if not separator:
            continue
        key, value = line.split(separator, 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            continue
        values[normalize_key(key)] = value
    return values


def resolve_tokens(args: argparse.Namespace) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()

    def add(token: str | None) -> None:
        if not token or token in seen:
            return
        seen.add(token)
        tokens.append(token)

    for token in args.token or []:
        add(token.strip())

    for env_name in ("CLAWHUB_TOKEN", "CLAWHUB_TOKEN_1", "CLAWHUB_TOKEN_2"):
        add(os.environ.get(env_name, "").strip())

    if args.accounts_file:
        account_values = parse_accounts_file(Path(args.accounts_file))
        for key in TOKEN_KEYS:
            add(account_values.get(normalize_key(key)))

    return tokens[:2]


def detect_git_source(repo_root: Path) -> dict[str, str]:
    remote = run_command(["git", "remote", "get-url", "origin"], cwd=repo_root)
    if remote.returncode != 0:
        raise RuntimeError("Could not resolve git remote origin for plugin source attribution.")
    repo_url = remote.stdout.strip()
    commit = run_command(["git", "rev-parse", "HEAD"], cwd=repo_root)
    if commit.returncode != 0:
        raise RuntimeError("Could not resolve git commit for plugin source attribution.")
    ref = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root)
    if ref.returncode != 0:
        raise RuntimeError("Could not resolve git branch for plugin source attribution.")

    dirty = run_command(["git", "status", "--short"], cwd=repo_root)
    repo = (
        repo_url.replace("git@github-work:", "")
        .replace("git@github.com:", "")
        .replace("https://github.com/", "")
        .replace(".git", "")
        .strip()
    )
    return {
        "repo": repo,
        "commit": commit.stdout.strip(),
        "ref": ref.stdout.strip(),
        "dirty": "true" if bool(dirty.stdout.strip()) else "false",
    }


@dataclass
class Artifact:
    key: str
    kind: str
    name: str
    version: str
    path: str
    display_name: str
    source_path: str | None = None


@dataclass
class ArtifactState:
    key: str
    kind: str
    name: str
    version: str
    path: str
    status: str = "pending"
    attempts: int = 0
    published_at: str | None = None
    last_checked_at: str | None = None
    last_attempt_at: str | None = None
    last_error: str | None = None
    token_slot: str | None = None
    release_ref: str | None = None


class StateStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.Lock()
        self.data = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"generated_at": None, "artifacts": {}}
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                payload.setdefault("artifacts", {})
                return payload
        except json.JSONDecodeError:
            pass
        return {"generated_at": None, "artifacts": {}}

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(".tmp")
        temp_path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        temp_path.replace(self.path)

    def upsert_artifact(self, artifact: Artifact) -> None:
        with self.lock:
            artifacts = self.data.setdefault("artifacts", {})
            current = artifacts.get(artifact.key, {})
            current.update(
                {
                    "key": artifact.key,
                    "kind": artifact.kind,
                    "name": artifact.name,
                    "version": artifact.version,
                    "path": artifact.path,
                }
            )
            artifacts[artifact.key] = current
            self.data["generated_at"] = iso_now()
            self.save()

    def mark(self, artifact: Artifact, **updates: Any) -> None:
        with self.lock:
            artifacts = self.data.setdefault("artifacts", {})
            current = artifacts.setdefault(
                artifact.key,
                {
                    "key": artifact.key,
                    "kind": artifact.kind,
                    "name": artifact.name,
                    "version": artifact.version,
                    "path": artifact.path,
                },
            )
            current.update(updates)
            current["version"] = artifact.version
            current["path"] = artifact.path
            self.data["generated_at"] = iso_now()
            self.save()

    def get(self, artifact: Artifact) -> dict[str, Any]:
        with self.lock:
            return dict(self.data.get("artifacts", {}).get(artifact.key, {}))


class SharedQueue:
    def __init__(self, artifacts: list[Artifact]) -> None:
        self._items = deque(artifacts)
        self._lock = threading.Lock()

    def pop(self) -> Artifact | None:
        with self._lock:
            return self._items.popleft() if self._items else None

    def push_front(self, artifact: Artifact) -> None:
        with self._lock:
            self._items.appendleft(artifact)

    def remaining(self) -> int:
        with self._lock:
            return len(self._items)


@dataclass
class WorkerResult:
    slot: str
    published: int = 0
    skipped: int = 0
    failed: int = 0
    rate_limited: bool = False
    notes: list[str] = field(default_factory=list)


class Worker(threading.Thread):
    def __init__(
        self,
        *,
        slot: str,
        token: str,
        args: argparse.Namespace,
        queue: SharedQueue,
        state: StateStore,
        source_info: dict[str, str],
    ) -> None:
        super().__init__(daemon=True)
        self.slot = slot
        self.token = token
        self.args = args
        self.queue = queue
        self.state = state
        self.source_info = source_info
        self.result = WorkerResult(slot=slot)
        self.config_path = Path(args.config_root) / f"{slot}.json"
        self.publish_times: deque[float] = deque()

    def log(self, message: str) -> None:
        print(f"[{self.slot}] {message}", flush=True)

    def clawhub(self, command: list[str], timeout: int = 900) -> subprocess.CompletedProcess[str]:
        return run_command(
            ["clawhub", *command],
            env={"CLAWHUB_CONFIG_PATH": str(self.config_path)},
            timeout=timeout,
        )

    def login(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        result = self.clawhub(["login", "--token", self.token, "--no-browser"], timeout=120)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "ClawHub login failed.")
        whoami = self.clawhub(["whoami"], timeout=120)
        if whoami.returncode == 0:
            self.log(f"authenticated as {whoami.stdout.strip()}")
        else:
            self.log("authenticated")

    def run(self) -> None:
        try:
            self.login()
        except Exception as exc:  # noqa: BLE001
            self.result.failed += 1
            self.result.notes.append(str(exc))
            self.log(f"login failed: {exc}")
            return

        while True:
            artifact = self.queue.pop()
            if artifact is None:
                return

            if self.is_quota_exhausted():
                self.queue.push_front(artifact)
                self.result.rate_limited = True
                self.result.notes.append(
                    f"quota reached after {self.result.published} publish(es); rerun after the hourly window resets"
                )
                self.log("hourly quota reached; stopping this worker")
                return

            try:
                if self.check_remote_exists(artifact):
                    self.state.mark(
                        artifact,
                        status="published",
                        published_at=iso_now(),
                        last_checked_at=iso_now(),
                        last_error=None,
                        token_slot=self.slot,
                    )
                    self.result.skipped += 1
                    self.log(f"skip remote-existing {artifact.kind}:{artifact.name}@{artifact.version}")
                    continue

                if self.args.dry_run:
                    self.state.mark(
                        artifact,
                        status="planned",
                        last_checked_at=iso_now(),
                        token_slot=self.slot,
                    )
                    self.result.skipped += 1
                    self.log(f"dry-run {artifact.kind}:{artifact.name}@{artifact.version}")
                    continue

                publish_result = self.publish_artifact(artifact)
                output = "\n".join(
                    part for part in (publish_result.stdout.strip(), publish_result.stderr.strip()) if part
                )
                release_ref = extract_release_ref(output)
                self.publish_times.append(time.time())
                self.state.mark(
                    artifact,
                    status="published",
                    attempts=self.state.get(artifact).get("attempts", 0) + 1,
                    published_at=iso_now(),
                    last_attempt_at=iso_now(),
                    last_checked_at=iso_now(),
                    last_error=None,
                    token_slot=self.slot,
                    release_ref=release_ref,
                )
                self.result.published += 1
                self.log(f"published {artifact.kind}:{artifact.name}@{artifact.version}")
            except PublishError as exc:
                attempts = self.state.get(artifact).get("attempts", 0) + 1
                status = "rate_limited" if exc.rate_limited else "failed"
                self.state.mark(
                    artifact,
                    status=status,
                    attempts=attempts,
                    last_attempt_at=iso_now(),
                    last_checked_at=iso_now(),
                    last_error=exc.message,
                    token_slot=self.slot,
                )
                if exc.rate_limited:
                    self.result.rate_limited = True
                    self.result.notes.append(exc.message)
                    self.queue.push_front(artifact)
                    self.log(f"rate-limited while publishing {artifact.name}; stopping this worker")
                    return
                self.result.failed += 1
                self.log(f"failed {artifact.kind}:{artifact.name}@{artifact.version}: {exc.message}")

    def is_quota_exhausted(self) -> bool:
        now = time.time()
        while self.publish_times and now - self.publish_times[0] >= 3600:
            self.publish_times.popleft()
        return len(self.publish_times) >= self.args.per_token_per_hour

    def check_remote_exists(self, artifact: Artifact) -> bool:
        for attempt in range(1, self.args.probe_retries + 1):
            if artifact.kind == "skill":
                result = self.clawhub(["inspect", artifact.name, "--json"], timeout=120)
            else:
                result = self.clawhub(["package", "inspect", artifact.name, "--json"], timeout=120)
            if result.returncode == 0:
                return True
            text = f"{result.stdout}\n{result.stderr}"
            if any(pattern.search(text) for pattern in NOT_FOUND_PATTERNS):
                return False
            if is_transient_probe_error(text) and attempt < self.args.probe_retries:
                self.log(
                    f"probe retry {attempt}/{self.args.probe_retries - 1} for {artifact.name}: {clean_error(text)}"
                )
                time.sleep(self.args.probe_retry_delay)
                continue
            raise PublishError(f"remote probe failed for {artifact.name}: {clean_error(text)}")
        return False

    def publish_artifact(self, artifact: Artifact) -> subprocess.CompletedProcess[str]:
        if artifact.kind == "skill":
            command = [
                "publish",
                artifact.path,
                "--slug",
                artifact.name,
                "--name",
                artifact.display_name,
                "--version",
                artifact.version,
                "--tags",
                self.args.tags,
            ]
        else:
            if not artifact.source_path:
                raise PublishError("Missing source_path for plugin publish.")
            command = [
                "package",
                "publish",
                artifact.path,
                "--family",
                "code-plugin",
                "--name",
                artifact.name,
                "--display-name",
                artifact.display_name,
                "--version",
                artifact.version,
                "--tags",
                self.args.tags,
                "--source-repo",
                self.source_info["repo"],
                "--source-commit",
                self.source_info["commit"],
                "--source-ref",
                self.source_info["ref"],
                "--source-path",
                artifact.source_path,
            ]
        result = self.clawhub(command, timeout=self.args.publish_timeout)
        if result.returncode == 0:
            return result
        error_text = clean_error(f"{result.stdout}\n{result.stderr}")
        raise PublishError(error_text, rate_limited=is_rate_limited(error_text))


class PublishError(RuntimeError):
    def __init__(self, message: str, *, rate_limited: bool = False) -> None:
        super().__init__(message)
        self.message = message
        self.rate_limited = rate_limited


def is_rate_limited(text: str) -> bool:
    return any(pattern.search(text) for pattern in RATE_LIMIT_PATTERNS)


def is_transient_probe_error(text: str) -> bool:
    return any(pattern.search(text) for pattern in TRANSIENT_PROBE_PATTERNS)


def clean_error(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " | ".join(lines[-8:]) if lines else "unknown error"


def extract_release_ref(text: str) -> str | None:
    match = re.search(r"\(([^()]+)\)\s*$", text.strip())
    return match.group(1) if match else None


def discover_skill_artifacts(root: Path) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for skill_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        frontmatter = load_frontmatter(skill_file)
        version = str(frontmatter.get("version") or "1.0.0")
        display_name = titleize_slug(str(frontmatter.get("name") or skill_dir.name))
        artifacts.append(
            Artifact(
                key=f"skill:{skill_dir.name}",
                kind="skill",
                name=skill_dir.name,
                version=version,
                path=str(skill_dir.relative_to(REPO_ROOT)),
                display_name=display_name,
            )
        )
    return artifacts


def discover_plugin_artifacts(root: Path, source_repo_root: Path) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for plugin_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        package_json_path = plugin_dir / "package.json"
        manifest_path = plugin_dir / "openclaw.plugin.json"
        if not package_json_path.exists() or not manifest_path.exists():
            continue
        package_json = json.loads(package_json_path.read_text(encoding="utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        source_path = plugin_dir.relative_to(source_repo_root).as_posix()
        artifacts.append(
            Artifact(
                key=f"plugin:{package_json['name']}",
                kind="plugin",
                name=str(package_json["name"]),
                version=str(package_json.get("version") or "1.0.0"),
                path=str(plugin_dir.relative_to(REPO_ROOT)),
                display_name=str(manifest.get("name") or titleize_slug(plugin_dir.name)),
                source_path=source_path,
            )
        )
    return artifacts


def maybe_build(args: argparse.Namespace) -> None:
    if args.skip_build:
        return

    steps = [
        ["python3", "scripts/normalize_target_skills.py"],
        ["python3", "scripts/build_clawhub_release.py"],
    ]
    if args.targets in {"plugin", "both"}:
        steps.append(["python3", "scripts/build_clawhub_plugin_release.py"])

    for command in steps:
        result = run_command(command, timeout=1800)
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        if result.returncode != 0:
            raise RuntimeError(f"Build step failed: {' '.join(command)}")


def filter_pending(artifacts: list[Artifact], state: StateStore, force: bool) -> list[Artifact]:
    pending: list[Artifact] = []
    for artifact in artifacts:
        state.upsert_artifact(artifact)
        if force:
            pending.append(artifact)
            continue
        current = state.get(artifact)
        if current.get("status") == "published" and current.get("version") == artifact.version:
            continue
        pending.append(artifact)
    return pending


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publish unpublished ClawHub skills/plugins with dual-token scheduling.",
    )
    parser.add_argument(
        "--targets",
        choices=("skill", "plugin", "both"),
        default="both",
        help="Which release layers to publish.",
    )
    parser.add_argument(
        "--accounts-file",
        default=str(DEFAULT_ACCOUNTS_FILE),
        help="Optional credentials file containing clawhub_ApI_token entries.",
    )
    parser.add_argument(
        "--token",
        action="append",
        help="ClawHub API token. Repeat for a second token.",
    )
    parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="Persisted publish state JSON.",
    )
    parser.add_argument(
        "--config-root",
        default=str(DEFAULT_CONFIG_ROOT),
        help="Directory for per-token ClawHub CLI config files.",
    )
    parser.add_argument(
        "--skill-root",
        default=str(DEFAULT_SKILL_ROOT),
        help="Root directory for ClawHub skill publishes.",
    )
    parser.add_argument(
        "--plugin-root",
        default=str(DEFAULT_PLUGIN_ROOT),
        help="Root directory for ClawHub plugin publishes.",
    )
    parser.add_argument(
        "--source-repo-root",
        default=str(REPO_ROOT),
        help="Git repo root used for plugin source attribution.",
    )
    parser.add_argument(
        "--per-token-per-hour",
        type=int,
        default=4,
        help="Conservative hourly publish cap for each token.",
    )
    parser.add_argument(
        "--tags",
        default="latest",
        help="Comma-separated tags passed to publish commands.",
    )
    parser.add_argument(
        "--publish-timeout",
        type=int,
        default=1800,
        help="Timeout in seconds for each publish command.",
    )
    parser.add_argument(
        "--probe-retries",
        type=int,
        default=3,
        help="Retry count for transient remote probe failures before marking an artifact failed.",
    )
    parser.add_argument(
        "--probe-retry-delay",
        type=float,
        default=2.0,
        help="Seconds to wait between transient remote probe retries.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip rebuilding the ClawHub release layers first.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore local publish state and probe/publish every artifact again.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve state and remote existence without publishing.",
    )
    return parser


def print_summary(results: list[WorkerResult], pending_after: int) -> None:
    published = sum(item.published for item in results)
    skipped = sum(item.skipped for item in results)
    failed = sum(item.failed for item in results)
    print("", flush=True)
    print("ClawHub batch summary", flush=True)
    print(f"  published: {published}", flush=True)
    print(f"  skipped:   {skipped}", flush=True)
    print(f"  failed:    {failed}", flush=True)
    print(f"  pending:   {pending_after}", flush=True)
    for item in results:
        note = f" ({'; '.join(item.notes)})" if item.notes else ""
        print(
            f"  {item.slot}: published={item.published}, skipped={item.skipped}, failed={item.failed}, rate_limited={item.rate_limited}{note}",
            flush=True,
        )


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    tokens = resolve_tokens(args)
    if not tokens:
        parser.error("No ClawHub tokens found. Provide --token or use example/accounts.")
    if len(tokens) < 2:
        print("Only one ClawHub token resolved; continuing with a single worker.", flush=True)

    maybe_build(args)

    state = StateStore(Path(args.state_file))
    source_repo_root = Path(args.source_repo_root).resolve()
    source_info = detect_git_source(source_repo_root)
    if source_info["dirty"] == "true":
        print(
            "Warning: source repo has uncommitted changes. Plugin source attribution will point at the current HEAD commit.",
            flush=True,
        )

    artifacts: list[Artifact] = []
    if args.targets in {"skill", "both"}:
        artifacts.extend(discover_skill_artifacts(Path(args.skill_root)))
    if args.targets in {"plugin", "both"}:
        artifacts.extend(discover_plugin_artifacts(Path(args.plugin_root), source_repo_root))

    if not artifacts:
        print("No publishable artifacts found.", flush=True)
        return 0

    pending = filter_pending(artifacts, state, force=args.force)
    if not pending:
        print("Everything in local state is already marked published at the current version.", flush=True)
        return 0

    print(f"Resolved {len(pending)} pending artifact(s).", flush=True)
    queue = SharedQueue(pending)
    workers = [
        Worker(
            slot=f"token-{index}",
            token=token,
            args=args,
            queue=queue,
            state=state,
            source_info=source_info,
        )
        for index, token in enumerate(tokens, start=1)
    ]

    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

    results = [worker.result for worker in workers]
    print_summary(results, queue.remaining())
    return 0 if not any(item.failed for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
