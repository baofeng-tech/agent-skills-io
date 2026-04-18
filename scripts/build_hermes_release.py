#!/usr/bin/env python3
"""Build a Hermes-ready release tree from targetSkills/."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import build_claude_release as base


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "targetSkills"
OUTPUT_ROOT = REPO_ROOT / "hermes-release"


def infer_category(name: str, description: str) -> str:
    lower = f"{name} {description}".lower()
    if "twitter" in lower or lower.startswith("x-"):
        return "communication"
    if "youtube" in lower:
        return "research"
    if any(token in lower for token in ("stock", "market", "portfolio", "dividend", "prediction", "kalshi", "polymarket", "finance")):
        return "finance"
    if any(token in lower for token in ("search", "tavily", "perplexity", "scholar", "last30days", "research")):
        return "research"
    if any(token in lower for token in ("media-gen", "image", "video")):
        return "creative"
    if any(token in lower for token in ("llm", "provider", "qwen", "deepseek", "router")):
        return "ai"
    return "automation"


def infer_tags(name: str, description: str, category: str) -> list[str]:
    tags = [category]
    lower = f"{name} {description}".lower()
    for token in ("twitter", "x", "youtube", "search", "research", "market", "stock", "prediction", "llm", "router", "image", "video", "aisa"):
        if token in lower and token not in tags:
            tags.append(token)
    return tags[:8]


def infer_related(name: str) -> list[str]:
    if "twitter" in name or name.startswith("x-"):
        return ["aisa-twitter-command-center", "aisa-twitter-post-engage"]
    if "youtube" in name:
        return ["aisa-youtube-search", "aisa-youtube-serp-scout"]
    if "search" in name or "last30days" in name:
        return ["search", "aisa-multi-search-engine"]
    if "market" in name or "stock" in name or "prediction" in name:
        return ["market", "prediction-market"]
    if "llm" in name or "provider" in name:
        return ["aisa-provider", "llm-router"]
    return []


def needs_aisa_key(skill_dir: Path) -> bool:
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "AISA_API_KEY" in text:
            return True
    return False


def clean_frontmatter(skill_dir: Path, frontmatter: dict[str, Any]) -> dict[str, Any]:
    name = str(frontmatter.get("name") or skill_dir.name).strip()
    description = base.normalize_description(name, str(frontmatter.get("description") or ""))
    category = infer_category(name, description)
    tags = infer_tags(name, description, category)
    related = [item for item in infer_related(name) if item != name]

    cleaned: dict[str, Any] = {
        "name": name,
        "description": description,
    }
    for key in ("version", "author", "license", "homepage", "repository"):
        value = frontmatter.get(key)
        if key == "homepage":
            value = base.normalize_homepage(value)
        if value not in (None, "", []):
            cleaned[key] = value

    cleaned["metadata"] = {
        "hermes": {
            "tags": tags,
        }
    }
    if related:
        cleaned["metadata"]["hermes"]["related_skills"] = related[:4]

    if needs_aisa_key(skill_dir):
        cleaned["required_environment_variables"] = [
            {
                "name": "AISA_API_KEY",
                "prompt": "AIsa API key",
                "help": "Get your key from https://aisa.one or the AIsa marketplace account panel.",
                "required_for": "AIsa-backed API access",
            }
        ]

    return cleaned


def normalize_body(body: str, skill_name: str) -> str:
    body = base.add_release_note(base.rewrite_skill_body(body, skill_name), "hermes")
    body = base.rewrite_user_facing_markdown(body, "hermes", skill_name)
    body = body.replace("## When to use", "## When to Use")
    body = body.replace("## When NOT to use", "## Pitfalls")
    body = body.replace("## Quick Start", "## Quick Reference")
    if "## Verification" not in body:
        body = body.rstrip() + "\n\n## Verification\n\n- Confirm the command returns structured output or a successful API response.\n- If the workflow is stateful, re-run a read/list/status command to verify the new state.\n"
    return body


def build_skill(src_dir: Path) -> dict[str, object]:
    frontmatter, body = base.load_frontmatter(src_dir / "SKILL.md")
    skill_frontmatter = clean_frontmatter(src_dir, frontmatter)
    category = infer_category(skill_frontmatter["name"], skill_frontmatter["description"])
    out_dir = OUTPUT_ROOT / category / src_dir.name

    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    base.copy_tree(src_dir, out_dir)

    audit = base.SkillAudit(
        name=src_dir.name,
        source_path=str(src_dir.relative_to(REPO_ROOT)),
        output_path=str(out_dir.relative_to(REPO_ROOT)),
        description=skill_frontmatter["description"],
    )
    base.prune_release_tree(out_dir, audit)
    base.patch_runtime_files(out_dir, audit)
    base.rewrite_markdown_tree(out_dir, "hermes", audit)

    (out_dir / "SKILL.md").write_text(
        base.dump_skill(skill_frontmatter, normalize_body(body, src_dir.name)),
        encoding="utf-8",
    )
    base.write_skill_readme(out_dir, skill_frontmatter, "hermes")
    audit.changes.append("replaced source README with a Hermes-oriented release README")
    return {
        "name": src_dir.name,
        "category": category,
        "path": str(out_dir.relative_to(REPO_ROOT)),
        "description": skill_frontmatter["description"],
        "residual_risks": audit.residual_risks,
        "changes": audit.changes,
    }


def write_docs(skills: list[dict[str, object]]) -> None:
    counts: dict[str, int] = {}
    for skill in skills:
        counts[skill["category"]] = counts.get(skill["category"], 0) + 1

    readme = [
        "# Hermes Release",
        "",
        "Hermes-oriented packaged copy of all `targetSkills/` mother skills.",
        "",
        "## Structure",
        "",
        "- Skills are organized by Hermes-style categories such as `research/`, `communication/`, and `finance/`.",
        "- Each skill keeps a standard `SKILL.md + scripts + references` layout.",
        "- Frontmatter is normalized for Hermes fields like `metadata.hermes.tags` and `required_environment_variables`.",
        "",
        "## Category Counts",
        "",
    ]
    for category, count in sorted(counts.items()):
        readme.append(f"- `{category}`: {count}")
    readme.extend(
        [
            "",
            "## Publish Paths",
            "",
            "- GitHub repo + `hermes skills install github:owner/repo/path`",
            "- Skills Hub / custom tap packaging",
            "- Well-known index distribution if you later expose the repo via a website",
        ]
    )
    (OUTPUT_ROOT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    audit_lines = [
        "# Hermes Release Audit",
        "",
        f"- Skills converted: {len(skills)}",
        "",
    ]
    for skill in skills:
        audit_lines.append(f"## {skill['name']}")
        audit_lines.append("")
        audit_lines.append(f"- Category: `{skill['category']}`")
        audit_lines.append(f"- Path: `{skill['path']}`")
        audit_lines.append(f"- Description: {skill['description']}")
        for change in skill["changes"]:
            audit_lines.append(f"- Change: {change}")
        for risk in skill["residual_risks"]:
            audit_lines.append(f"- Residual risk: {risk}")
        audit_lines.append("")
    (OUTPUT_ROOT / "AUDIT.md").write_text("\n".join(audit_lines), encoding="utf-8")

    index = {
        "generated_at": "2026-04-17",
        "source": "targetSkills",
        "skills": skills,
    }
    (OUTPUT_ROOT / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    skills = [build_skill(path.parent) for path in sorted(SOURCE_ROOT.glob("*/SKILL.md"))]
    write_docs(skills)
    print(f"Built {len(skills)} Hermes-ready skills into {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
