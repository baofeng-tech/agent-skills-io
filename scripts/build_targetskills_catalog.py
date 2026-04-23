#!/usr/bin/env python3
"""Rebuild the lightweight catalog files that live at targetSkills/ root."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import build_claude_release as base


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_ROOT = REPO_ROOT / "targetSkills"
PUBLIC_REPO = "https://github.com/AIsa-team/agent-skills"
PUBLIC_BRANCH = "agentskills"
PUBLIC_BRANCH_URL = f"{PUBLIC_REPO}/tree/{PUBLIC_BRANCH}"


def generated_at() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def infer_category(name: str, description: str) -> str:
    lower = f"{name} {description}".lower()
    if "twitter" in lower or lower.startswith("x-"):
        return "twitter"
    if "youtube" in lower:
        return "youtube"
    if any(token in lower for token in ("stock", "market", "portfolio", "dividend", "prediction", "finance", "crypto")):
        return "finance"
    if any(token in lower for token in ("search", "research", "tavily", "perplexity", "scholar", "last30days")):
        return "search"
    if any(token in lower for token in ("media", "image", "video")):
        return "media"
    if any(token in lower for token in ("llm", "router", "provider", "model")):
        return "ai"
    return "automation"


def load_skills() -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for skill_dir in sorted(path for path in TARGET_ROOT.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        frontmatter, _body = base.load_frontmatter(skill_file)
        name = str(frontmatter.get("name") or skill_dir.name).strip()
        description = str(frontmatter.get("description") or f"{name} skill").strip()
        skills.append(
            {
                "name": name,
                "path": skill_dir.name,
                "description": description,
                "category": infer_category(name, description),
                "source": f"{PUBLIC_BRANCH_URL}/{skill_dir.name}",
            }
        )
    return skills


def write_index_json(skills: list[dict[str, str]]) -> None:
    payload = {
        "repository": PUBLIC_REPO,
        "branch": PUBLIC_BRANCH,
        "branch_url": PUBLIC_BRANCH_URL,
        "generated_at": generated_at(),
        "skills": [
            {
                "name": skill["name"],
                "category": skill["category"],
                "description": skill["description"],
                "path": skill["path"],
                "source": skill["source"],
                "entry": "SKILL.md",
            }
            for skill in skills
        ],
    }
    (TARGET_ROOT / "index.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_index_markdown(skills: list[dict[str, str]]) -> None:
    lines = [
        "# AIsa Target Skills Catalog",
        "",
        "This catalog lists the current cross-platform mother skills in `targetSkills/`.",
        "",
        f"- Generated at: `{generated_at()}`",
        f"- Repository target: `{PUBLIC_REPO}`",
        f"- Branch target: `{PUBLIC_BRANCH}`",
        f"- Total skills: `{len(skills)}`",
        "",
        "## Skills",
        "",
    ]
    for skill in skills:
        lines.append(f"- `{skill['name']}`")
        lines.append(f"  - Category: `{skill['category']}`")
        lines.append(f"  - Path: `{skill['path']}`")
        lines.append(f"  - Description: {skill['description']}")
    (TARGET_ROOT / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_well_known_index(skills: list[dict[str, str]]) -> None:
    payload = {
        "version": "1.0",
        "generated_at": generated_at(),
        "provider": {
            "name": "AIsa",
            "repository": PUBLIC_REPO,
            "branch": PUBLIC_BRANCH,
            "homepage": PUBLIC_BRANCH_URL,
        },
        "skills": [
            {
                "name": skill["name"],
                "description": skill["description"],
                "location": skill["source"],
            }
            for skill in skills
        ],
    }
    (TARGET_ROOT / "well-known-skills-index.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    skills = load_skills()
    write_index_json(skills)
    write_index_markdown(skills)
    write_well_known_index(skills)
    print(f"Rebuilt targetSkills catalog for {len(skills)} skills.")


if __name__ == "__main__":
    main()
