#!/usr/bin/env python3
"""Static regression checks for the unified GitHub Actions workflow."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "unified-skill-pipeline.yml"
RUNS_ON_EXPR = "${{ fromJSON(vars.SELF_HOSTED_RUNNER_RUNS_ON_JSON || '[\"self-hosted\"]') }}"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    text = WORKFLOW_PATH.read_text(encoding="utf-8")

    require(
        "SELF_HOSTED_RUNNER_LABELS" not in text,
        "legacy SELF_HOSTED_RUNNER_LABELS must not reappear; use SELF_HOSTED_RUNNER_RUNS_ON_JSON only",
    )
    require(
        "SELF_HOSTED_RUNNER_RUNS_ON_JSON: ${{ vars.SELF_HOSTED_RUNNER_RUNS_ON_JSON || '[\"self-hosted\"]' }}" in text,
        "preflight must read the same runner JSON used by self-hosted runs-on",
    )
    require(
        "run_self_hosted_publish:\n        description: \"Also run the optional self-hosted publish lane\"\n        required: false\n        default: false" in text
        and "run_suspicious_repair:\n        description: \"After diagnosis, remediate matching suspicious artifacts and republish them\"\n        required: false\n        default: false" in text
        and "run_breakout_rollout:\n        description: \"Run the dedicated breakout rollout lane\"\n        required: false\n        default: false" in text,
        "manual dispatch must not request self-hosted lanes by default when no runner is guaranteed",
    )
    require(
        "AUTO_FULL_PLATFORM_PUBLISH: ${{ vars.AUTO_FULL_PLATFORM_PUBLISH || 'false' }}" in text
        and "AUTO_RUN_SUSPICIOUS_REPAIR: ${{ vars.AUTO_RUN_SUSPICIOUS_REPAIR || 'false' }}" in text
        and "AUTO_RUN_BREAKOUT_ROLLOUT: ${{ vars.AUTO_RUN_BREAKOUT_ROLLOUT || 'false' }}" in text,
        "scheduled self-hosted lanes must be opt-in through repository variables",
    )
    require(
        "suspicious_rescan_wait_seconds:" in text
        and "PIPELINE_SUSPICIOUS_RESCAN_WAIT_SECONDS" in text
        and '"--rescan-before-repair"' in text
        and '"--rescan-wait-seconds" "${PIPELINE_SUSPICIOUS_RESCAN_WAIT_SECONDS:-180}"' in text,
        "suspicious remediation must request a ClawHub rescan before editing or republishing",
    )
    remediation_text = (REPO_ROOT / "scripts" / "clawhub_suspicious_remediation.py").read_text(encoding="utf-8")
    require(
        '"--slug-conflict-strategy"' in remediation_text
        and 'default="fail"' in remediation_text
        and "do not repair the flagged URL" in remediation_text,
        "targeted suspicious remediation must fail on slug conflicts instead of publishing fallback slugs",
    )
    require(
        text.count(f"runs-on: {RUNS_ON_EXPR}") == 3,
        "the three self-hosted lanes must all use SELF_HOSTED_RUNNER_RUNS_ON_JSON",
    )
    require(
        'if [[ "${any_requested}" == "true" && "${can_queue}" != "true" ]]; then' in text
        and 'echo "::error title=Self-hosted runner preflight::${reason}"' in text
        and "exit 1" in text,
        "requested self-hosted lanes must fail fast when no matching runner is confirmed",
    )
    require(
        '"https://api.github.com/users/${owner}"' in text
        and '"${owner_type}" == "organization"' in text
        and '"${owner_type}" == "user"' in text
        and "organization-runner fallback is not applicable" in text,
        "preflight must verify owner type and skip org-runner fallback for personal repositories",
    )
    require(
        "SELF_HOSTED_RUNNER_RUNS_ON_JSON only selects labels and does not register or start a runner" in text,
        "zero-runner failures must explain that labels are not runner registration",
    )
    require(
        "force_self_hosted_queue enabled" in text,
        "manual force queue mode must stay explicit in summaries",
    )
    require(
        "python3 scripts/test_clawhub_batch_publish_exit.py" in text,
        "hosted validation must cover ClawHub batch publish exit-code semantics",
    )
    require(
        "python3 scripts/test_clawhub_live_status_review.py" in text,
        "hosted validation must cover ClawHub Review verdict semantics",
    )
    require(
        "python3 scripts/test_clawhub_plugin_auth_metadata.py" in text,
        "hosted validation must cover ClawHub plugin auth metadata",
    )
    require(
        "python3 scripts/test_twitter_oauth_client_safety.py" in text,
        "hosted validation must cover Twitter OAuth public-write safety",
    )
    print("GitHub Actions workflow guard checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"workflow guard check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
