#!/usr/bin/env python3
"""Build native-first ClawHub plugin packages from clawhub-release/ skills."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import build_claude_release as base


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "clawhub-release"
OUTPUT_ROOT = REPO_ROOT / "clawhub-plugin-release"
PLUGIN_ROOT = OUTPUT_ROOT / "plugins"
ZIP_ROOT = OUTPUT_ROOT / "zips"
SOURCE_REPO = "https://github.com/baofeng-tech/agent-skills-io"
RUNTIME_IGNORE = shutil.ignore_patterns(
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".pytest_cache",
    "node_modules",
    ".DS_Store",
)
OPTIONAL_ENV_ALLOWLIST = {
    "AISA_BASE_URL",
    "AISA_MODEL",
    "LAST30DAYS_FUN_MODEL",
    "LAST30DAYS_PLANNER_MODEL",
    "LAST30DAYS_RERANK_MODEL",
    "TWITTER_RELAY_BASE_URL",
    "TWITTER_RELAY_TIMEOUT",
    "XIAOHONGSHU_API_BASE",
}
OPTIONAL_ENV_IGNORE = {
    "AISA_API_KEY",
    "CLAUDE_PLUGIN_ROOT",
}


def infer_keywords(name: str, description: str) -> list[str]:
    lower = f"{name} {description}".lower()
    keywords = ["aisa", "clawhub", "openclaw", "native-plugin", "agent-skill"]
    for token in (
        "twitter",
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


def load_skills() -> list[dict[str, object]]:
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

        required_bins = merge_env_lists(
            requires.get("bins"),
            openclaw_meta.get("requires", {}).get("bins") if isinstance(openclaw_meta.get("requires"), dict) else None,
            aisa_meta.get("requires", {}).get("bins") if isinstance(aisa_meta.get("requires"), dict) else None,
        )
        env_vars = merge_env_lists(
            requires.get("env"),
            openclaw_meta.get("requires", {}).get("env") if isinstance(openclaw_meta.get("requires"), dict) else None,
            aisa_meta.get("requires", {}).get("env") if isinstance(aisa_meta.get("requires"), dict) else None,
        )
        optional_env_vars = infer_optional_env_vars(skill_dir, metadata)

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
                "required_bins": required_bins,
                "env_vars": env_vars,
                "optional_env_vars": optional_env_vars,
                "primary_env": str(primary_env).strip(),
                "emoji": emoji,
            }
        )
    return skills


def plugin_slug(skill_name: str) -> str:
    return f"{skill_name}-plugin"


def plugin_description(skill: dict[str, object]) -> str:
    lead_parts: list[str] = []
    required_bins = [value for value in skill.get("required_bins", []) if isinstance(value, str)]
    env_vars = [value for value in skill.get("env_vars", []) if isinstance(value, str)]
    requirement_tokens = required_bins + env_vars
    network_target = relay_default_url(skill) or ("https://api.aisa.one" if "AISA_API_KEY" in env_vars else "")
    if requirement_tokens:
        if len(requirement_tokens) == 1:
            lead_parts.append(f"Requires {requirement_tokens[0]}.")
        else:
            lead_parts.append(f"Requires {', '.join(requirement_tokens[:-1])}, and {requirement_tokens[-1]}.")
    if env_vars and network_target:
        lead_parts.append(f"Uses the supplied {env_vars[0]} to send requests to {network_target}.")
    lead = f"{' '.join(lead_parts)} " if lead_parts else ""
    return (
        f"{lead}Native-first ClawHub plugin for `{skill['name']}`. "
        f"Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. "
        f"{skill['description']}"
    )


def humanize_env_name(env_name: str) -> str:
    return env_name.replace("_", " ").title()


def merge_env_lists(*sources: object) -> list[str]:
    merged: list[str] = []
    for source in sources:
        if not isinstance(source, list):
            continue
        for env_name in source:
            if isinstance(env_name, str) and env_name not in merged:
                merged.append(env_name)
    return merged


def build_runtime_requirements(skill: dict[str, object]) -> dict[str, object]:
    requirements: dict[str, object] = {}
    required_bins = [value for value in skill.get("required_bins", []) if isinstance(value, str)]
    env_vars = [value for value in skill.get("env_vars", []) if isinstance(value, str)]
    optional_env_vars = [value for value in skill.get("optional_env_vars", []) if isinstance(value, str)]
    primary_env = str(skill.get("primary_env") or "").strip()
    network_target = relay_default_url(skill) or ("https://api.aisa.one" if "AISA_API_KEY" in env_vars else "")

    if required_bins:
        requirements["bins"] = required_bins
    if env_vars:
        requirements["env"] = env_vars
    if optional_env_vars:
        requirements["optionalEnv"] = optional_env_vars
    if primary_env:
        requirements["primaryEnv"] = primary_env
    if network_target:
        requirements["networkTargets"] = [network_target]
    return requirements


def build_runtime_metadata(skill: dict[str, object]) -> dict[str, object]:
    runtime = build_runtime_requirements(skill)
    metadata_entry: dict[str, object] = {}
    requires: dict[str, object] = {}
    if runtime.get("bins"):
        requires["bins"] = runtime["bins"]
    if runtime.get("env"):
        requires["env"] = runtime["env"]
    if requires:
        metadata_entry["requires"] = requires
    if runtime.get("optionalEnv"):
        metadata_entry["optionalEnv"] = runtime["optionalEnv"]
    if runtime.get("primaryEnv"):
        metadata_entry["primaryEnv"] = runtime["primaryEnv"]
    if runtime.get("networkTargets"):
        metadata_entry["networkTargets"] = runtime["networkTargets"]
    return {"aisa": metadata_entry}


def infer_optional_env_vars(skill_dir: Path, metadata: dict[str, object]) -> list[str]:
    merged: list[str] = []
    for scope in ("aisa", "openclaw"):
        scoped = metadata.get(scope) if isinstance(metadata.get(scope), dict) else {}
        optional_envs = scoped.get("optionalEnv") if isinstance(scoped, dict) else None
        if isinstance(optional_envs, list):
            for env_name in optional_envs:
                if isinstance(env_name, str) and env_name not in merged:
                    merged.append(env_name)
    if merged:
        return merged

    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for env_name in re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text):
            if env_name in OPTIONAL_ENV_IGNORE or env_name not in OPTIONAL_ENV_ALLOWLIST:
                continue
            if env_name not in merged:
                merged.append(env_name)
    return merged


def relay_default_url(skill: dict[str, object]) -> str | None:
    lower = f"{skill.get('name', '')} {skill.get('path', '')}".lower()
    if "twitter" in lower or lower.startswith("x-"):
        return "https://api.aisa.one/apis/v1/twitter"
    return None


def build_config_property(env_name: str) -> dict[str, object]:
    if env_name == "AISA_API_KEY":
        return {
            "type": "string",
            "title": humanize_env_name(env_name),
            "description": f"Provide {env_name} for the packaged AIsa skill runtime.",
            "format": "password",
        }
    return {
        "type": "string",
        "title": humanize_env_name(env_name),
        "description": f"Optional runtime setting for {env_name}.",
    }


def build_config_schema(skill: dict[str, object]) -> dict[str, object]:
    env_vars = [env_name for env_name in skill.get("env_vars", []) if isinstance(env_name, str)]
    optional_env_vars = [env_name for env_name in skill.get("optional_env_vars", []) if isinstance(env_name, str)]
    properties: dict[str, object] = {}
    for env_name in env_vars + optional_env_vars:
        properties[env_name] = build_config_property(env_name)

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
    runtime_requirements = build_runtime_requirements(skill)
    runtime_metadata = build_runtime_metadata(skill)
    config_schema = build_config_schema(skill)
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
        "repository": SOURCE_REPO,
        "license": skill["license"],
        "metadata": runtime_metadata,
        "configSchema": config_schema,
        "runtimeRequirements": runtime_requirements,
        "aisa": runtime_metadata["aisa"],
        "openclaw": {
            "runtimeRequirements": runtime_requirements,
        },
    }
    write_json(plugin_dir / ".claude-plugin" / "plugin.json", manifest)

    openclaw_manifest = {
        "id": slug,
        "name": base.prettify_skill_name(skill_name),
        "description": plugin_description(skill),
        "version": skill["version"],
        "skills": ["./skills"],
        "configSchema": config_schema,
        "runtimeRequirements": runtime_requirements,
        "metadata": runtime_metadata,
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
            "url": f"{SOURCE_REPO}.git",
        },
        "metadata": runtime_metadata,
        "aisa": runtime_metadata["aisa"],
        "openclaw": {
            "extensions": ["./index.ts"],
            "compat": {
                "pluginApi": "^1.0.0",
            },
            "build": {
                "openclawVersion": "^1.0.0",
            },
            "runtimeRequirements": runtime_requirements,
        },
    }
    write_json(plugin_dir / "package.json", package_json)

    readme_lines = [
        f"# {base.prettify_skill_name(skill_name)} Plugin",
        "",
        "ClawHub/OpenClaw native-first plugin wrapper for the packaged AIsa skill.",
        "",
        "## Runtime Requirements",
        "",
        f"- Required bins: `{', '.join(skill['required_bins'])}`" if skill.get("required_bins") else "- Required bins: none",
        f"- Required env vars: `{', '.join(skill['env_vars'])}`" if skill.get("env_vars") else "- Required env vars: none",
        f"- Primary env: `{skill['primary_env']}`" if skill.get("primary_env") else "- Primary env: none",
        (
            f"- Network target: `{relay_default_url(skill)}`"
            if relay_default_url(skill)
            else "- Network target: `https://api.aisa.one`"
            if "AISA_API_KEY" in skill.get("env_vars", [])
            else "- Network target: see the packaged skill's runtime docs"
        ),
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
        "## Provenance",
        "",
        f"- Source repository: `{SOURCE_REPO}`",
        f"- Embedded skill path: `skills/{skill['path']}/SKILL.md`",
        "- The runtime behavior remains inside the packaged skill payload and its public docs.",
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
