#!/usr/bin/env python3
"""Build native-first ClawHub plugin packages from clawhub-release/ skills."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import build_claude_release as base


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "clawhub-release"
OUTPUT_ROOT = REPO_ROOT / "clawhub-plugin-release"
PLUGIN_ROOT = OUTPUT_ROOT / "plugins"
ZIP_ROOT = OUTPUT_ROOT / "zips"
RUNTIME_IGNORE = shutil.ignore_patterns(
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".pytest_cache",
    "node_modules",
    ".DS_Store",
)


def infer_keywords(name: str, description: str) -> list[str]:
    lower = f"{name} {description}".lower()
    keywords = ["aisa", "clawhub", "openclaw", "native-plugin", "agent-skill"]
    for token in (
        "twitter",
        "x",
        "youtube",
        "search",
        "research",
        "market",
        "stock",
        "prediction",
        "media",
        "image",
        "video",
        "llm",
        "router",
        "provider",
    ):
        if token in lower and token not in keywords:
            keywords.append(token)
    return keywords[:10]


def load_skills() -> list[dict[str, str]]:
    skills: list[dict[str, object]] = []
    for skill_dir in sorted(path for path in SOURCE_ROOT.iterdir() if path.is_dir()):
        frontmatter, _body = base.load_frontmatter(skill_dir / "SKILL.md")
        name = str(frontmatter.get("name") or skill_dir.name).strip()
        description = str(frontmatter.get("description") or f"{name} ClawHub bundle plugin.")
        version = str(frontmatter.get("version") or "1.0.0")
        license_value = str(frontmatter.get("license") or "MIT")
        requires = frontmatter.get("requires") if isinstance(frontmatter.get("requires"), dict) else {}
        metadata = frontmatter.get("metadata") if isinstance(frontmatter.get("metadata"), dict) else {}
        openclaw_meta = metadata.get("openclaw") if isinstance(metadata.get("openclaw"), dict) else {}
        aisa_meta = metadata.get("aisa") if isinstance(metadata.get("aisa"), dict) else {}

        env_vars: list[str] = []
        for source in (
            requires.get("env"),
            openclaw_meta.get("requires", {}).get("env") if isinstance(openclaw_meta.get("requires"), dict) else None,
            aisa_meta.get("requires", {}).get("env") if isinstance(aisa_meta.get("requires"), dict) else None,
        ):
            if isinstance(source, list):
                for env_name in source:
                    if isinstance(env_name, str) and env_name not in env_vars:
                        env_vars.append(env_name)

        primary_env = (
            frontmatter.get("primaryEnv")
            or openclaw_meta.get("primaryEnv")
            or aisa_meta.get("primaryEnv")
            or (env_vars[0] if env_vars else "")
        )
        emoji = str(openclaw_meta.get("emoji") or aisa_meta.get("emoji") or "").strip()
        skills.append(
            {
                "name": name,
                "description": description,
                "version": version,
                "license": license_value,
                "path": skill_dir.name,
                "env_vars": env_vars,
                "primary_env": str(primary_env).strip(),
                "emoji": emoji,
            }
        )
    return skills


def plugin_slug(skill_name: str) -> str:
    return f"{skill_name}-plugin"


def plugin_description(skill: dict[str, str]) -> str:
    return (
        f"Native-first ClawHub plugin for `{skill['name']}`. "
        f"Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. "
        f"{skill['description']}"
    )


def humanize_env_name(env_name: str) -> str:
    return env_name.replace("_", " ").title()


def build_config_schema(skill: dict[str, object]) -> dict[str, object]:
    env_vars = [env_name for env_name in skill.get("env_vars", []) if isinstance(env_name, str)]
    properties: dict[str, object] = {}
    for env_name in env_vars:
        properties[env_name] = {
            "type": "string",
            "title": humanize_env_name(env_name),
            "description": f"Provide {env_name} for the packaged AIsa skill runtime.",
            "format": "password",
        }

    schema: dict[str, object] = {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
    }
    if env_vars:
        schema["required"] = env_vars
    return schema


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def zip_plugin(source_dir: Path, zip_path: Path) -> None:
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED, compresslevel=1) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir))


def build_plugin(skill: dict[str, object]) -> dict[str, str]:
    skill_name = skill["name"]
    slug = plugin_slug(skill_name)
    plugin_dir = PLUGIN_ROOT / slug
    shutil.rmtree(plugin_dir, ignore_errors=True)
    (plugin_dir / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (plugin_dir / "skills").mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        SOURCE_ROOT / skill["path"],
        plugin_dir / "skills" / skill["path"],
        dirs_exist_ok=True,
        ignore=RUNTIME_IGNORE,
    )

    manifest = {
        "name": slug,
        "description": plugin_description(skill),
        "version": skill["version"],
        "author": {"name": "AIsa"},
        "homepage": "https://aisa.one",
        "repository": "https://github.com/AIsa-team/agent-skills",
        "license": skill["license"],
    }
    write_json(plugin_dir / ".claude-plugin" / "plugin.json", manifest)

    openclaw_manifest = {
        "id": slug,
        "name": base.prettify_skill_name(skill_name),
        "description": plugin_description(skill),
        "version": skill["version"],
        "skills": ["./skills"],
        "configSchema": build_config_schema(skill),
    }
    if skill.get("emoji"):
        openclaw_manifest["uiHints"] = {"emoji": skill["emoji"]}
    write_json(plugin_dir / "openclaw.plugin.json", openclaw_manifest)

    index_ts = [
        "const plugin = {",
        f'  id: "{slug}",',
        f'  name: "{base.prettify_skill_name(skill_name)}",',
        "  register() {",
        "    // Native wrapper only. The packaged skill payload is declared in openclaw.plugin.json.",
        "  },",
        "};",
        "",
        "export default plugin;",
    ]
    (plugin_dir / "index.ts").write_text("\n".join(index_ts) + "\n", encoding="utf-8")

    package_json = {
        "name": slug,
        "version": skill["version"],
        "description": plugin_description(skill),
        "license": skill["license"],
        "type": "module",
        "keywords": infer_keywords(skill_name, skill["description"]),
        "homepage": "https://aisa.one",
        "repository": {
            "type": "git",
            "url": "https://github.com/AIsa-team/agent-skills.git",
        },
        "openclaw": {
            "extensions": ["./index.ts"],
            "compat": {
                "pluginApi": "^1.0.0",
            },
            "build": {
                "openclawVersion": "^1.0.0",
            },
        },
    }
    write_json(plugin_dir / "package.json", package_json)

    readme_lines = [
        f"# {base.prettify_skill_name(skill_name)} Plugin",
        "",
        "ClawHub/OpenClaw native-first plugin wrapper for the packaged AIsa skill.",
        "",
        "## What It Ships",
        "",
        f"- Bundle plugin id: `{slug}`",
        f"- Native manifest: `openclaw.plugin.json`",
        f"- Native entrypoint: `index.ts`",
        f"- Embedded skill: `skills/{skill['path']}/SKILL.md`",
        "- Format: native OpenClaw plugin plus Claude-compatible bundle fallback",
        "",
        "## Why This Format",
        "",
        "- Uses the OpenClaw-native manifest path that current plugin docs expect.",
        "- Keeps the packaged skill payload intact under `skills/` for ClawHub/OpenClaw skill loading.",
        "- Retains `.claude-plugin/plugin.json` so Claude-compatible marketplace tooling still recognizes the package.",
        "- Reuses the already-hardened `clawhub-release/` skill payload.",
        "",
        "## Install After Publishing",
        "",
        "```bash",
        f"openclaw plugins install clawhub:{slug}",
        "```",
        "",
        "## Publish Locally",
        "",
        "```bash",
        f"clawhub package publish ./plugins/{slug} --dry-run",
        f"clawhub package publish ./plugins/{slug}",
        "```",
        "",
        "## Notes",
        "",
        f"- Runtime requirements and guardrails remain inside `skills/{skill['path']}/SKILL.md`.",
        "- If both native and bundle markers exist, OpenClaw prefers the native plugin path.",
        "- This package keeps side effects explicit and relies on the packaged skill's repo-local defaults where applicable.",
    ]
    (plugin_dir / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    zip_path = ZIP_ROOT / f"{slug}.zip"
    zip_plugin(plugin_dir, zip_path)
    return {
        "plugin": slug,
        "skill": skill_name,
        "path": str(plugin_dir.relative_to(REPO_ROOT)),
        "zip": str(zip_path.relative_to(REPO_ROOT)),
        "description": package_json["description"],
    }


def write_docs(plugins: list[dict[str, str]]) -> None:
    readme = [
        "# ClawHub Plugin Release",
        "",
        "ClawHub native-first plugin packaging layer generated from `clawhub-release/`.",
        "",
        "## Purpose",
        "",
        "- Wrap every packaged AIsa skill as an installable ClawHub/OpenClaw plugin.",
        "- Prefer the OpenClaw native manifest path while keeping Claude-compatible bundle metadata for cross-marketplace reuse.",
        "- Produce ready-to-publish directories plus root-flat zip artifacts.",
        "",
        "## Layout",
        "",
        "- `plugins/<skill>-plugin/`: publishable plugin directory",
        "- `zips/<skill>-plugin.zip`: root-flat upload/archive artifact",
        "",
        "## Publish Loop",
        "",
        "```bash",
        "for dir in clawhub-plugin-release/plugins/*; do",
        "  [ -d \"$dir\" ] || continue",
        "  clawhub package publish \"$dir\" --dry-run",
        "done",
        "```",
        "",
        "## Generated Plugins",
        "",
    ]
    for plugin in plugins:
        readme.append(f"- `{plugin['plugin']}` → `{plugin['skill']}`")
    (OUTPUT_ROOT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    publishing = [
        "# Publishing ClawHub Bundle Plugins",
        "",
        "1. Build `targetSkills/` and `clawhub-release/` first.",
        "2. Run `python3 scripts/build_clawhub_plugin_release.py`.",
        "3. Dry-run each plugin with `clawhub package publish <dir> --dry-run`.",
        "4. Publish the approved plugin directories with `clawhub package publish <dir>`.",
        "5. Prefer publishing from a Git-backed repo so ClawHub can keep source attribution.",
        "",
        "## Why Native-First Dual Format",
        "",
        "- Current OpenClaw docs treat `openclaw.plugin.json` as the native plugin contract and prefer it over bundle markers.",
        "- Keeping `.claude-plugin/plugin.json` alongside the native manifest preserves Claude-marketplace compatibility without giving up native ClawHub structure.",
        "- The packaged skill still lives under `skills/`, so the runtime surface remains skill-first and conservative.",
    ]
    (OUTPUT_ROOT / "PUBLISHING.md").write_text("\n".join(publishing) + "\n", encoding="utf-8")

    audit = {
        "generated_at": "2026-04-20",
        "source": "clawhub-release",
        "plugins": plugins,
    }
    write_json(OUTPUT_ROOT / "index.json", audit)

    audit_lines = [
        "# ClawHub Plugin Release Audit",
        "",
        f"- Generated plugins: {len(plugins)}",
        "- Packaging mode: native-first dual format (`openclaw.plugin.json` + `index.ts` + `package.json` + optional `.claude-plugin/plugin.json` + embedded `skills/`)",
        "- Zip rule: archives are written root-flat with required files at archive root.",
        "",
    ]
    for plugin in plugins:
        audit_lines.extend(
            [
                f"## {plugin['plugin']}",
                "",
                f"- Skill: `{plugin['skill']}`",
                f"- Directory: `{plugin['path']}`",
                f"- Zip: `{plugin['zip']}`",
                f"- Description: {plugin['description']}",
                "",
            ]
        )
    (OUTPUT_ROOT / "AUDIT.md").write_text("\n".join(audit_lines), encoding="utf-8")

    gitignore = [
        ".DS_Store",
        "__pycache__/",
        "*.pyc",
    ]
    (OUTPUT_ROOT / ".gitignore").write_text("\n".join(gitignore) + "\n", encoding="utf-8")


def main() -> None:
    shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
    PLUGIN_ROOT.mkdir(parents=True, exist_ok=True)
    ZIP_ROOT.mkdir(parents=True, exist_ok=True)

    plugins: list[dict[str, str]] = []
    skills = load_skills()
    total = len(skills)
    for index, skill in enumerate(skills, start=1):
        print(f"[{index}/{total}] building {skill['name']}", flush=True)
        plugins.append(build_plugin(skill))
    write_docs(plugins)
    print(f"Built {len(plugins)} ClawHub native-first plugins into {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
