#!/usr/bin/env python3
"""Static regression checks for the unified GitHub Actions workflow."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "unified-skill-pipeline.yml"
RUNS_ON_EXPR = "${{ fromJSON(needs['self-hosted-preflight'].outputs.runs_on_json || '[\"self-hosted\"]') }}"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_outputs(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value
    return values


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def validate_continuation_planner() -> None:
    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        state = tmp / "state.json"
        diagnosis = tmp / "diagnosis.json"
        variants = tmp / "variants.json"
        live = tmp / "live.json"
        output = tmp / "github-output.txt"

        write_json(state, {"last_run": {"synced_skills": ["aisa-twitter-api"], "created_skills": []}})
        write_json(
            diagnosis,
            {
                "artifacts": [
                    {
                        "key": "plugin:aisa-twitter-api-plugin",
                        "publisher_handle": "bibaofeng",
                        "severity": "blocker",
                        "scan_status": "suspicious",
                        "suspicious": True,
                    }
                ]
            },
        )
        write_json(variants, {"variants": [{"source": "aisa-twitter-api", "slug": "aisa-twitter-command"}]})
        write_json(
            live,
            {
                "artifacts": [
                    {"key": "skill:aisa-twitter-command", "scan_status": "clean", "suspicious": False, "pending": False},
                    {
                        "key": "plugin:aisa-twitter-command-plugin",
                        "scan_status": "clean",
                        "suspicious": False,
                        "pending": False,
                    },
                ]
            },
        )

        result = subprocess.run(
            [
                sys.executable,
                "scripts/plan_workflow_continuation.py",
                "--state-file",
                str(state),
                "--diagnosis-file",
                str(diagnosis),
                "--breakout-file",
                str(variants),
                "--live-status-file",
                str(live),
                "--github-output",
                str(output),
                "--ignore-git-status",
            ],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        require(result.returncode == 0, f"continuation planner failed: {result.stderr}")
        values = read_outputs(output)
        require(values.get("publish_requested") == "true", "planner must auto-request publish for synced skills")
        require(
            values.get("suspicious_requested") == "true",
            "planner must auto-request suspicious repair for owned suspicious blockers",
        )
        require(
            values.get("breakout_requested") == "true",
            "planner must auto-request breakout rollout when a breakout source changed",
        )

        output.unlink()
        write_json(state, {"last_run": {"synced_skills": [], "created_skills": []}})
        write_json(
            diagnosis,
            {
                "artifacts": [
                    {
                        "key": "skill:web-search",
                        "publisher_handle": "someone-else",
                        "severity": "blocker",
                        "scan_status": "suspicious",
                        "suspicious": True,
                    }
                ]
            },
        )
        write_json(variants, {"variants": [{"source": "aisa-twitter-api", "slug": "aisa-twitter-command"}]})
        result = subprocess.run(
            [
                sys.executable,
                "scripts/plan_workflow_continuation.py",
                "--state-file",
                str(state),
                "--diagnosis-file",
                str(diagnosis),
                "--breakout-file",
                str(variants),
                "--live-status-file",
                str(live),
                "--github-output",
                str(output),
                "--ignore-git-status",
            ],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        require(result.returncode == 0, f"continuation planner no-work case failed: {result.stderr}")
        values = read_outputs(output)
        require(values.get("publish_requested") == "false", "planner must skip publish when no release work exists")
        require(
            values.get("suspicious_requested") == "false",
            "planner must skip non-owned suspicious blockers by default",
        )
        require(
            values.get("breakout_requested") == "false",
            "planner must skip clean breakout variants when their sources did not change",
        )


def validate_continuation_dirty_filter() -> None:
    import plan_workflow_continuation as planner

    require(
        not planner.generated_release_dirty(
            [
                "targetSkills/us-stock-analyst/AAPL_analysis_20260508.json",
                "targets/aisa-api-regression-report-2026-05-08.json",
            ]
        ),
        "planner must not request publish continuation for AISA smoke/report output only",
    )
    require(
        planner.generated_release_dirty(["targetSkills/aisa-twitter-api/SKILL.md"]),
        "planner must still request publish continuation for real targetSkills source changes",
    )


def validate_prediction_market_client_hardening() -> None:
    """Lock the upstream-sync hardening that keeps prediction-market smoke tests stable."""
    import unified_skill_pipeline as pipeline

    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        client = tmp / "prediction_market_client.py"
        client.write_text(
            '''\
import json
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


class PredictionMarketClient:
    """Small fixture that mirrors the upstream client shape."""

    def _request(self) -> Dict[str, Any]:
        req = urllib.request.Request("https://example.test")
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as e:
            return {"success": False, "error": {"code": "NETWORK_ERROR", "message": str(e.reason)}}

    def _raw_get(self) -> Dict[str, Any]:
        req = urllib.request.Request("https://example.test")
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as e:
            return {"success": False, "error": {"code": "NETWORK_ERROR", "message": str(e.reason)}}


def main() -> None:
    result = []
    sys.exit(0 if result.get("success", True) else 1)
''',
            encoding="utf-8",
        )

        require(
            pipeline.harden_prediction_market_client(client),
            "pipeline must patch upstream prediction-market clients after sync",
        )
        hardened = client.read_text(encoding="utf-8")
        require("def api_result_ok(result: Any) -> bool:" in hardened, "hardener must add list-safe exit logic")
        require("def decode_json_body(body: bytes) -> Dict[str, Any]:" in hardened, "hardener must add JSON decoder")
        require(
            hardened.count("return decode_json_body(response.read())") == 2,
            "hardener must wrap both normal request paths",
        )
        require("except TimeoutError as e:" in hardened, "hardener must classify timeout errors as network errors")
        require(
            "sys.exit(0 if api_result_ok(result) else 1)" in hardened,
            "hardener must avoid calling dict.get on list payloads",
        )
        require(
            not pipeline.harden_prediction_market_client(client),
            "prediction-market hardening must be idempotent",
        )


def main() -> int:
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    dispatch_block = text.split("workflow_dispatch:", 1)[1].split("schedule:", 1)[0]
    dispatch_input_count = len(re.findall(r"^      [A-Za-z_][A-Za-z0-9_]*:\n", dispatch_block, flags=re.MULTILINE))

    require(
        "SELF_HOSTED_RUNNER_LABELS" not in text,
        "legacy SELF_HOSTED_RUNNER_LABELS must not reappear; use SELF_HOSTED_RUNNER_RUNS_ON_JSON only",
    )
    require(
        "SELF_HOSTED_RUNNER_RUNS_ON_JSON: ${{ vars.SELF_HOSTED_RUNNER_RUNS_ON_JSON || '[\"self-hosted\"]' }}" in text,
        "preflight must read the same runner JSON used by self-hosted runs-on",
    )
    require(
        "run_self_hosted_publish:\n        description: \"Publish continuation mode after hosted validation\"\n        required: false\n        default: auto\n        type: choice" in text
        and "run_suspicious_repair:\n        description: \"Suspicious remediation continuation mode after diagnosis\"\n        required: false\n        default: auto\n        type: choice" in text
        and "run_breakout_rollout:\n        description: \"Breakout rollout continuation mode\"\n        required: false\n        default: auto\n        type: choice" in text,
        "manual dispatch continuation controls must default to auto, not a hard false skip",
    )
    require(
        dispatch_input_count <= 25 and "allow_hosted_continuation:" not in text,
        "workflow_dispatch must stay within GitHub's 25-input limit; hosted fallback is controlled by repo variable",
    )
    require(
        "CONTINUATION_PUBLISH_MODE: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.run_self_hosted_publish || vars.AUTO_FULL_PLATFORM_PUBLISH || 'auto' }}" in text
        and "CONTINUATION_SUSPICIOUS_MODE: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.run_suspicious_repair || vars.AUTO_RUN_SUSPICIOUS_REPAIR || 'auto' }}" in text
        and "CONTINUATION_BREAKOUT_MODE: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.run_breakout_rollout || vars.AUTO_RUN_BREAKOUT_ROLLOUT || 'auto' }}" in text,
        "scheduled continuation lanes must default to auto planning instead of false",
    )
    require(
        "python3 scripts/plan_workflow_continuation.py" in text
        and "publish_requested: ${{ steps.continuation.outputs.publish_requested }}" in text
        and "PLANNED_PUBLISH_REQUESTED: ${{ needs.sync-build-test.outputs.publish_requested || 'false' }}" in text,
        "workflow must plan continuation lanes from hosted pipeline outputs before preflight",
    )
    require(
        "suspicious_rescan_wait_seconds:" in text
        and "PIPELINE_SUSPICIOUS_RESCAN_WAIT_SECONDS" in text
        and '"--rescan-before-repair"' in text
        and '"--rescan-wait-seconds" "${PIPELINE_SUSPICIOUS_RESCAN_WAIT_SECONDS:-180}"' in text,
        "suspicious remediation must request a ClawHub rescan before editing or republishing",
    )
    remediation_text = (REPO_ROOT / "scripts" / "clawhub_suspicious_remediation.py").read_text(encoding="utf-8")
    pipeline_text = (REPO_ROOT / "scripts" / "unified_skill_pipeline.py").read_text(encoding="utf-8")
    require(
        '"--slug-conflict-strategy"' in remediation_text
        and 'default="fail"' in remediation_text
        and "do not repair the flagged URL" in remediation_text,
        "targeted suspicious remediation must fail on slug conflicts instead of publishing fallback slugs",
    )
    require(
        "No upstream skill changes detected." in pipeline_text
        and "state_needs_no_change_refresh = (" in pipeline_text
        and "or any(\n                last_run.get(field)" in pipeline_text
        and '"last_run": asdict(summary)' in pipeline_text,
        "unified pipeline must refresh stale last_run on no-change runs without self-committing every empty run",
    )
    require(
        text.count(f"runs-on: {RUNS_ON_EXPR}") == 3,
        "the three continuation lanes must all use the preflight-selected runs-on target",
    )
    require(
        'if [[ "${any_requested}" == "true" && "${can_queue}" != "true" ]]; then' in text
        and 'echo "::error title=Self-hosted runner preflight::${reason}"' in text
        and "exit 1" in text,
        "requested continuation lanes must still fail fast if neither self-hosted nor hosted fallback can run them",
    )
    require(
        "AUTO_ALLOW_HOSTED_CONTINUATION: ${{ vars.AUTO_ALLOW_HOSTED_CONTINUATION || 'true' }}" in text
        and "runs_on_json='[\"ubuntu-latest\"]'" in text
        and "using GitHub-hosted continuation fallback" in text,
        "preflight must be able to use hosted continuation fallback when no self-hosted runner is online",
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
        "- Continuation lanes can run: " in text
        and "- Runner decision: GitHub-hosted fallback selected after self-hosted inventory did not match" in text
        and "- Can queue self-hosted jobs: " not in text,
        "preflight summaries must distinguish continuation executability from self-hosted queue availability",
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
    require(
        "PIPELINE_AISA_API_REGRESSION_TIMEOUT: ${{ vars.AUTO_AISA_API_REGRESSION_TIMEOUT || '45' }}" in text
        and "PIPELINE_AISA_API_REGRESSION_RETRIES: ${{ vars.AUTO_AISA_API_REGRESSION_RETRIES || '0' }}" in text
        and "--timeout \"${PIPELINE_AISA_API_REGRESSION_TIMEOUT:-45}\"" in text
        and "--retries \"${PIPELINE_AISA_API_REGRESSION_RETRIES:-0}\"" in text,
        "hosted AISA regression must be bounded by CI-level timeout and retry controls",
    )
    aisa_regression_text = (REPO_ROOT / "scripts" / "test_aisa_api_skills.py").read_text(encoding="utf-8")
    require(
        "AISA API regression [{index}]" in aisa_regression_text and "flush=True" in aisa_regression_text,
        "AISA regression must print per-command progress so CI logs do not look stuck",
    )
    require(
        "except subprocess.TimeoutExpired as exc:" in aisa_regression_text
        and "Command timed out after {timeout} seconds" in aisa_regression_text
        and "subprocess.CompletedProcess(" in aisa_regression_text,
        "AISA regression command timeouts must become transient results instead of crashing the runner",
    )
    require(
        "AISA_REGRESSION_OUTPUT_DIR" in aisa_regression_text
        and "aisa-api-regression-stock-analyst" in aisa_regression_text
        and '"--output"' in aisa_regression_text,
        "AISA regression smoke commands must write stock analyst output outside targetSkills",
    )
    require(
        "targets/aisa-api-regression-report-*.json targetSkills/*/*_analysis_*.json" in text
        and "git restore --staged --worktree -- \"$report\"" in text,
        "hosted auto-commit must exclude AISA smoke/report outputs so validation HEAD does not drift",
    )
    require(
        "harden_synced_skill_runtime(dst_dir)" in pipeline_text
        and "harden_prediction_market_client" in pipeline_text
        and "UPSTREAM_NON_JSON" in pipeline_text,
        "unified pipeline must preserve prediction-market client hardening after upstream all-sync",
    )
    validate_continuation_planner()
    validate_continuation_dirty_filter()
    validate_prediction_market_client_hardening()
    print("GitHub Actions workflow guard checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"workflow guard check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
