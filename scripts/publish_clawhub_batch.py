#!/usr/bin/env python3
"""Batch-publish ClawHub skills and plugins with multi-token scheduling."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from clawhub_live_status import ArtifactRef, scan_artifact_status, scan_needs_retry, scan_result_to_state


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
ALREADY_EXISTS_PATTERNS = (
    re.compile(r"already\s+exists", re.IGNORECASE),
    re.compile(r"already\s+published", re.IGNORECASE),
    re.compile(r"\b409\b"),
    re.compile(r"\bconflict\b", re.IGNORECASE),
    re.compile(r"\bduplicate\b", re.IGNORECASE),
)
SLUG_TAKEN_PATTERNS = (
    re.compile(r"slug\s+is\s+already\s+taken", re.IGNORECASE),
    re.compile(r"choose\s+a\s+different\s+slug", re.IGNORECASE),
)
TOKEN_KEY_PATTERN = re.compile(r"^clawhubapitoken(?P<index>\d*)$")
OWNER_SLOT_HINTS = {
    "baofeng-tech": "token-1",
    "bibaofeng": "token-2",
    "aisadocs": "token-3",
}
SLOT_OWNER_HINTS = {slot: owner for owner, slot in OWNER_SLOT_HINTS.items()}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def normalize_key(raw: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", raw.lower())


def infer_preferred_slot(meta: dict[str, Any]) -> str | None:
    if not isinstance(meta, dict):
        return None
    live_scan = meta.get("live_scan") if isinstance(meta.get("live_scan"), dict) else {}
    owner_handle = str(live_scan.get("publisher_handle") or meta.get("owner_handle") or "").strip().lstrip("@")
    if owner_handle:
        mapped = OWNER_SLOT_HINTS.get(owner_handle.lower())
        if mapped:
            return mapped
    detail_url = str(live_scan.get("detail_url") or "").strip()
    match = re.search(r"https?://[^/]+/([^/]+)/([^/]+)", detail_url)
    if match and match.group(1).lower() != "plugins":
        mapped = OWNER_SLOT_HINTS.get(match.group(1).strip().lstrip("@").lower())
        if mapped:
            return mapped
    slot = str(meta.get("token_slot") or "").strip()
    return slot or None


def owner_hint_for_slot(slot: str | None) -> str | None:
    if not slot:
        return None
    return SLOT_OWNER_HINTS.get(slot)


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


def suffix_publish_name(name: str, suffix: str) -> str:
    cleaned_suffix = re.sub(r"[^a-z0-9-]+", "-", suffix.lower()).strip("-")
    if not cleaned_suffix:
        return name
    if name.endswith("-plugin"):
        return f"{name[: -len('-plugin')]}-{cleaned_suffix}-plugin"
    return f"{name}-{cleaned_suffix}"


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
    if args and args[0] == "clawhub":
        clawhub_bin = (
            os.environ.get("CLAWHUB_BIN", "").strip()
            or shutil.which("clawhub")
            or shutil.which("clawhub.cmd")
            or shutil.which("clawhub.exe")
        )
        if clawhub_bin:
            if os.name == "nt" and clawhub_bin.lower().endswith((".cmd", ".bat")):
                args = ["cmd.exe", "/c", clawhub_bin, *args[1:]]
            else:
                args = [clawhub_bin, *args[1:]]
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        args,
        cwd=str(cwd),
        env=merged_env,
        text=True,
        encoding="utf-8",
        errors="replace",
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


def token_sort_key(key: str) -> tuple[int, str]:
    match = TOKEN_KEY_PATTERN.match(key)
    if not match:
        return (sys.maxsize, key)
    raw_index = match.group("index")
    index = int(raw_index) if raw_index else 1
    return (index, key)


def extract_account_tokens(account_values: dict[str, str]) -> list[str]:
    return [
        account_values[key]
        for key in sorted(account_values, key=token_sort_key)
        if TOKEN_KEY_PATTERN.match(key)
    ]


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

    env_tokens: list[tuple[int, str]] = []
    for env_name, value in os.environ.items():
        if not value:
            continue
        if env_name == "CLAWHUB_TOKEN":
            env_tokens.append((1, value))
            continue
        match = re.fullmatch(r"CLAWHUB_TOKEN_(\d+)", env_name)
        if match:
            env_tokens.append((int(match.group(1)), value))
    for _index, value in sorted(env_tokens, key=lambda item: item[0]):
        add(value.strip())

    if args.accounts_file:
        account_values = parse_accounts_file(Path(args.accounts_file))
        for value in extract_account_tokens(account_values):
            add(value)

    return tokens


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

    dirty_value = "unknown"
    try:
        dirty = run_command(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=repo_root,
            timeout=20,
        )
        if dirty.returncode == 0:
            dirty_value = "true" if bool(dirty.stdout.strip()) else "false"
    except subprocess.TimeoutExpired:
        dirty_value = "unknown"
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
        "dirty": dirty_value,
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
            next_version = artifact.version
            current_status = str(current.get("status") or "")
            current_version = current.get("version")
            if current_status == "published" and current_version:
                next_version = str(current_version)
            elif should_preserve_state_version(current_version, artifact.version):
                next_version = str(current_version)
            current.update(
                {
                    "key": artifact.key,
                    "kind": artifact.kind,
                    "name": artifact.name,
                    "version": next_version,
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
            if should_preserve_state_version(current.get("version"), artifact.version):
                current["version"] = current.get("version")
            else:
                current["version"] = artifact.version
            current["path"] = artifact.path
            self.data["generated_at"] = iso_now()
            self.save()

    def get(self, artifact: Artifact) -> dict[str, Any]:
        with self.lock:
            return dict(self.data.get("artifacts", {}).get(artifact.key, {}))

    def get_by_key(self, key: str) -> dict[str, Any]:
        with self.lock:
            return dict(self.data.get("artifacts", {}).get(key, {}))

    def recent_publish_times(self, slot: str, *, window_seconds: int = 3600) -> list[float]:
        cutoff = utc_now().timestamp() - window_seconds
        timestamps: list[float] = []
        with self.lock:
            for meta in self.data.get("artifacts", {}).values():
                if not isinstance(meta, dict):
                    continue
                if meta.get("status") != "published" or meta.get("token_slot") != slot:
                    continue
                publish_mode = meta.get("publish_mode")
                if publish_mode not in (None, "published"):
                    continue
                if publish_mode is None and int(meta.get("attempts") or 0) <= 0:
                    continue
                published_at = parse_iso_datetime(meta.get("published_at"))
                if published_at is None:
                    continue
                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=timezone.utc)
                timestamp = published_at.timestamp()
                if timestamp >= cutoff:
                    timestamps.append(timestamp)
        return sorted(timestamps)


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

    def push_back(self, artifact: Artifact) -> None:
        with self._lock:
            self._items.append(artifact)

    def remaining(self) -> int:
        with self._lock:
            return len(self._items)


@dataclass
class WorkerResult:
    slot: str
    published: int = 0
    skipped: int = 0
    failed: int = 0
    suspicious: int = 0
    rate_limited: bool = False
    notes: list[str] = field(default_factory=list)


class Worker(threading.Thread):
    def __init__(
        self,
        *,
        slot: str,
        slot_index: int,
        token: str,
        args: argparse.Namespace,
        queue: SharedQueue,
        state: StateStore,
        source_info: dict[str, str],
    ) -> None:
        super().__init__(daemon=True)
        self.slot = slot
        self.slot_index = slot_index
        self.token = token
        self.args = args
        self.queue = queue
        self.state = state
        self.source_info = source_info
        self.result = WorkerResult(slot=slot)
        self.config_path = Path(args.config_root) / f"{slot}.json"
        self.publish_times: deque[float] = deque(self.state.recent_publish_times(slot))

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
        carried = len(self.publish_times)
        if carried:
            self.log(f"carrying forward {carried} real publish(es) from the past hour")

    def inspect_payload(self, artifact: Artifact) -> Any | None:
        remote_name = self.current_publish_name(artifact)
        try:
            if artifact.kind == "skill":
                result = self.clawhub(["inspect", remote_name, "--json"], timeout=self.args.scan_inspect_timeout)
            else:
                result = self.clawhub(
                    ["package", "inspect", remote_name, "--json"],
                    timeout=self.args.scan_inspect_timeout,
                )
        except subprocess.TimeoutExpired:
            return None
        if result.returncode != 0:
            return None
        return try_parse_json(result.stdout)

    def current_publish_name(self, artifact: Artifact) -> str:
        current_state = self.state.get(artifact)
        return str(current_state.get("published_name") or artifact.name)

    def conflict_publish_name(self, artifact: Artifact) -> str:
        current_state = self.state.get(artifact)
        existing = str(current_state.get("published_name") or "").strip()
        if existing and existing != artifact.name:
            return existing
        if artifact.kind == "plugin" and artifact.name.endswith("-plugin"):
            sibling_key = f"skill:{artifact.name[: -len('-plugin')]}"
            sibling_state = self.state.get_by_key(sibling_key)
            sibling_name = str(sibling_state.get("name") or "").strip()
            sibling_published_name = str(sibling_state.get("published_name") or "").strip()
            if sibling_published_name and sibling_published_name != sibling_name:
                return f"{sibling_published_name}-plugin"
        return suffix_publish_name(artifact.name, f"slot{self.slot_index}")

    def post_publish_scan(self, artifact: Artifact) -> None:
        if not self.args.post_publish_scan:
            return

        current_state = self.state.get(artifact)
        cached_scan = current_state.get("live_scan") if isinstance(current_state.get("live_scan"), dict) else {}
        remote_name = self.current_publish_name(artifact)
        artifact_ref = ArtifactRef(
            key=artifact.key,
            kind=artifact.kind,
            name=remote_name,
            version=artifact.version,
            path=artifact.path,
            release_ref=str(current_state.get("release_ref") or "") or None,
            detail_url=str(cached_scan.get("detail_url") or "") or None,
        )

        for attempt in range(1, self.args.scan_retries + 1):
            result = scan_artifact_status(
                artifact_ref,
                inspect_payload_getter=lambda _artifact_ref: self.inspect_payload(artifact),
                skill_owner_candidates=self.args.scan_skill_owner,
                render_mode=self.args.scan_render_mode,
                request_timeout=self.args.scan_request_timeout,
                render_timeout_ms=self.args.scan_render_timeout_ms,
                render_wait_ms=self.args.scan_render_wait_ms,
            )
            self.state.mark(artifact, live_scan=scan_result_to_state(result))
            if result.suspicious:
                self.result.suspicious += 1
                self.log(
                    f"live scan flagged suspicious {artifact.kind}:{remote_name} "
                    f"(vt={result.virus_total or '-'}, clawscan={result.clawscan_verdict or result.openclaw_verdict or '-'}, "
                    f"static={result.static_analysis_status or '-'})"
                )
                if result.suspicious_reason:
                    self.log(f"live scan reason: {result.suspicious_reason}")
                return
            if not scan_needs_retry(result) or attempt >= self.args.scan_retries:
                status_label = "pending" if result.pending else "ok"
                self.log(
                    f"live scan {status_label} {artifact.kind}:{remote_name} "
                    f"(vt={result.virus_total or '-'}, clawscan={result.clawscan_verdict or result.openclaw_verdict or '-'}, "
                    f"static={result.static_analysis_status or '-'})"
                )
                return
            self.log(
                f"live scan pending for {artifact.kind}:{remote_name}; "
                f"retrying in {self.args.scan_retry_delay:.1f}s"
            )
            time.sleep(self.args.scan_retry_delay)

    def remote_version_exists(self, artifact: Artifact) -> bool | None:
        remote_name = self.current_publish_name(artifact)
        try:
            if artifact.kind == "skill":
                result = self.clawhub(["inspect", remote_name, "--json"], timeout=120)
            else:
                result = self.clawhub(["package", "inspect", remote_name, "--json"], timeout=120)
        except subprocess.TimeoutExpired:
            return None
        if result.returncode == 0:
            return parse_remote_probe(result.stdout, artifact.version).version_exists
        text = f"{result.stdout}\n{result.stderr}"
        if any(pattern.search(text) for pattern in NOT_FOUND_PATTERNS):
            return False
        return None

    def publish_with_fallback(self, artifact: Artifact, *, attempts: int, reason: str) -> bool:
        fallback_name = self.conflict_publish_name(artifact)
        if fallback_name == self.current_publish_name(artifact):
            return False

        self.log(f"{reason}; retrying with fallback slug {fallback_name}")
        publish_result, published_name = self.publish_artifact(
            artifact,
            publish_name=fallback_name,
        )
        output = "\n".join(
            part for part in (publish_result.stdout.strip(), publish_result.stderr.strip()) if part
        )
        release_ref = extract_release_ref(output)
        self.publish_times.append(time.time())
        self.state.mark(
            artifact,
            status="published",
            attempts=attempts,
            published_at=iso_now(),
            last_attempt_at=iso_now(),
            last_checked_at=iso_now(),
            last_error=None,
            token_slot=self.slot,
            owner_handle=owner_hint_for_slot(self.slot),
            published_name=published_name,
            release_ref=release_ref,
            publish_mode="published-fallback",
        )
        self.result.published += 1
        self.log(
            f"published fallback {artifact.kind}:{artifact.name}@{artifact.version} as {published_name}"
        )
        self.post_publish_scan(artifact)
        return True

    def run(self) -> None:
        try:
            self.login()
        except Exception as exc:  # noqa: BLE001
            self.result.failed += 1
            self.result.notes.append(str(exc))
            self.log(f"login failed: {exc}")
            return

        start_delay = self.args.worker_start_stagger_seconds * max(self.slot_index - 1, 0)
        if start_delay > 0:
            self.log(f"waiting {start_delay:.1f}s before starting publishes")
            time.sleep(start_delay)

        while True:
            artifact = self.queue.pop()
            if artifact is None:
                return

            preferred_slot = infer_preferred_slot(self.state.get(artifact))
            if preferred_slot and preferred_slot != self.slot:
                self.queue.push_back(artifact)
                time.sleep(1.0)
                continue

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
                        published_name=self.current_publish_name(artifact),
                        publish_mode="remote-existing",
                    )
                    self.result.skipped += 1
                    self.log(
                        f"skip remote-existing {artifact.kind}:{self.current_publish_name(artifact)}@{artifact.version}"
                    )
                    self.post_publish_scan(artifact)
                    continue

                if self.args.dry_run:
                    current_state = self.state.get(artifact)
                    status = str(current_state.get("status") or "planned")
                    if status not in {"published", "failed", "rate_limited"}:
                        status = "planned"
                    self.state.mark(
                        artifact,
                        status=status,
                        last_checked_at=iso_now(),
                        token_slot=self.slot,
                    )
                    self.result.skipped += 1
                    self.log(f"dry-run {artifact.kind}:{artifact.name}@{artifact.version}")
                    continue

                publish_result, published_name = self.publish_artifact(artifact)
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
                    owner_handle=owner_hint_for_slot(self.slot),
                    published_name=published_name,
                    release_ref=release_ref,
                    publish_mode="published",
                )
                self.result.published += 1
                self.log(f"published {artifact.kind}:{artifact.name}@{artifact.version} as {published_name}")
                self.post_publish_scan(artifact)
            except PublishError as exc:
                attempts = self.state.get(artifact).get("attempts", 0) + 1
                if exc.slug_taken and self.args.slug_conflict_strategy == "suffix-by-slot":
                    try:
                        if self.publish_with_fallback(
                            artifact,
                            attempts=attempts,
                            reason=f"slug conflict for {artifact.kind}:{artifact.name}",
                        ):
                            continue
                    except PublishError as fallback_exc:
                        exc = fallback_exc
                if exc.already_exists:
                    remote_version_exists = self.remote_version_exists(artifact)
                    if self.args.slug_conflict_strategy == "suffix-by-slot" and remote_version_exists is not True:
                        try:
                            if self.publish_with_fallback(
                                artifact,
                                attempts=attempts,
                                reason=f"owner/version conflict for {artifact.kind}:{artifact.name}",
                            ):
                                continue
                        except PublishError as fallback_exc:
                            exc = fallback_exc
                            remote_version_exists = self.remote_version_exists(artifact)
                    if remote_version_exists is True:
                        self.state.mark(
                            artifact,
                            status="published",
                            attempts=attempts,
                            published_at=iso_now(),
                            last_attempt_at=iso_now(),
                            last_checked_at=iso_now(),
                            last_error=None,
                            token_slot=self.slot,
                            published_name=self.current_publish_name(artifact),
                            publish_mode="publish-existing",
                        )
                        self.result.skipped += 1
                        self.log(
                            f"skip publish-existing {artifact.kind}:{self.current_publish_name(artifact)}@{artifact.version}: {exc.message}"
                        )
                        self.post_publish_scan(artifact)
                        continue
                    exc = PublishError(
                        (
                            f"{exc.message} | remote slug {self.current_publish_name(artifact)} "
                            f"did not confirm version {artifact.version}; use the original owner token "
                            "or keep the slot fallback strategy."
                        ),
                    )
                status = "rate_limited" if exc.rate_limited else "failed"
                current_state = self.state.get(artifact)
                preserved_slot = (
                    infer_preferred_slot(current_state)
                    if current_state.get("published_name")
                    else self.slot
                ) or self.slot
                self.state.mark(
                    artifact,
                    status=status,
                    attempts=attempts,
                    last_attempt_at=iso_now(),
                    last_checked_at=iso_now(),
                    last_error=exc.message,
                    token_slot=preserved_slot,
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
        if self.args.force:
            return False
        remote_name = self.current_publish_name(artifact)
        for attempt in range(1, self.args.probe_retries + 1):
            try:
                if artifact.kind == "skill":
                    result = self.clawhub(["inspect", remote_name, "--json"], timeout=120)
                else:
                    result = self.clawhub(["package", "inspect", remote_name, "--json"], timeout=120)
            except subprocess.TimeoutExpired:
                text = "inspect timed out"
                if attempt < self.args.probe_retries:
                    self.log(
                        f"probe retry {attempt}/{self.args.probe_retries - 1} for {remote_name}: {text}"
                    )
                    time.sleep(self.args.probe_retry_delay)
                    continue
                raise PublishError(f"remote probe failed for {remote_name}: {text}")
            if result.returncode == 0:
                probe = parse_remote_probe(result.stdout, artifact.version)
                if probe.version_exists:
                    return True
                if probe.known_versions:
                    versions = ", ".join(probe.known_versions)
                    self.log(
                        f"remote slug exists for {remote_name}, but local version {artifact.version} "
                        f"is not among remote versions [{versions}]; attempting publish"
                    )
                else:
                    self.log(
                        f"remote slug exists for {remote_name}, but inspect did not expose version details; "
                        f"attempting publish for {artifact.version}"
                    )
                return False
            text = f"{result.stdout}\n{result.stderr}"
            if any(pattern.search(text) for pattern in NOT_FOUND_PATTERNS):
                return False
            if is_transient_probe_error(text) and attempt < self.args.probe_retries:
                self.log(
                    f"probe retry {attempt}/{self.args.probe_retries - 1} for {remote_name}: {clean_error(text)}"
                )
                time.sleep(self.args.probe_retry_delay)
                continue
            raise PublishError(f"remote probe failed for {remote_name}: {clean_error(text)}")
        return False

    def publish_artifact(self, artifact: Artifact, *, publish_name: str | None = None) -> tuple[subprocess.CompletedProcess[str], str]:
        target_name = publish_name or self.current_publish_name(artifact)
        publish_path = artifact.path
        temp_plugin_dir: Path | None = None
        if artifact.kind == "skill":
            command = [
                "publish",
                publish_path,
                "--slug",
                target_name,
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
            if target_name != artifact.name:
                temp_plugin_dir = self.prepare_plugin_publish_dir(artifact, target_name)
                publish_path = str(temp_plugin_dir)
            command = [
                "package",
                "publish",
                publish_path,
                "--family",
                "code-plugin",
                "--name",
                target_name,
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
        try:
            result = self.clawhub(command, timeout=self.args.publish_timeout)
        finally:
            if temp_plugin_dir is not None:
                shutil.rmtree(temp_plugin_dir.parent, ignore_errors=True)
        if result.returncode == 0:
            return result, target_name
        error_text = clean_error(f"{result.stdout}\n{result.stderr}")
        raise PublishError(
            error_text,
            rate_limited=is_rate_limited(error_text),
            already_exists=is_already_exists(error_text),
            slug_taken=is_slug_taken(error_text),
        )

    def prepare_plugin_publish_dir(self, artifact: Artifact, publish_name: str) -> Path:
        source_dir = Path(artifact.path)
        temp_root = Path(tempfile.mkdtemp(prefix="clawhub-plugin-publish-", dir=str(REPO_ROOT / ".tmp-clawhub-auth")))
        temp_dir = temp_root / source_dir.name
        shutil.copytree(source_dir, temp_dir)

        package_json_path = temp_dir / "package.json"
        openclaw_manifest_path = temp_dir / "openclaw.plugin.json"
        claude_manifest_path = temp_dir / ".claude-plugin" / "plugin.json"

        package_json = json.loads(package_json_path.read_text(encoding="utf-8"))
        package_json["name"] = publish_name
        package_json_path.write_text(json.dumps(package_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        openclaw_manifest = json.loads(openclaw_manifest_path.read_text(encoding="utf-8"))
        openclaw_manifest["id"] = publish_name
        openclaw_manifest_path.write_text(
            json.dumps(openclaw_manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        if claude_manifest_path.exists():
            claude_manifest = json.loads(claude_manifest_path.read_text(encoding="utf-8"))
            claude_manifest["name"] = publish_name
            claude_manifest_path.write_text(
                json.dumps(claude_manifest, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        return temp_dir


class PublishError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        rate_limited: bool = False,
        already_exists: bool = False,
        slug_taken: bool = False,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.rate_limited = rate_limited
        self.already_exists = already_exists
        self.slug_taken = slug_taken


@dataclass(frozen=True)
class RemoteProbe:
    version_exists: bool
    known_versions: list[str] = field(default_factory=list)


def try_parse_json(text: str) -> Any | None:
    if not isinstance(text, str):
        return None
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def collect_version_strings(payload: Any) -> set[str]:
    versions: set[str] = set()

    def visit(value: Any, *, key_hint: str | None = None) -> None:
        if isinstance(value, dict):
            for key, inner in value.items():
                normalized = normalize_key(str(key))
                if "version" in normalized and isinstance(inner, (str, int, float)):
                    versions.add(str(inner))
                visit(inner, key_hint=normalized)
            return
        if isinstance(value, list):
            for item in value:
                visit(item, key_hint=key_hint)
            return
        if key_hint and "version" in key_hint and isinstance(value, (str, int, float)):
            versions.add(str(value))

    visit(payload)
    return versions


def parse_remote_probe(text: str, version: str) -> RemoteProbe:
    payload = try_parse_json(text)
    if payload is None:
        return RemoteProbe(version_exists=False, known_versions=[])
    known_versions = sorted(collect_version_strings(payload))
    return RemoteProbe(version_exists=version in known_versions, known_versions=known_versions)


def is_rate_limited(text: str) -> bool:
    return any(pattern.search(text) for pattern in RATE_LIMIT_PATTERNS)


def is_already_exists(text: str) -> bool:
    return any(pattern.search(text) for pattern in ALREADY_EXISTS_PATTERNS)


def is_slug_taken(text: str) -> bool:
    return any(pattern.search(text) for pattern in SLUG_TAKEN_PATTERNS)


def is_transient_probe_error(text: str) -> bool:
    return any(pattern.search(text) for pattern in TRANSIENT_PROBE_PATTERNS)


def clean_error(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " | ".join(lines[-8:]) if lines else "unknown error"


def extract_release_ref(text: str) -> str | None:
    match = re.search(r"\(([^()]+)\)\s*$", text.strip())
    return match.group(1) if match else None


def parse_version_parts(value: str | None) -> tuple[int, ...]:
    if not value:
        return ()
    parts: list[int] = []
    for raw in str(value).split("."):
        raw = raw.strip()
        if not raw:
            return ()
        if not raw.isdigit():
            return ()
        parts.append(int(raw))
    return tuple(parts)


def should_preserve_state_version(current_version: str | None, artifact_version: str) -> bool:
    current_parts = parse_version_parts(current_version)
    artifact_parts = parse_version_parts(artifact_version)
    if not current_parts or not artifact_parts:
        return False
    return current_parts > artifact_parts


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
                path=str(skill_dir.resolve()),
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
                path=str(plugin_dir.resolve()),
                display_name=str(manifest.get("name") or titleize_slug(plugin_dir.name)),
                source_path=source_path,
            )
        )
    return artifacts


def filter_requested_artifacts(artifacts: list[Artifact], requested_keys: list[str]) -> list[Artifact]:
    if not requested_keys:
        return artifacts

    available = {artifact.key: artifact for artifact in artifacts}
    filtered: list[Artifact] = []
    seen: set[str] = set()
    missing: list[str] = []

    for raw_key in requested_keys:
        key = str(raw_key).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        artifact = available.get(key)
        if artifact is None:
            missing.append(key)
            continue
        filtered.append(artifact)

    if missing:
        print(
            "Warning: requested artifacts were not found locally: " + ", ".join(missing),
            flush=True,
        )
    return filtered


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
        description="Publish unpublished ClawHub skills/plugins with multi-token scheduling.",
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
        help="Optional credentials file containing clawhub_ApI_token, clawhub_ApI_token2, clawhub_ApI_token3... entries.",
    )
    parser.add_argument(
        "--token",
        action="append",
        help="ClawHub API token. Repeat to add more workers.",
    )
    parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="Persisted publish state JSON.",
    )
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Only publish the specified artifact key(s), such as skill:search or plugin:twitter-plugin. Repeatable.",
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
        "--worker-start-stagger-seconds",
        type=float,
        default=6.0,
        help="Delay between worker start times so multiple accounts do not publish in the same instant.",
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
        "--post-publish-scan",
        action="store_true",
        help="After a publish or remote-existing skip, check the live ClawHub page for VirusTotal/ClawScan/Static analysis status.",
    )
    parser.add_argument(
        "--slug-conflict-strategy",
        choices=("fail", "suffix-by-slot"),
        default="suffix-by-slot",
        help="How to handle ClawHub ownership/slug conflicts. The default retries with a slot-specific fallback slug.",
    )
    parser.add_argument(
        "--scan-retries",
        type=int,
        default=4,
        help="Retry count for post-publish live scan checks when the page is still pending.",
    )
    parser.add_argument(
        "--scan-retry-delay",
        type=float,
        default=15.0,
        help="Seconds to wait between post-publish live scan retries.",
    )
    parser.add_argument(
        "--scan-render-mode",
        choices=("off", "auto", "always"),
        default="auto",
        help="Whether post-publish live scans should use Playwright rendering for dynamic pages.",
    )
    parser.add_argument(
        "--scan-request-timeout",
        type=int,
        default=20,
        help="HTTP timeout in seconds for post-publish live scans.",
    )
    parser.add_argument(
        "--scan-render-timeout-ms",
        type=int,
        default=20000,
        help="Navigation timeout for Playwright-based post-publish live scans.",
    )
    parser.add_argument(
        "--scan-render-wait-ms",
        type=int,
        default=5000,
        help="Extra wait window for dynamic page HTML to stabilize during post-publish live scans.",
    )
    parser.add_argument(
        "--scan-inspect-timeout",
        type=int,
        default=25,
        help="Timeout in seconds for `clawhub inspect` during post-publish skill URL resolution.",
    )
    parser.add_argument(
        "--scan-skill-owner",
        action="append",
        default=[],
        help="Optional skill owner handle(s) used to guess skill detail URLs when inspect does not resolve them.",
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
    suspicious = sum(item.suspicious for item in results)
    print("", flush=True)
    print("ClawHub batch summary", flush=True)
    print(f"  published: {published}", flush=True)
    print(f"  skipped:   {skipped}", flush=True)
    print(f"  failed:    {failed}", flush=True)
    print(f"  suspicious:{suspicious}", flush=True)
    print(f"  pending:   {pending_after}", flush=True)
    for item in results:
        note = f" ({'; '.join(item.notes)})" if item.notes else ""
        print(
            f"  {item.slot}: published={item.published}, skipped={item.skipped}, failed={item.failed}, suspicious={item.suspicious}, rate_limited={item.rate_limited}{note}",
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
    else:
        print(f"Resolved {len(tokens)} ClawHub token(s).", flush=True)

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
    artifacts = filter_requested_artifacts(artifacts, args.artifact)

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
            slot_index=index,
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
