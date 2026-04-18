#!/usr/bin/env python3
"""Build a Claude-market-ready release layer from targetSkills/.

This script keeps the cross-platform mother skills untouched and emits a
cleaner release tree that is easier to publish to a public GitHub repo for
Claude Code / skills.sh distribution.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "targetSkills"
OUTPUT_ROOT = REPO_ROOT / "claude-release"
INDEX_PATH = SOURCE_ROOT / "index.json"

KEEP_TOP_LEVEL_FILES = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "LICENSE.txt",
    "LICENSE.md",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "index.ts",
}
KEEP_DIRS = {"scripts", "references", "assets"}
REMOVE_DIR_NAMES = {"__pycache__", ".pytest_cache", "node_modules", ".DS_Store"}
REMOVE_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp", ".sqlite", ".db"}
REMOVE_FILE_NAMES = {
    "TEST_REPORT.md",
    "_meta.json",
}
REMOVE_SCRIPT_PATTERNS = (
    re.compile(r"^compare\.sh$"),
    re.compile(r"^sync\.sh$"),
    re.compile(r"^test-.*\.sh$"),
    re.compile(r"^run-tests\.sh$"),
)


@dataclass
class SkillAudit:
    name: str
    source_path: str
    output_path: str
    description: str
    changes: list[str] = field(default_factory=list)
    residual_risks: list[str] = field(default_factory=list)


def load_frontmatter(skill_path: Path) -> tuple[dict[str, Any], str]:
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    _, raw_yaml, body = parts
    try:
        data = yaml.safe_load(raw_yaml) or {}
        if not isinstance(data, dict):
            data = {}
    except yaml.YAMLError:
        data = parse_loose_frontmatter(raw_yaml)
    return data, body.lstrip("\n")


def parse_loose_frontmatter(raw_yaml: str) -> dict[str, Any]:
    """Best-effort parser for historical SKILL.md frontmatter.

    Some imported skills use colon-heavy description values without quoting them,
    which breaks strict YAML parsing. For release generation we only need a small
    set of top-level fields, so a conservative line parser is sufficient.
    """

    allowed = {
        "name",
        "description",
        "version",
        "license",
        "homepage",
        "repository",
        "author",
        "argument-hint",
        "allowed-tools",
        "user-invocable",
        "when_to_use",
    }
    parsed: dict[str, Any] = {}
    for line in raw_yaml.splitlines():
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in allowed:
            continue
        value = value.strip().strip('"').strip("'")
        if key == "user-invocable":
            parsed[key] = value.lower() == "true"
        elif value:
            parsed[key] = value
    return parsed


def dump_skill(frontmatter: dict[str, Any], body: str) -> str:
    raw_yaml = yaml.safe_dump(
        frontmatter,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    ).strip()
    return f"---\n{raw_yaml}\n---\n\n{body.rstrip()}\n"


def normalize_description(name: str, description: str) -> str:
    cleaned = " ".join((description or "").split())
    if not cleaned:
        cleaned = f"{name} Claude Code skill."

    if not re.search(r"\bUse when\b:?", cleaned, flags=re.IGNORECASE) and "触发条件：" not in cleaned:
        suffix = infer_use_when(name, cleaned)
        cleaned = f"{cleaned.rstrip('.')}." if not cleaned.endswith((".", "。")) else cleaned
        cleaned = f"{cleaned} Use when: {suffix}."
    return cleaned


def infer_use_when(name: str, description: str) -> str:
    lower = f"{name} {description}".lower()
    if "twitter" in lower or lower.startswith("x-"):
        return "the user needs X/Twitter research, monitoring, posting, or engagement workflows"
    if "youtube" in lower:
        return "the user needs YouTube search, trend discovery, channel research, or SERP analysis"
    if "search" in lower or "tavily" in lower or "scholar" in lower or "perplexity" in lower:
        return "the user needs web search, research, source discovery, or content extraction"
    if "stock" in lower or "market" in lower or "portfolio" in lower or "dividend" in lower:
        return "the user needs market data, stock analysis, watchlists, or portfolio workflows"
    if "prediction" in lower or "polymarket" in lower or "kalshi" in lower:
        return "the user needs prediction market quotes, scanning, or arbitrage analysis"
    if "llm" in lower or "provider" in lower:
        return "the user needs model routing, provider setup, or Chinese LLM access guidance"
    if "media" in lower or "image" in lower or "video" in lower:
        return "the user needs AI image or video generation workflows"
    if "last30days" in lower:
        return "the user needs recent multi-source research across the last 30 days"
    return "the user needs this workflow's domain-specific automation or guidance"


def extract_when_to_use(description: str) -> str | None:
    match = re.search(r"Use when:?\s*(.+)$", description, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip().rstrip(".")
    if "触发条件：" in description:
        return description.split("触发条件：", 1)[1].strip().rstrip("。")
    return None


def infer_allowed_tools(skill_dir: Path, frontmatter: dict[str, Any]) -> str | None:
    existing = frontmatter.get("allowed-tools")
    if existing:
        return existing

    tools: list[str] = ["Read"]
    if (skill_dir / "scripts").exists():
        tools.extend(["Bash", "Grep"])
    return " ".join(dict.fromkeys(tools))


def normalize_homepage(homepage: Any) -> str | None:
    if homepage in (None, "", []):
        return None
    value = str(homepage).strip()
    if not value:
        return None
    if "openclaw.ai" in value:
        return "https://aisa.one"
    return value


def prettify_skill_name(name: str) -> str:
    words = name.replace("_", "-").split("-")
    titled = []
    for word in words:
        lower = word.lower()
        if lower == "aisa":
            titled.append("AIsa")
        elif lower in {"llm", "api"}:
            titled.append(lower.upper())
        elif lower in {"x"}:
            titled.append("X")
        elif word:
            titled.append(word.capitalize())
    return " ".join(titled) if titled else name


def build_release_note(platform: str) -> str:
    if platform == "claude":
        runtime = "Claude Code"
    elif platform == "hermes":
        runtime = "Hermes"
    else:
        runtime = "this runtime"
    return (
        f"> Release note: This package is published for {runtime}. "
        "References to OpenClaw below describe the original source workflow, "
        "a companion runtime, or compatibility guidance unless the skill is explicitly about OpenClaw itself."
    )


def rewrite_user_facing_markdown(text: str, platform: str, skill_name: str) -> str:
    rewritten = text

    replacements = {
        "# OpenClaw Twitter OAuth": "# Twitter OAuth",
        "# OpenClaw Twitter Engagement": "# Twitter Engagement",
        "### OpenClaw Attachment Flow": "### Attachment Flow",
        "Reuse OpenClaw context instead of local file-based conversation persistence.": "Reuse the current conversation context instead of local file-based conversation persistence.",
        "keep the returned `tweets[]` structure in OpenClaw context.": "keep the returned `tweets[]` structure in the current conversation context.",
        "rely on OpenClaw context only.": "rely on the current conversation context only.",
        'python3 scripts/twitter_oauth_client.py post --text "Hello from OpenClaw"': 'python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa"',
        "preferred path for OpenClaw.": "preferred path for this release.",
        "When the user drops image or video files into OpenClaw:": "When the user provides image or video files in the current workspace:",
        "When the user drops image/video files into OpenClaw:": "When the user provides image/video files in the current workspace:",
        "OpenClaw stores the attachment in the local workspace and provides the workspace file path to the skill.": "The runtime stores the attachment in the local workspace and provides the workspace file path to the skill.",
        "OpenClaw auto-detects `AISA_API_KEY` and registers AIsa as a provider. No config file changes needed.": "If your runtime supports provider auto-discovery, `AISA_API_KEY` may be enough. Otherwise use the explicit config examples below.",
        "Or configure in OpenClaw plugin settings:": "If your runtime supports plugin-level configuration, you can also provide the key there:",
        "Multi-source search engine plugin for [OpenClaw](https://docs.openclaw.ai), powered by [AIsa API](https://aisa.one).": "Multi-source search skill package powered by [AIsa API](https://aisa.one), adapted for this release layer.",
        "## Install": "## Setup",
    }
    for old, new in replacements.items():
        rewritten = rewritten.replace(old, new)

    rewritten = re.sub(r"(?m)^# OpenClaw ([^\n]+)$", r"# \1", rewritten)
    rewritten = re.sub(r"(?m)^## OpenClaw ([^\n]+)$", r"## \1", rewritten)

    if skill_name == "aisa-provider":
        note = build_release_note(platform)
        if note not in rewritten:
            title_match = re.match(r"(?s)(# .+?\n\n)", rewritten)
            if title_match:
                rewritten = rewritten.replace(title_match.group(1), title_match.group(1) + note + "\n\n", 1)
            else:
                rewritten = note + "\n\n" + rewritten

    return rewritten


def write_skill_readme(skill_dir: Path, frontmatter: dict[str, Any], platform: str) -> None:
    runtime = "Claude Code" if platform == "claude" else "Hermes"
    name = str(frontmatter.get("name") or skill_dir.name)
    description = str(frontmatter.get("description") or f"{name} skill package.")
    title = prettify_skill_name(name)
    lines = [
        f"# {title}",
        "",
        f"Release-ready {runtime} skill package generated from `targetSkills/{skill_dir.name}`.",
        "",
        f"- Skill name: `{name}`",
        f"- Entry point: `SKILL.md`",
        f"- Runtime assets: `scripts/`, `references/`, `assets/` when present",
        "",
        "## Notes",
        "",
        f"- {description}",
        "- This README is release-specific and replaces source READMEs that were written for other runtimes.",
        "- If the underlying instructions mention OpenClaw, treat that as source-context or compatibility guidance unless the skill is specifically about OpenClaw setup.",
        "",
        "## Quick Start",
        "",
        "1. Open `SKILL.md` to review invocation guidance and runtime requirements.",
        "2. Set any required environment variables before running bundled scripts.",
        "3. Use repo-relative paths like `python3 scripts/...` when following command examples.",
    ]
    (skill_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rewrite_markdown_tree(skill_dir: Path, platform: str, audit: SkillAudit) -> None:
    updated = 0
    for path in skill_dir.rglob("*.md"):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        new_text = rewrite_user_facing_markdown(text, platform, skill_dir.name)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
    if updated:
        audit.changes.append(f"rewrote {updated} markdown file(s) to reduce OpenClaw-specific release wording")


def clean_frontmatter(skill_dir: Path, frontmatter: dict[str, Any]) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}

    name = str(frontmatter.get("name") or skill_dir.name).strip()
    description = normalize_description(name, str(frontmatter.get("description") or ""))

    cleaned["name"] = name
    cleaned["description"] = description

    for key in ("version", "license", "repository", "author", "argument-hint"):
        value = frontmatter.get(key)
        if value not in (None, "", []):
            cleaned[key] = value
    homepage = normalize_homepage(frontmatter.get("homepage"))
    if homepage:
        cleaned["homepage"] = homepage

    allowed_tools = infer_allowed_tools(skill_dir, frontmatter)
    if allowed_tools:
        cleaned["allowed-tools"] = allowed_tools

    if frontmatter.get("user-invocable") is True:
        cleaned["user-invocable"] = True

    when_to_use = frontmatter.get("when_to_use") or extract_when_to_use(description)
    if when_to_use:
        cleaned["when_to_use"] = when_to_use

    return cleaned


def add_release_note(body: str, platform: str) -> str:
    note = build_release_note(platform)
    if "OpenClaw" not in body or note in body:
        return body
    return note + "\n\n" + body.lstrip()


def rewrite_skill_body(body: str, skill_name: str) -> str:
    body = re.sub(
        rf'"?\$\{{CLAUDE_PLUGIN_ROOT\}}/skills/{re.escape(skill_name)}/scripts/([^"\s`]+)"?',
        r"scripts/\1",
        body,
    )
    body = re.sub(
        rf'"?\$\{{CLAUDE_PLUGIN_ROOT\}}/skills/{re.escape(skill_name)}/([^"\s`]+)"?',
        r"\1",
        body,
    )
    body = body.replace("${CLAUDE_PLUGIN_ROOT}/skills/", "")
    body = body.replace("${CLAUDE_PLUGIN_ROOT}/", "")
    body = body.replace("{baseDir}/", "")
    body = body.replace("${CLAUDE_PLUGIN_DATA}", "./.claude-skill-data")
    body = body.replace("the plugin's `userConfig` values", "environment variables")
    body = body.replace("plugin's `userConfig`", "environment variables")
    body = body.replace("When installed as a Claude plugin, the key is configured via the plugin's `userConfig`.", "Set `AISA_API_KEY` in the environment before running the script.")
    body = body.replace("When installed as a Claude plugin, the key is configured via the plugin's `userConfig`", "Set `AISA_API_KEY` in the environment before running the script")
    body = body.replace("Or use the plugin's `userConfig` values (set automatically when the plugin is enabled).", "Environment variables are the supported setup path for this release.")
    body = body.replace("Portfolio data is stored in `${CLAUDE_PLUGIN_DATA}/portfolios.json` for persistence across sessions.", "Portfolio data is stored under `./.claude-skill-data/stock-analysis/portfolios.json` by default.")
    body = body.replace("Watchlist data is stored in `${CLAUDE_PLUGIN_DATA}/watchlist.json` for persistence across sessions.", "Watchlist data is stored under `./.claude-skill-data/stock-analysis/watchlist.json` by default.")

    # Normalize command examples to repo-relative execution where possible.
    body = re.sub(r'python3\s+"?scripts/', "python3 scripts/", body)
    body = body.replace('scripts/', 'scripts/')
    body = re.sub(r'python3\s+\./scripts/', "python3 scripts/", body)
    return body


def should_skip(path: Path) -> bool:
    if path.name in REMOVE_DIR_NAMES or path.name in REMOVE_FILE_NAMES:
        return True
    if path.suffix in REMOVE_SUFFIXES:
        return True
    if path.parent.name == "scripts":
        return any(pattern.match(path.name) for pattern in REMOVE_SCRIPT_PATTERNS)
    return False


def copy_tree(src: Path, dst: Path) -> list[str]:
    kept: list[str] = []
    for item in src.iterdir():
        if item.is_dir():
            if item.name not in KEEP_DIRS or should_skip(item):
                continue
            shutil.copytree(
                item,
                dst / item.name,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    "__pycache__",
                    "*.pyc",
                    "*.pyo",
                    ".pytest_cache",
                    "node_modules",
                ),
            )
            kept.append(item.name)
            continue

        if item.name in KEEP_TOP_LEVEL_FILES and not should_skip(item):
            shutil.copy2(item, dst / item.name)
            kept.append(item.name)
    return kept


def prune_release_tree(skill_dir: Path, audit: SkillAudit) -> None:
    removed = 0
    for path in sorted(skill_dir.rglob("*"), reverse=True):
        if path.is_dir() and path.name in REMOVE_DIR_NAMES:
            shutil.rmtree(path, ignore_errors=True)
            removed += 1
            continue
        if not path.is_file():
            continue
        if should_skip(path):
            path.unlink()
            removed += 1
    if removed:
        audit.changes.append(f"removed {removed} non-runtime generated/test files from the release bundle")


def patch_runtime_files(skill_dir: Path, audit: SkillAudit) -> None:
    for oauth_path in skill_dir.rglob("twitter_oauth_client.py"):
        text = oauth_path.read_text(encoding="utf-8")
        old = "    if output[\"ok\"] and args.open_browser:\n        webbrowser.open(auth_url)\n"
        new = (
            "    if output[\"ok\"] and args.open_browser:\n"
            "        print(\"Browser auto-open is disabled in the Claude release. Open authorization_url manually.\")\n"
        )
        if old in text:
            oauth_path.write_text(text.replace(old, new), encoding="utf-8")
            audit.changes.append(f"disabled browser auto-open in {oauth_path.relative_to(skill_dir)}")

    path_rewrites = {
        "scripts/watchlist.py": (
            'os.environ.get("CLAWDBOT_STATE_DIR", os.path.expanduser("~/.clawdbot"))',
            'os.environ.get("CLAWDBOT_STATE_DIR", str(Path.cwd() / ".claude-skill-data"))',
        ),
        "scripts/portfolio.py": (
            'os.environ.get("CLAWDBOT_STATE_DIR", os.path.expanduser("~/.clawdbot"))',
            'os.environ.get("CLAWDBOT_STATE_DIR", str(Path.cwd() / ".claude-skill-data"))',
        ),
        "scripts/lib/env.py": (
            'CONFIG_DIR = Path.home() / ".config" / "last30days"',
            'CONFIG_DIR = Path.cwd() / ".claude-skill-data" / "last30days"',
        ),
    }

    for relative_path, (old, new) in path_rewrites.items():
        file_path = skill_dir / relative_path
        if not file_path.exists():
            continue
        text = file_path.read_text(encoding="utf-8")
        if old in text:
            file_path.write_text(text.replace(old, new), encoding="utf-8")
            audit.changes.append(f"switched default local storage to repo-local path in {relative_path}")

    for ui_path in skill_dir.rglob("ui.py"):
        text = ui_path.read_text(encoding="utf-8")
        updated = text.replace("~/.config/last30days/.env", "./.claude-skill-data/last30days/.env")
        if updated != text:
            ui_path.write_text(updated, encoding="utf-8")
            audit.changes.append(f"updated config path messaging in {ui_path.relative_to(skill_dir)}")


def build_skill(src_dir: Path, out_dir: Path) -> SkillAudit:
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    kept = copy_tree(src_dir, out_dir)
    frontmatter, body = load_frontmatter(src_dir / "SKILL.md")
    cleaned_frontmatter = clean_frontmatter(src_dir, frontmatter)
    cleaned_body = add_release_note(rewrite_user_facing_markdown(rewrite_skill_body(body, src_dir.name), "claude", src_dir.name), "claude")
    (out_dir / "SKILL.md").write_text(
        dump_skill(cleaned_frontmatter, cleaned_body),
        encoding="utf-8",
    )

    description = cleaned_frontmatter["description"]
    audit = SkillAudit(
        name=src_dir.name,
        source_path=str(src_dir.relative_to(REPO_ROOT)),
        output_path=str(out_dir.relative_to(REPO_ROOT)),
        description=description,
    )

    prune_release_tree(out_dir, audit)
    audit.changes.append("rewrote SKILL.md frontmatter for Claude-friendly search and invocation")
    if "metadata" in frontmatter or "compatibility" in frontmatter:
        audit.changes.append("stripped platform-specific metadata from release frontmatter")
    if "allowed-tools" not in frontmatter and cleaned_frontmatter.get("allowed-tools"):
        audit.changes.append("inferred allowed-tools for Claude Code compatibility")
    if "Use when:" in description or "触发条件：" in description:
        audit.changes.append("ensured description carries explicit trigger phrasing for search and selection")

    patch_runtime_files(out_dir, audit)
    rewrite_markdown_tree(out_dir, "claude", audit)
    write_skill_readme(out_dir, cleaned_frontmatter, "claude")
    audit.changes.append("replaced source README with a Claude-oriented release README")

    if any(name in kept for name in ("scripts", "references")):
        audit.changes.append("copied runtime scripts/references only")

    lower = src_dir.name.lower()
    if "last30days" in lower:
        audit.residual_risks.append("Large runtime surface remains; verify Python 3.12+ and AISA-only flow before public publishing.")
    if "stock-portfolio" in lower or "stock-watchlist" in lower:
        audit.residual_risks.append("Local persistence is still present, but defaults are repo-local instead of home-directory paths.")
    if "twitter" in lower or lower.startswith("x-"):
        audit.residual_risks.append("OAuth flow still requires the user to open the returned authorization URL manually.")

    return audit


def write_root_readme(audits: list[SkillAudit]) -> None:
    lines = [
        "# Claude Release",
        "",
        "This directory is a GitHub-ready Claude / skills.sh release layer generated from `targetSkills/`.",
        "",
        "## Purpose",
        "",
        "- Keep `targetSkills/` as the cross-platform mother-skill layer.",
        "- Publish a cleaner Claude-oriented layer without OpenClaw-heavy frontmatter noise.",
        "- Reduce obvious upload and trust-review risks by removing non-runtime files and home-directory defaults where practical.",
        "",
        "## What Was Changed",
        "",
        "- `SKILL.md` frontmatter was normalized to Claude-friendly fields such as `name`, `description`, `allowed-tools`, and optional `when_to_use`.",
        "- Descriptions were normalized to include explicit trigger phrasing (`Use when:` / `触发条件：`) for better discoverability.",
        "- Non-runtime files such as `__pycache__`, `*.pyc`, compare scripts, sync scripts, and test helpers were removed from release bundles.",
        "- High-risk defaults were reduced for OAuth auto-open and home-directory persistence.",
        "",
        "## Publishing To ClaudeMarketplaces",
        "",
        "`claudemarketplaces.com` currently behaves like an index, not a manual upload console:",
        "",
        "1. Publish this directory as a public GitHub repository.",
        "2. Keep the skill directories at the repo root so each skill has `<skill>/SKILL.md`.",
        "3. Seed installs through `skills.sh` or direct GitHub sharing so the repo becomes discoverable in the wider skills ecosystem.",
        "4. Optionally create a separate Claude plugin marketplace repo later if you want `/plugin marketplace add owner/repo` distribution.",
        "",
        "## Skill Count",
        "",
        f"- Generated skills: {len(audits)}",
        "",
        "## Validation",
        "",
        "- Review `AUDIT.md` before publishing.",
        "- Spot-check the highest-risk bundles first: Twitter, `last30days`, `stock-portfolio`, and `stock-watchlist`.",
    ]
    (OUTPUT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_publish_docs(audits: list[SkillAudit]) -> None:
    publishing = [
        "# Publishing Claude Release",
        "",
        "This directory is intended to be pushed as the root of a public GitHub repository for Claude Code / skills.sh distribution.",
        "",
        "## Recommended Flow",
        "",
        "1. Create a new public GitHub repository.",
        "2. Copy the contents of this directory to the repository root.",
        "3. Commit all files except local test artifacts.",
        "4. Push to GitHub and seed at least one install path through `skills.sh` or direct GitHub sharing.",
        "5. Optionally build a plugin marketplace wrapper from this directory for `/plugin marketplace add` users.",
        "",
        "## Recommended Repo Contents",
        "",
        "- One skill directory per root folder",
        "- `README.md`",
        "- `AUDIT.md`",
        "- `index.json`",
        "- `.gitignore`",
        "",
        f"## Generated Skill Count\n\n- {len(audits)}",
    ]
    (OUTPUT_ROOT / "PUBLISHING.md").write_text("\n".join(publishing) + "\n", encoding="utf-8")

    commit_notes = [
        "# Commit Notes",
        "",
        "Suggested initial commit message:",
        "",
        "`feat: publish AIsa Claude-ready skill catalog`",
        "",
        "Suggested follow-up commit message after smoke-test fixes:",
        "",
        "`chore: tighten Claude skill packaging and runtime defaults`",
        "",
        "Suggested repository description:",
        "",
        "`Claude Code and skills.sh-ready AIsa skill catalog with conservative runtime packaging.`",
    ]
    (OUTPUT_ROOT / "COMMIT_NOTES.md").write_text("\n".join(commit_notes) + "\n", encoding="utf-8")

    gitignore = [
        ".DS_Store",
        "__pycache__/",
        "*.pyc",
        ".pytest_cache/",
        ".claude-skill-data/",
        "*.log",
    ]
    (OUTPUT_ROOT / ".gitignore").write_text("\n".join(gitignore) + "\n", encoding="utf-8")


def write_index(audits: list[SkillAudit]) -> None:
    data = {
        "generated_at": "2026-04-17",
        "source": "targetSkills",
        "skills": [
            {
                "name": audit.name,
                "path": audit.output_path.replace("claude-release/", "", 1),
                "description": audit.description,
                "residual_risks": audit.residual_risks,
            }
            for audit in audits
        ],
    }
    (OUTPUT_ROOT / "index.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_audit(audits: list[SkillAudit]) -> None:
    lines = [
        "# Claude Release Audit",
        "",
        "This report summarizes structural cleanup and residual publishing risk for the generated Claude release layer.",
        "",
        "## Summary",
        "",
        f"- Skills converted: {len(audits)}",
        f"- Skills with residual risk notes: {sum(1 for audit in audits if audit.residual_risks)}",
        "",
        "## Per Skill",
        "",
    ]
    for audit in audits:
        lines.append(f"### {audit.name}")
        lines.append("")
        lines.append(f"- Source: `{audit.source_path}`")
        lines.append(f"- Output: `{audit.output_path}`")
        lines.append(f"- Description: {audit.description}")
        for change in audit.changes:
            lines.append(f"- Change: {change}")
        for risk in audit.residual_risks:
            lines.append(f"- Residual risk: {risk}")
        lines.append("")
    (OUTPUT_ROOT / "AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def load_skill_dirs() -> list[Path]:
    return sorted(
        path.parent
        for path in SOURCE_ROOT.glob("*/SKILL.md")
        if path.parent.is_dir()
    )


def main() -> None:
    source_dirs = load_skill_dirs()
    shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    audits = []
    for src_dir in source_dirs:
        audits.append(build_skill(src_dir, OUTPUT_ROOT / src_dir.name))

    write_root_readme(audits)
    write_publish_docs(audits)
    write_index(audits)
    write_audit(audits)

    print(f"Built {len(audits)} Claude-ready skills into {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
