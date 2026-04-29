#!/usr/bin/env python3
"""Turn live ClawHub scan results into stable diagnosis JSON and doc updates."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_SKILL_ROOT = REPO_ROOT / "targetSkills"
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
    "static_analysis_patterns": {
        "severity": "blocker",
        "keywords": ("static analysis", "pattern detected", "child_process", "shell command execution"),
        "summary": "Static analysis found execution or side-effect patterns that need trimming or clearer justification.",
        "actions": [
            "Remove non-runtime helper files from the shipped package when they are the source of the finding.",
            "If the pattern is a real runtime need, explain the exact boundary and intended command/file behavior in public docs.",
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


def load_frontmatter(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1]) or {}
    return data if isinstance(data, dict) else {}


def resolve_clawhub_slug(skill_name: str, frontmatter: dict[str, Any]) -> str:
    metadata = frontmatter.get("metadata") if isinstance(frontmatter.get("metadata"), dict) else {}
    candidates: list[Any] = [
        frontmatter.get("clawhub-slug"),
        frontmatter.get("clawhub_slug"),
    ]
    for scope in ("clawhub", "openclaw", "aisa"):
        scoped = metadata.get(scope) if isinstance(metadata, dict) else None
        if not isinstance(scoped, dict):
            continue
        candidates.extend(
            [
                scoped.get("slug"),
                scoped.get("clawhubSlug"),
                scoped.get("clawhub_slug"),
            ]
        )
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return skill_name


def build_clawhub_alias_maps() -> tuple[dict[str, str], dict[str, str]]:
    source_to_alias: dict[str, str] = {}
    alias_to_source: dict[str, str] = {}
    if not TARGET_SKILL_ROOT.exists():
        return source_to_alias, alias_to_source

    for skill_dir in sorted(path for path in TARGET_SKILL_ROOT.iterdir() if path.is_dir()):
        frontmatter = load_frontmatter(skill_dir / "SKILL.md")
        alias = resolve_clawhub_slug(skill_dir.name, frontmatter)
        source_to_alias[skill_dir.name] = alias
        alias_to_source[alias] = skill_dir.name
    return source_to_alias, alias_to_source


def resolve_source_skill_name(kind: str, name: str, alias_to_source: dict[str, str]) -> str | None:
    if kind == "skill":
        if (TARGET_SKILL_ROOT / name / "SKILL.md").exists():
            return name
        return alias_to_source.get(name)

    if kind == "plugin" and name.endswith("-plugin"):
        base = name[: -len("-plugin")]
        if (TARGET_SKILL_ROOT / base / "SKILL.md").exists():
            return base
        return alias_to_source.get(base)

    return None


def current_artifact_key(kind: str, source_skill: str, source_to_alias: dict[str, str]) -> str:
    alias = source_to_alias.get(source_skill) or source_skill
    if kind == "plugin":
        return f"plugin:{alias}-plugin"
    return f"skill:{alias}"


def is_superseded_by_clean_alias(
    item: dict[str, Any],
    status_lookup: dict[str, dict[str, Any]],
    source_to_alias: dict[str, str],
    alias_to_source: dict[str, str],
) -> bool:
    kind = str(item.get("kind") or "").strip()
    name = str(item.get("name") or "").strip()
    key = str(item.get("key") or "").strip()
    if kind not in {"skill", "plugin"} or not name or not key:
        return False

    source_skill = resolve_source_skill_name(kind, name, alias_to_source)
    if not source_skill:
        return False

    current_key = current_artifact_key(kind, source_skill, source_to_alias)
    if current_key == key:
        return False

    current_item = status_lookup.get(current_key)
    if not isinstance(current_item, dict):
        return False

    return not bool(current_item.get("suspicious")) and not bool(current_item.get("pending"))


def classify_rules(item: dict[str, Any]) -> list[str]:
    reason = normalize_text(item.get("suspicious_reason"))
    status = normalize_text(item.get("scan_status"))
    static_status = normalize_text(item.get("static_analysis_status"))
    static_summary = normalize_text(item.get("static_analysis_summary"))
    matched: list[str] = []
    if item.get("pending") or status in {"pending", "unresolved"}:
        matched.append("pending_scan")
    if static_status in {"warning", "suspicious", "malicious"} or "pattern detected" in static_summary:
        matched.append("static_analysis_patterns")
    for rule_id, meta in RULES.items():
        if rule_id in {"pending_scan", "static_analysis_patterns"}:
            continue
        if any(keyword in reason or keyword in static_summary for keyword in meta["keywords"]):
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
        "publisher_handle": item.get("publisher_handle"),
        "severity": severity,
        "scan_status": item.get("scan_status"),
        "virus_total": item.get("virus_total"),
        "clawscan_verdict": item.get("clawscan_verdict") or item.get("openclaw_verdict"),
        "openclaw_verdict": item.get("openclaw_verdict"),
        "static_analysis_status": item.get("static_analysis_status"),
        "static_analysis_summary": item.get("static_analysis_summary"),
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
    source_to_alias, alias_to_source = build_clawhub_alias_maps()
    status_items = [item for item in (status_payload.get("artifacts") or []) if isinstance(item, dict)]
    status_lookup = {
        str(item.get("key") or "").strip(): item
        for item in status_items
        if str(item.get("key") or "").strip()
    }
    artifacts = [
        render_artifact_record(item, publish_artifacts.get(str(item.get("key") or ""), {}))
        for item in status_items
        if item.get("suspicious") or item.get("pending")
        if not is_superseded_by_clean_alias(item, status_lookup, source_to_alias, alias_to_source)
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
