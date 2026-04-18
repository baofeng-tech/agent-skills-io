#!/usr/bin/env python3
"""Build a Claude Code plugin marketplace wrapper around claude-release/."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import build_claude_release as base


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "claude-release"
OUTPUT_ROOT = REPO_ROOT / "claude-marketplace"


def infer_category(name: str, description: str) -> str:
    lower = f"{name} {description}".lower()
    if "twitter" in lower or lower.startswith("x-"):
        return "communication"
    if "youtube" in lower:
        return "media"
    if any(token in lower for token in ("stock", "market", "portfolio", "dividend", "prediction", "kalshi", "polymarket")):
        return "finance"
    if any(token in lower for token in ("search", "tavily", "perplexity", "scholar", "last30days", "research")):
        return "research"
    if any(token in lower for token in ("media-gen", "image", "video")):
        return "creative"
    if any(token in lower for token in ("llm", "provider", "qwen", "deepseek", "router")):
        return "ai"
    return "automation"


def infer_tags(name: str, description: str) -> list[str]:
    tokens = []
    lower = f"{name} {description}".lower()
    for token in ("twitter", "x", "youtube", "search", "research", "market", "stock", "prediction", "llm", "router", "image", "video"):
        if token in lower:
            tokens.append(token)
    if not tokens:
        tokens.append("automation")
    return tokens[:6]


def load_skills() -> list[dict[str, str]]:
    skills = []
    for skill_dir in sorted(path for path in SOURCE_ROOT.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        frontmatter, _body = base.load_frontmatter(skill_file)
        skills.append(
            {
                "name": frontmatter.get("name", skill_dir.name),
                "description": frontmatter.get("description", f"{skill_dir.name} Claude Code plugin"),
                "path": skill_dir.name,
            }
        )
    return skills


def build_plugin(skill: dict[str, str]) -> dict[str, object]:
    plugin_dir = OUTPUT_ROOT / "plugins" / skill["name"]
    shutil.rmtree(plugin_dir, ignore_errors=True)
    (plugin_dir / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (plugin_dir / "skills").mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        SOURCE_ROOT / skill["path"],
        plugin_dir / "skills" / skill["path"],
        dirs_exist_ok=True,
    )

    plugin_manifest = {
        "name": skill["name"],
        "description": skill["description"],
        "version": "1.0.0",
        "author": {"name": "AIsa"},
        "homepage": "https://aisa.one",
        "repository": "https://github.com/AIsa-team/agent-skills",
        "license": "MIT",
    }
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(plugin_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    readme = [
        f"# {skill['name']}",
        "",
        "Claude Code plugin wrapper for the packaged AIsa skill.",
        "",
        "## Contents",
        "",
        f"- Skill namespace: `/"+ skill["name"] + ":" + skill["path"] + "`",
        f"- Skill source: `skills/{skill['path']}/SKILL.md`",
    ]
    (plugin_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    category = infer_category(skill["name"], skill["description"])
    tags = infer_tags(skill["name"], skill["description"])
    return {
        "name": skill["name"],
        "description": skill["description"],
        "source": f"./plugins/{skill['name']}",
        "category": category,
        "tags": tags,
    }


def main() -> None:
    shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
    (OUTPUT_ROOT / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "plugins").mkdir(parents=True, exist_ok=True)

    skills = load_skills()
    plugins = [build_plugin(skill) for skill in skills]

    marketplace = {
        "name": "aisa-claude-marketplace",
        "metadata": {
            "description": "AIsa Claude Code marketplace for packaged skills derived from targetSkills.",
            "author": {"name": "AIsa"},
        },
        "plugins": plugins,
    }
    (OUTPUT_ROOT / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    readme = [
        "# AIsa Claude Marketplace",
        "",
        "Local Git-based Claude Code marketplace wrapper for the generated AIsa skills.",
        "",
        "## Test Locally",
        "",
        "```bash",
        "claude /plugin marketplace add ./claude-marketplace",
        "claude /plugin install aisa-twitter-command-center@aisa-claude-marketplace",
        "```",
        "",
        "## Notes",
        "",
        "- Plugin entries use relative `./plugins/<name>` sources, which matches Claude Code's Git-based marketplace guidance.",
        "- Each plugin embeds its own `skills/<skill>/` directory so cache installs do not break file resolution.",
    ]
    (OUTPUT_ROOT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    print(f"Built {len(plugins)} Claude marketplace plugins into {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
