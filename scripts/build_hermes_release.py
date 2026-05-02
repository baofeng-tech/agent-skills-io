#!/usr/bin/env python3
"""Build a Hermes-ready release tree from targetSkills/."""

from __future__ import annotations

import json
import re
import stat
import shutil
from pathlib import Path
from typing import Any

import build_claude_release as base


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "targetSkills"
OUTPUT_ROOT = REPO_ROOT / "hermes-release"


SAFE_EXECUTABLE_SUFFIXES = {
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".py",
}
NON_RUNTIME_DIRS = {"references"}
HERMES_DATA_DIR = ".hermes-skill-data"
PREFERRED_ENTRYPOINTS = (
    "run-last30days.sh",
    "run-watchlist.sh",
    "run-briefing.sh",
    "search_client.py",
    "market_client.py",
    "youtube_client.py",
    "twitter_client.py",
    "twitter_oauth_client.py",
    "twitter_engagement_client.py",
    "prediction_market_client.py",
    "arbitrage_finder.py",
    "media_gen_client.py",
    "stock_analyst.py",
    "analyze_stock.py",
    "watchlist.py",
    "briefing.py",
    "portfolio.py",
    "dividends.py",
    "hot_scanner.py",
    "rumor_scanner.py",
    "cn_llm_client.py",
    "llm_router_client.py",
    "perplexity_search_client.py",
)
CLIENT_CONSTRUCTOR_RE = re.compile(r"client = ([A-Za-z_]+Client)\(\)")
HERMES_PATCH_FILE_ORDER = {
    "scripts/twitter_oauth_client.py": 10,
    "scripts/twitter_engagement_client.py": 20,
    "scripts/twitter_client.py": 30,
    "scripts/lib/ui.py": 10,
    "scripts/lib/env.py": 20,
    "scripts/prediction_market_client.py": 10,
    "scripts/arbitrage_finder.py": 20,
    "scripts/test_api_data.py": 10,
    "scripts/stock_analyst.py": 20,
}


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
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "AISA_API_KEY" in text:
            return True
    return False


def infer_required_bins(skill_dir: Path) -> list[str]:
    bins: list[str] = []
    suffixes = {path.suffix.lower() for path in skill_dir.rglob("*") if path.is_file()}
    if ".py" in suffixes:
        bins.append("python3")
    if ".sh" in suffixes:
        bins.append("bash")
    if {".js", ".mjs", ".cjs", ".ts"} & suffixes:
        bins.append("node")
    return bins


def infer_runtime_entrypoints(skill_dir: Path) -> list[str]:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return []

    candidates: dict[str, Path] = {}
    for path in sorted(scripts_dir.iterdir()):
        if not path.is_file():
            continue
        if path.name.startswith(("test-", "verify_", "evaluate_", "generate-")):
            continue
        if path.suffix not in {".py", ".sh"}:
            continue
        candidates[path.name] = path

    ordered: list[Path] = []
    for name in PREFERRED_ENTRYPOINTS:
        path = candidates.pop(name, None)
        if path is not None:
            ordered.append(path)
    ordered.extend(candidates[name] for name in sorted(candidates))

    commands: list[str] = []
    for path in ordered[:3]:
        rel = path.relative_to(skill_dir).as_posix()
        if path.suffix == ".sh":
            commands.append(f"bash {rel} --help")
        else:
            commands.append(f"python3 {rel} --help")
    return commands


def build_minimal_body(skill_dir: Path, skill_name: str, description: str) -> str:
    quick_reference = infer_runtime_entrypoints(skill_dir)
    lines = [
        f"# {skill_name}",
        "",
        description,
        "",
        "## When to Use",
        "",
        "- Use this release when the user needs the runtime packaged under `scripts/`.",
        "- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.",
        "- For Hermes community installs, keep setup explicit and review the command help text before the first run.",
        "",
        "## Setup",
        "",
        "- Review `README.md` for the release-specific summary and structure.",
        "- Use repo-relative paths under `scripts/`.",
        "- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.",
    ]
    if quick_reference:
        lines.extend(
            [
                "",
                "## Quick Reference",
                "",
            ]
        )
        for command in quick_reference:
            lines.append(f"- `{command}`")
    lines.extend(
        [
            "",
            "## Verification",
            "",
            "- Confirm the command returns structured output or a successful API response.",
            "- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.",
        ]
    )
    return "\n".join(lines) + "\n"


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

    bins = infer_required_bins(skill_dir)
    cleaned["metadata"] = {
        "aisa": {
            "emoji": "🛠",
            "requires": {
                "bins": bins,
                "env": ["AISA_API_KEY"] if needs_aisa_key(skill_dir) else [],
            },
            "primaryEnv": "AISA_API_KEY" if needs_aisa_key(skill_dir) else None,
            "compatibility": ["openclaw", "claude-code", "hermes"],
        },
        "hermes": {
            "tags": tags,
        },
    }
    if not cleaned["metadata"]["aisa"]["requires"]["env"]:
        cleaned["metadata"]["aisa"]["requires"].pop("env")
        cleaned["metadata"]["aisa"].pop("primaryEnv")
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


def drop_non_runtime_docs(skill_dir: Path, audit: base.SkillAudit) -> None:
    removed = 0
    for name in NON_RUNTIME_DIRS:
        path = skill_dir / name
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
            removed += 1
    if removed:
        audit.changes.append("removed non-runtime documentation directories from the Hermes release bundle")


def insert_before(text: str, needle: str, insert: str) -> str:
    if insert in text or needle not in text:
        return text
    return text.replace(needle, insert + needle, 1)


def patch_hermes_runtime_files(skill_dir: Path, audit: base.SkillAudit) -> None:
    def patch_sort_key(path: Path) -> tuple[int, str]:
        rel = path.relative_to(skill_dir).as_posix()
        return (HERMES_PATCH_FILE_ORDER.get(rel, 999), rel)

    for path in sorted(skill_dir.rglob("*.py"), key=patch_sort_key):
        text = path.read_text(encoding="utf-8")
        updated = text

        replacements = {
            'self.api_key = api_key or os.environ.get("AISA_API_KEY")': 'self.api_key = api_key',
            "self.api_key = api_key or os.environ.get('AISA_API_KEY')": "self.api_key = api_key",
            'args.api_key or os.environ.get("AISA_API_KEY")': "args.api_key",
            "args.api_key or os.environ.get('AISA_API_KEY')": "args.api_key",
            'api_key = explicit or os.environ.get("AISA_API_KEY")': "api_key = explicit",
            "api_key = explicit or os.environ.get('AISA_API_KEY')": "api_key = explicit",
            'api_key = os.environ.get("AISA_API_KEY")': "api_key = args.api_key",
            "api_key = os.environ.get('AISA_API_KEY')": "api_key = args.api_key",
            'base_url = os.environ.get("AISA_BASE_URL", "https://api.aisa.one/v1")': 'base_url = "https://api.aisa.one/v1"',
            'model = os.environ.get("AISA_MODEL", "gpt-4o")': 'model = "gpt-4o"',
            'return os.environ.get(name, default)': "return default",
            'or get_env("AISA_API_KEY")': "",
            "or get_env('AISA_API_KEY')": "",
            'os.environ.get("CLAWDBOT_STATE_DIR", str(Path.cwd() / ".claude-skill-data"))': f'str(Path.cwd() / "{HERMES_DATA_DIR}")',
            'CONFIG_DIR = Path.cwd() / ".claude-skill-data" / "last30days"': f'CONFIG_DIR = Path.cwd() / "{HERMES_DATA_DIR}" / "last30days"',
            "./.claude-skill-data": f"./{HERMES_DATA_DIR}",
            ".claude-skill-data": HERMES_DATA_DIR,
            "AISA_API_KEY is required. Set it via environment variable or pass to constructor.": "AIsa API key is required. Pass it explicitly via --api-key or constructor.",
            "Error: AISA_API_KEY environment variable is not set.": "Error: --api-key is required.",
            "Requires the AISA_API_KEY environment variable.": "Requires an explicit AIsa API key parameter.",
            "uv run ": "python3 ",
        }
        for old, new in replacements.items():
            updated = updated.replace(old, new)

        if "def get_api_key() -> str:" in updated:
            updated = updated.replace(
                'def get_api_key() -> str:\n    key = os.environ.get("AISA_API_KEY", "")\n    if not key:\n        print("Error: --api-key is required.", file=sys.stderr)\n        print("Get your key at https://aisa.one", file=sys.stderr)\n        sys.exit(1)\n    return key\n',
                'def get_api_key(explicit: str) -> str:\n    key = (explicit or "").strip()\n    if not key:\n        print("Error: --api-key is required.", file=sys.stderr)\n        print("Get your key at https://aisa.one", file=sys.stderr)\n        sys.exit(1)\n    return key\n',
            )
            updated = updated.replace("get_api_key()", "get_api_key(args.api_key)")

        updated = CLIENT_CONSTRUCTOR_RE.sub(r"client = \1(api_key=args.api_key)", updated)

        has_api_key_flag = (
            'parser.add_argument("--api-key"' in updated
            or "parser.add_argument('--api-key'" in updated
        )
        if 'args.api_key' in updated and not has_api_key_flag:
            updated = insert_before(
                updated,
                "    subparsers =",
                '    parser.add_argument("--api-key", required=True, help="AIsa API key")\n\n',
            )
            has_api_key_flag = (
                'parser.add_argument("--api-key"' in updated
                or "parser.add_argument('--api-key'" in updated
            )
            if not has_api_key_flag:
                updated = insert_before(
                    updated,
                    "    args = parser.parse_args()",
                    '    parser.add_argument("--api-key", required=True, help="AIsa API key")\n\n',
                )

        updated = updated.replace(
            'parser.add_argument("--aisa-api-key", help="Override AISA_API_KEY")',
            'parser.add_argument("--aisa-api-key", required=True, help="AIsa API key")',
        )
        updated = updated.replace(
            "parser.add_argument('--aisa-api-key', help='Override AISA_API_KEY')",
            "parser.add_argument('--aisa-api-key', required=True, help='AIsa API key')",
        )

        if updated != text:
            path.write_text(updated, encoding="utf-8")
            audit.changes.append(f"patched Hermes runtime auth and storage defaults in {path.relative_to(skill_dir)}")


def normalize_permissions(skill_dir: Path) -> None:
    """Strip executable bits from non-runtime documentation and data files."""
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in SAFE_EXECUTABLE_SUFFIXES:
            continue
        mode = path.stat().st_mode
        normalized_mode = mode & ~(
            stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )
        if normalized_mode != mode:
            path.chmod(normalized_mode)


def build_skill(src_dir: Path) -> dict[str, object]:
    frontmatter, _body = base.load_frontmatter(src_dir / "SKILL.md")
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
    drop_non_runtime_docs(out_dir, audit)
    patch_hermes_runtime_files(out_dir, audit)
    normalize_permissions(out_dir)

    (out_dir / "SKILL.md").write_text(
        base.dump_skill(
            skill_frontmatter,
            build_minimal_body(out_dir, src_dir.name, skill_frontmatter["description"]),
        ),
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
        "- Each skill keeps a runtime-focused `SKILL.md + scripts/` layout, with non-runtime reference docs stripped from this release layer.",
        "- Frontmatter is normalized for `metadata.aisa`, `metadata.hermes.tags`, and `required_environment_variables`.",
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
