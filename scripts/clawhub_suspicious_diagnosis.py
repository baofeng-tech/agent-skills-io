#!/usr/bin/env python3
"""Turn live ClawHub scan results into stable diagnosis JSON and doc updates."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATUS_FILE = REPO_ROOT / "targets" / "clawhub-live-status.json"
DEFAULT_PUBLISH_STATE = REPO_ROOT / "targets" / "clawhub-publish-state.json"
DEFAULT_OUTPUT_FILE = REPO_ROOT / "targets" / "clawhub-suspicious-diagnosis.json"
DEFAULT_DOC_FILE = REPO_ROOT / "targets" / "clawhub-suspicious-causes-and-fixes-2026-04-25.md"
AUTO_BEGIN = "<!-- AUTO-DIAGNOSIS:BEGIN -->"
AUTO_END = "<!-- AUTO-DIAGNOSIS:END -->"

RULES: dict[str, dict[str, Any]] = {
    "pending_scan": {
        "severity": "warning",
        "keywords": ("pending", "unresolved"),
        "summary": "Security scan output is not final yet.",
        "actions": [
            "Keep pending, clean, and suspicious as separate states in automation.",
            "Retry live scan before treating the package as resolved.",
        ],
    },
    "relay_trust_surface": {
        "severity": "blocker",
        "keywords": ("relay", "api.aisa.one", "third-party", "aisa_api_key"),
        "summary": "Relay/API trust surface is under-described for the shipped package.",
        "actions": [
            "State the network target and secret flow explicitly in SKILL.md, README, and manifests.",
            "Keep the auth story API-key-only unless the runtime truly needs more.",
        ],
    },
    "oauth_upload_side_effects": {
        "severity": "blocker",
        "keywords": ("oauth", "upload", "media", "posting", "post on your behalf"),
        "summary": "OAuth, posting, or media-upload side effects are not explicit enough.",
        "actions": [
            "Explain user approval, upload paths, and posting behavior in publish-facing docs.",
            "Avoid phrasing that makes posting look silent or automatic by default.",
        ],
    },
    "metadata_env_mismatch": {
        "severity": "blocker",
        "keywords": ("manifest", "metadata", "registry", "env", "requirement mismatch", "omitted"),
        "summary": "Registry/manifest/docs/env requirements drifted away from the shipped runtime.",
        "actions": [
            "Align SKILL.md, README, package manifests, and registry-facing metadata.",
            "Declare every required env var in the same shape across all publish layers.",
        ],
    },
    "prompt_scaffold_copy": {
        "severity": "warning",
        "keywords": ("prompt-injection", "prescriptive prompts", "prompt scaffold", "highly prescriptive"),
        "summary": "Public copy looks like exposed prompt scaffolding rather than user-facing instructions.",
        "actions": [
            "Rewrite public SKILL.md copy in user/task language.",
            "Keep internal prompting strategy out of the public package surface.",
        ],
    },
    "platform_trust_gap": {
        "severity": "warning",
        "keywords": ("trust", "coherent", "provenance", "source", "publisher"),
        "summary": "Trust and provenance surfaces are weaker than the package behavior requires.",
        "actions": [
            "Keep source links, manifests, and README provenance aligned.",
            "Make external writes, uploads, and remote execution boundaries easy to verify.",
        ],
    },
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip().lower()


def classify_rules(item: dict[str, Any]) -> list[str]:
    reason = normalize_text(item.get("suspicious_reason"))
    status = normalize_text(item.get("scan_status"))
    matched: list[str] = []
    if item.get("pending") or status in {"pending", "unresolved"}:
        matched.append("pending_scan")
    for rule_id, meta in RULES.items():
        if rule_id == "pending_scan":
            continue
        if any(keyword in reason for keyword in meta["keywords"]):
            matched.append(rule_id)
    if not matched and item.get("suspicious"):
        matched.append("platform_trust_gap")
    return sorted(dict.fromkeys(matched))


def render_artifact_record(item: dict[str, Any], publish_meta: dict[str, Any]) -> dict[str, Any]:
    rule_ids = classify_rules(item)
    recommendations: list[str] = []
    severities = [RULES[rule_id]["severity"] for rule_id in rule_ids if rule_id in RULES]
    for rule_id in rule_ids:
        recommendations.extend(RULES[rule_id]["actions"])
    severity = "blocker" if "blocker" in severities else "warning" if severities else "note"
    return {
        "key": item.get("key"),
        "kind": item.get("kind"),
        "name": item.get("name"),
        "severity": severity,
        "scan_status": item.get("scan_status"),
        "virus_total": item.get("virus_total"),
        "openclaw_verdict": item.get("openclaw_verdict"),
        "suspicious": bool(item.get("suspicious")),
        "pending": bool(item.get("pending")),
        "rule_ids": rule_ids,
        "rule_summaries": [RULES[rule_id]["summary"] for rule_id in rule_ids if rule_id in RULES],
        "recommended_actions": recommendations,
        "detail_url": item.get("detail_url"),
        "local_path": publish_meta.get("path"),
        "release_ref": publish_meta.get("release_ref"),
        "reason": item.get("suspicious_reason"),
    }


def build_payload(status_payload: dict[str, Any], publish_payload: dict[str, Any]) -> dict[str, Any]:
    publish_artifacts = publish_payload.get("artifacts") or {}
    artifacts = [
        render_artifact_record(item, publish_artifacts.get(str(item.get("key") or ""), {}))
        for item in (status_payload.get("artifacts") or [])
        if item.get("suspicious") or item.get("pending")
    ]
    artifacts.sort(key=lambda item: (item["severity"] != "blocker", item["kind"], item["name"]))
    rule_counter = Counter(rule_id for artifact in artifacts for rule_id in artifact["rule_ids"])
    return {
        "summary": {
            "artifacts": len(artifacts),
            "blockers": sum(1 for item in artifacts if item["severity"] == "blocker"),
            "warnings": sum(1 for item in artifacts if item["severity"] == "warning"),
            "pending": sum(1 for item in artifacts if item["pending"]),
            "rules": dict(sorted(rule_counter.items())),
        },
        "artifacts": artifacts,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_doc_block(payload: dict[str, Any]) -> str:
    lines = [
        "## 最新自动诊断快照",
        "",
        "- 诊断对象数：`{}`".format(payload["summary"]["artifacts"]),
        "- `blocker`：`{}`".format(payload["summary"]["blockers"]),
        "- `warning`：`{}`".format(payload["summary"]["warnings"]),
        "- `pending`：`{}`".format(payload["summary"]["pending"]),
        "",
        "### 当前高频规则",
        "",
    ]
    rules = payload["summary"]["rules"]
    if rules:
        for rule_id, count in rules.items():
            lines.append(f"- `{rule_id}`: `{count}`")
    else:
        lines.append("- 当前没有待处理的 suspicious / pending 诊断项。")

    lines.extend(["", "### 当前重点对象", ""])
    if payload["artifacts"]:
        for item in payload["artifacts"][:12]:
            lines.append(f"- `{item['key']}`")
            lines.append(f"  severity: `{item['severity']}` | status: `{item['scan_status'] or '-'}`")
            if item["rule_ids"]:
                lines.append(f"  rules: `{', '.join(item['rule_ids'])}`")
            if item.get("reason"):
                lines.append(f"  reason: {item['reason']}")
    else:
        lines.append("- 当前没有待处理对象。")
    return "\n".join(lines).rstrip() + "\n"


def update_doc(path: Path, payload: dict[str, Any]) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    block = f"{AUTO_BEGIN}\n{render_doc_block(payload)}{AUTO_END}\n"
    if AUTO_BEGIN in current and AUTO_END in current:
        updated = re.sub(
            rf"{re.escape(AUTO_BEGIN)}[\s\S]*?{re.escape(AUTO_END)}\n?",
            block,
            current,
            count=1,
        )
    else:
        suffix = "" if current.endswith("\n") or not current else "\n"
        updated = f"{current}{suffix}\n{block}"
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate structured ClawHub suspicious diagnosis output.")
    parser.add_argument("--status-file", default=str(DEFAULT_STATUS_FILE), help="Live scan JSON input.")
    parser.add_argument("--publish-state-file", default=str(DEFAULT_PUBLISH_STATE), help="Publish state JSON input.")
    parser.add_argument("--output-file", default=str(DEFAULT_OUTPUT_FILE), help="Diagnosis JSON output.")
    parser.add_argument(
        "--doc-file",
        default=str(DEFAULT_DOC_FILE),
        help="Rules doc to update with a generated diagnosis snapshot.",
    )
    parser.add_argument(
        "--doc-mode",
        choices=("skip", "update"),
        default="skip",
        help="Whether to update the diagnosis snapshot block inside the rules doc.",
    )
    args = parser.parse_args()

    status_payload = load_json(Path(args.status_file).resolve())
    publish_payload = load_json(Path(args.publish_state_file).resolve())
    payload = build_payload(status_payload, publish_payload)
    write_json(Path(args.output_file).resolve(), payload)
    if args.doc_mode == "update":
        update_doc(Path(args.doc_file).resolve(), payload)
    print(
        "Diagnosis generated: "
        f"{payload['summary']['artifacts']} artifacts, "
        f"{payload['summary']['blockers']} blockers, "
        f"{payload['summary']['warnings']} warnings."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
