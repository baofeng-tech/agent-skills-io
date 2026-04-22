#!/usr/bin/env python3
"""Normalize targetSkills/ SKILL.md frontmatter to the repo source-skill standard."""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

import build_claude_release as base


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "targetSkills"


def infer_emoji(name: str, description: str) -> str:
    lower = f"{name} {description}".lower()
    if "twitter" in lower or lower.startswith("x-"):
        return "🐦"
    if "youtube" in lower:
        return "▶️"
    if any(token in lower for token in ("search", "tavily", "perplexity", "scholar")):
        return "🔎"
    if any(token in lower for token in ("stock", "market", "portfolio", "dividend", "prediction", "finance")):
        return "📊"
    if any(token in lower for token in ("media", "image", "video")):
        return "🎬"
    if any(token in lower for token in ("llm", "provider", "router", "model")):
        return "🤖"
    if "last30days" in lower:
        return "📰"
    return "🛠"


def infer_required_bins(skill_dir: Path) -> list[str]:
    suffixes = {path.suffix.lower() for path in skill_dir.rglob("*") if path.is_file()}
    bins: list[str] = []
    if ".py" in suffixes:
        bins.append("python3")
    if ".sh" in suffixes:
        bins.append("bash")
    if {".js", ".mjs", ".cjs", ".ts"} & suffixes:
        bins.append("node")
    text_blob = collect_text_blob(skill_dir)
    heuristics = (
        (r"(?m)^\s*curl\b", "curl"),
        (r"(?m)^\s*(?:python3?|uv run)\b", "python3"),
        (r"(?m)^\s*openclaw\b", "openclaw"),
        (r"(?m)^\s*jq\b", "jq"),
    )
    for pattern, bin_name in heuristics:
        if re.search(pattern, text_blob) and bin_name not in bins:
            bins.append(bin_name)
    return bins


def infer_envs(skill_dir: Path) -> list[str]:
    envs: list[str] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "AISA_API_KEY" in text and "AISA_API_KEY" not in envs:
            envs.append("AISA_API_KEY")
    return envs


def collect_text_blob(skill_dir: Path) -> str:
    chunks: list[str] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
    return "\n".join(chunks)


def detect_domain(name: str, description: str) -> str:
    lower = f"{name} {description}".lower()
    if "twitter" in lower or lower.startswith("x-"):
        return "twitter"
    if "youtube" in lower:
        return "youtube"
    if "last30days" in lower:
        return "research"
    if any(token in lower for token in ("search", "tavily", "perplexity", "scholar", "web-search", "multi-search")):
        return "search"
    if any(token in lower for token in ("stock", "market", "portfolio", "dividend", "prediction", "finance")):
        return "finance"
    if any(token in lower for token in ("media", "image", "video")):
        return "media"
    if any(token in lower for token in ("llm", "provider", "router", "qwen", "deepseek", "kimi")):
        return "ai"
    return "automation"


def strip_use_when(description: str) -> str:
    if "触发条件：" in description:
        return description.split("触发条件：", 1)[0].rstrip(" 。.")
    return re.sub(r"\s*Use when:.*$", "", description, flags=re.IGNORECASE).rstrip(" .")


def description_conflicts_with_name(name: str, description: str) -> bool:
    name_domain = detect_domain(name, name)
    when_to_use = base.extract_when_to_use(description) or description
    desc_domain = detect_domain(when_to_use, when_to_use)
    if name_domain == "automation" or desc_domain == "automation":
        return False
    return name_domain != desc_domain


def normalize_skill_description(name: str, description: str) -> str:
    cleaned = base.normalize_description(name, description)
    if not description_conflicts_with_name(name, cleaned):
        return cleaned
    core = strip_use_when(cleaned)
    repaired = f"{core}. Use when: {infer_use_when_from_name(name)}."
    return " ".join(repaired.split())


def infer_use_when_from_name(name: str) -> str:
    domain = detect_domain(name, name)
    mapping = {
        "twitter": "the user needs X/Twitter research, monitoring, posting, or engagement workflows",
        "youtube": "the user needs YouTube search, trend discovery, channel research, or SERP analysis",
        "research": "the user needs recent multi-source research across the last 30 days",
        "search": "the user needs web search, research, source discovery, or content extraction",
        "finance": "the user needs market data, stock analysis, watchlists, or portfolio workflows",
        "media": "the user needs AI image or video generation workflows",
        "ai": "the user needs model routing, provider setup, or Chinese LLM access guidance",
        "automation": "the user needs this workflow's domain-specific automation or guidance",
    }
    return mapping[domain]


def build_compatibility(name: str, bins: list[str], envs: list[str]) -> str | None:
    requirements: list[str] = []
    if bins:
        requirements.append("system binaries " + ", ".join(bins))
    if envs:
        requirements.append("environment variables " + ", ".join(envs))
    if envs and "AISA_API_KEY" in envs:
        requirements.append("internet access to api.aisa.one")
    base_text = "Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs."
    if not requirements:
        return base_text
    joined = ", ".join(requirements[:-1]) + (" and " + requirements[-1] if len(requirements) > 1 else requirements[0])
    text = f"{base_text} Requires {joined}."
    return text[:500]


def extract_metadata(frontmatter: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    metadata = frontmatter.get("metadata") or {}
    if not isinstance(metadata, dict):
        return {}, {}
    aisa = metadata.get("aisa") or {}
    openclaw = metadata.get("openclaw") or {}
    if not isinstance(aisa, dict):
        aisa = {}
    if not isinstance(openclaw, dict):
        openclaw = {}
    return aisa, openclaw


def compact_none(data: Any) -> Any:
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            compacted = compact_none(value)
            if compacted in (None, "", [], {}):
                continue
            result[key] = compacted
        return result
    if isinstance(data, list):
        return [compact_none(item) for item in data if compact_none(item) not in (None, "", [], {})]
    return data


def normalize_skill(skill_dir: Path) -> bool:
    skill_path = skill_dir / "SKILL.md"
    frontmatter, body = base.load_frontmatter(skill_path)

    name = str(frontmatter.get("name") or skill_dir.name).strip()
    name = skill_dir.name
    description = normalize_skill_description(name, str(frontmatter.get("description") or ""))
    aisa_meta, openclaw_meta = extract_metadata(frontmatter)

    envs = (
        list((aisa_meta.get("requires") or {}).get("env") or [])
        or list((openclaw_meta.get("requires") or {}).get("env") or [])
        or infer_envs(skill_dir)
    )
    bins = (
        list((aisa_meta.get("requires") or {}).get("bins") or [])
        or list((openclaw_meta.get("requires") or {}).get("bins") or [])
        or infer_required_bins(skill_dir)
    )
    primary_env = aisa_meta.get("primaryEnv") or openclaw_meta.get("primaryEnv") or (envs[0] if envs else None)
    compatibility = list(aisa_meta.get("compatibility") or ["openclaw", "claude-code", "hermes"])
    emoji = str(aisa_meta.get("emoji") or openclaw_meta.get("emoji") or infer_emoji(name, description))

    cleaned: dict[str, Any] = {
        "name": name,
        "description": description,
    }
    license_value = frontmatter.get("license")
    if license_value not in (None, "", []):
        cleaned["license"] = license_value
    compatibility = build_compatibility(name, bins, envs)
    if compatibility:
        cleaned["compatibility"] = compatibility
    cleaned["metadata"] = {
        "aisa": compact_none(
            {
                "emoji": emoji,
                "requires": {
                    "bins": bins,
                    "env": envs,
                },
                "primaryEnv": primary_env,
                "compatibility": compatibility,
            }
        )
    }

    new_body = (
        body.replace("${SKILL_ROOT}", "{baseDir}")
        .replace("${LAST30DAYS_PYTHON}", "python3")
        .replace("${baseDir}", "{baseDir}")
        .replace("{baseDir}/", "")
        .replace("{baseDir}", ".")
    )
    new_text = base.dump_skill(cleaned, new_body)
    old_text = skill_path.read_text(encoding="utf-8")
    if new_text == old_text:
        return False
    skill_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    for path in sorted(SOURCE_ROOT.rglob("__pycache__"), reverse=True):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    changed = 0
    total = 0
    for skill_path in sorted(SOURCE_ROOT.glob("*/SKILL.md")):
        total += 1
        if normalize_skill(skill_path.parent):
            changed += 1
    print(f"Normalized {changed} of {total} target skills.")


if __name__ == "__main__":
    main()
