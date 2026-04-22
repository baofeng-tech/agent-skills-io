#!/usr/bin/env python3
"""Batch-publish Hermes skills via fork -> branch -> PR.

This bypasses the unstable forking/API path inside the current Hermes CLI
release while preserving the same end result:

- create/update a branch on the user's fork
- copy one packaged skill into `skills/<skill-name>/`
- open a PR against `baofeng-tech/Aisa-One-Skills-Hermes`
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
HERMES_RELEASE = REPO_ROOT / "hermes-release"
UPSTREAM_REPO = "baofeng-tech/Aisa-One-Skills-Hermes"
PUBLISH_OWNER = "baofeng-tech"
PUBLISH_REMOTE_NAME = "publish"
PUBLISH_REMOTE_URL = f"git@github-work:{UPSTREAM_REPO}.git"
LOCAL_HERMES_REPO = Path("/mnt/d/workplace/Aisa-One-Skills-Hermes")
WORK_CLONE = Path("/mnt/d/workplace/hermes-pr-batch-clone")
WINDOWS_GIT = "/mnt/d/Program Files/Git/cmd/git.exe"
WINDOWS_CURL = "/mnt/c/Windows/System32/curl.exe"
GIT_USER_NAME = "baofeng-tech"
GIT_USER_EMAIL = "baofeng-tech@users.noreply.github.com"


@dataclass
class PublishResult:
    skill: str
    status: str
    branch: str
    pr_url: str | None = None
    note: str | None = None


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=check,
        text=True,
        capture_output=True,
    )


def get_token() -> str:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token

    accounts = REPO_ROOT / "example" / "accounts"
    for line in accounts.read_text(encoding="utf-8").splitlines():
        if line.startswith("GITHUB_TOKEN="):
            token = line.split("=", 1)[1].strip()
            if token:
                return token
    raise SystemExit("GITHUB_TOKEN not found in environment or example/accounts")


def api_request(token: str, method: str, url: str, payload: dict | None = None) -> tuple[int, object]:
    cmd = [
        WINDOWS_CURL,
        "-sS",
        "--retry",
        "4",
        "--retry-all-errors",
        "--connect-timeout",
        "20",
        "--max-time",
        "90",
        "-w",
        "\n__STATUS__:%{http_code}",
        "-X",
        method,
        "-H",
        f"Authorization: Bearer {token}",
        "-H",
        "Accept: application/vnd.github+json",
    ]
    if payload is not None:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(payload, ensure_ascii=False)])
    cmd.append(url)
    try:
        proc = run(cmd)
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or exc.stdout or "").strip()
        raise RuntimeError(f"GitHub API request failed for {method} {url}: {stderr or exc.returncode}") from exc
    raw = proc.stdout.replace("\r\n", "\n")
    marker = "\n__STATUS__:"
    if marker not in raw:
        raise RuntimeError(f"Unable to parse GitHub API response status for {url}")
    body_text, status_text = raw.rsplit(marker, 1)
    status = int(status_text.strip() or "0")
    try:
        body = json.loads(body_text) if body_text.strip() else {}
    except json.JSONDecodeError:
        body = body_text
    return status, body


def fetch_open_pr_skill_names(token: str) -> dict[str, str]:
    status, body = api_request(
        token,
        "GET",
        f"https://api.github.com/repos/{UPSTREAM_REPO}/pulls?state=open&per_page=100",
    )
    if status != 200 or not isinstance(body, list):
        raise SystemExit(f"Failed to list open PRs (HTTP {status}): {body}")

    result: dict[str, str] = {}
    for pr in body:
        title = str(pr.get("title", "")).strip()
        if title.startswith("Add skill: "):
            skill_name = title.split("Add skill: ", 1)[1].strip()
            if skill_name:
                result[skill_name] = pr["html_url"]
                continue
        number = pr["number"]
        files_status, files_body = api_request(
            token,
            "GET",
            f"https://api.github.com/repos/{UPSTREAM_REPO}/pulls/{number}/files",
        )
        if files_status != 200 or not isinstance(files_body, list):
            continue
        for changed in files_body:
            parts = changed["filename"].split("/")
            if len(parts) >= 2 and parts[0] == "skills":
                result[parts[1]] = pr["html_url"]
                break
    return result


def list_release_skills() -> dict[str, Path]:
    skills: dict[str, Path] = {}
    for skill_file in HERMES_RELEASE.glob("*/*/SKILL.md"):
        skills[skill_file.parent.name] = skill_file.parent
    return skills


def ensure_clone() -> None:
    if not WORK_CLONE.exists():
        WORK_CLONE.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", str(LOCAL_HERMES_REPO), str(WORK_CLONE)])
    run(["git", "config", "user.name", GIT_USER_NAME], cwd=WORK_CLONE)
    run(["git", "config", "user.email", GIT_USER_EMAIL], cwd=WORK_CLONE)
    remotes = run(["git", "remote"], cwd=WORK_CLONE).stdout.split()
    if PUBLISH_REMOTE_NAME not in remotes:
        run(["git", "remote", "add", PUBLISH_REMOTE_NAME, PUBLISH_REMOTE_URL], cwd=WORK_CLONE)
    else:
        run(["git", "remote", "set-url", PUBLISH_REMOTE_NAME, PUBLISH_REMOTE_URL], cwd=WORK_CLONE)
    run(["git", "checkout", "main"], cwd=WORK_CLONE)
    run(["git", "fetch", "origin", "main"], cwd=WORK_CLONE)
    run(["git", "reset", "--hard", "origin/main"], cwd=WORK_CLONE)
    run(["git", "clean", "-fd"], cwd=WORK_CLONE)


def wpath(path: Path) -> str:
    return run(["wslpath", "-w", str(path)]).stdout.strip()


def reset_branch(branch: str) -> None:
    run(["git", "checkout", "main"], cwd=WORK_CLONE)
    run(["git", "reset", "--hard", "HEAD"], cwd=WORK_CLONE)
    run(["git", "clean", "-fd"], cwd=WORK_CLONE)
    run(["git", "checkout", "-B", branch], cwd=WORK_CLONE)


def stage_skill(skill_name: str, source_dir: Path) -> None:
    target_dir = WORK_CLONE / "skills" / skill_name
    shutil.rmtree(target_dir, ignore_errors=True)
    target_dir.mkdir(parents=True, exist_ok=True)
    for item in source_dir.iterdir():
        destination = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination)


def has_changes() -> bool:
    status = run(["git", "status", "--short"], cwd=WORK_CLONE).stdout.strip()
    return bool(status)


def commit_skill(skill_name: str) -> None:
    run(["git", "add", "-A"], cwd=WORK_CLONE)
    run(["git", "commit", "-m", f"Add skill: {skill_name}"], cwd=WORK_CLONE)


def push_branch(token: str, branch: str) -> None:
    run(
        [
            WINDOWS_GIT,
            "-C",
            wpath(WORK_CLONE),
            "push",
            PUBLISH_REMOTE_NAME,
            f"HEAD:refs/heads/{branch}",
            "--force",
        ]
    )


def create_pr(token: str, skill_name: str, branch: str) -> tuple[str | None, str | None]:
    status, body = api_request(
        token,
        "POST",
        f"https://api.github.com/repos/{UPSTREAM_REPO}/pulls",
        {
            "title": f"Add skill: {skill_name}",
            "head": f"{PUBLISH_OWNER}:{branch}",
            "base": "main",
            "body": f"Automated publish for `{skill_name}` from `hermes-release`.",
        },
    )
    if status in {200, 201} and isinstance(body, dict):
        return body.get("html_url"), None
    if status == 422 and isinstance(body, dict):
        return None, body.get("message", "Validation Failed")
    return None, f"HTTP {status}: {body}"


def resolve_targets(requested: list[str], open_prs: dict[str, str]) -> list[str]:
    release_skills = list_release_skills()
    if requested:
        missing_from_release = [name for name in requested if name not in release_skills]
        if missing_from_release:
            raise SystemExit(f"Unknown skill(s): {', '.join(missing_from_release)}")
        return requested
    return sorted(name for name in release_skills if name not in open_prs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Hermes fork -> PR publishes for packaged skills.")
    parser.add_argument("skills", nargs="*", help="Specific skill names to publish. Default: all release skills without an open PR.")
    parser.add_argument("--report", default="targets/hermes-fork-pr-batch-report-2026-04-20.json", help="JSON report path")
    args = parser.parse_args()

    token = get_token()
    open_prs = fetch_open_pr_skill_names(token)
    targets = resolve_targets(args.skills, open_prs)
    release_skills = list_release_skills()
    ensure_clone()

    results: list[PublishResult] = []
    for skill_name in targets:
        branch = f"add-skill-{skill_name}"
        if skill_name in open_prs:
            results.append(PublishResult(skill=skill_name, status="already_open", branch=branch, pr_url=open_prs[skill_name]))
            continue

        try:
            reset_branch(branch)
            stage_skill(skill_name, release_skills[skill_name])
            if not has_changes():
                results.append(PublishResult(skill=skill_name, status="no_changes", branch=branch))
                continue
            commit_skill(skill_name)
            push_branch(token, branch)
            pr_url, note = create_pr(token, skill_name, branch)
            if pr_url:
                results.append(PublishResult(skill=skill_name, status="pr_created", branch=branch, pr_url=pr_url))
            else:
                results.append(PublishResult(skill=skill_name, status="push_only", branch=branch, note=note))
        except subprocess.CalledProcessError as exc:
            note = (exc.stderr or exc.stdout or str(exc)).strip()
            results.append(PublishResult(skill=skill_name, status="failed", branch=branch, note=note[:500]))

    report_path = (REPO_ROOT / args.report).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "target_repo": UPSTREAM_REPO,
        "head_owner": PUBLISH_OWNER,
        "base_commit": run(["git", "rev-parse", "HEAD"], cwd=LOCAL_HERMES_REPO).stdout.strip(),
        "requested": args.skills or [],
        "results": [
            {
                "skill": item.skill,
                "status": item.status,
                "branch": f"{PUBLISH_OWNER}:{item.branch}",
                "pr_url": item.pr_url,
                "note": item.note,
            }
            for item in results
        ],
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for item in results:
        summary = f"{item.skill}: {item.status}"
        if item.pr_url:
            summary += f" -> {item.pr_url}"
        elif item.note:
            summary += f" ({item.note})"
        print(summary)
    print(f"Report written to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
