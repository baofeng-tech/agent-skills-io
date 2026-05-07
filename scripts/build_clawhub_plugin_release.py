#!/usr/bin/env python3
"""Build native-first ClawHub plugin packages from clawhub-release/ skills."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import build_claude_release as base
from release_zip import write_deterministic_zip


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
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "INCLUDE_SOURCES",
    "LAST30DAYS_CONFIG_DIR",
    "LAST30DAYS_DEBUG",
    "LAST30DAYS_FUN_MODEL",
    "LAST30DAYS_PLANNER_MODEL",
    "LAST30DAYS_REASONING_PROVIDER",
    "LAST30DAYS_REDDIT_COMMENTS",
    "LAST30DAYS_RERANK_MODEL",
    "LAST30DAYS_X_BACKEND",
    "LAST30DAYS_YOUTUBE_TRANSCRIPTS",
    "TWITTER_RELAY_BASE_URL",
    "TWITTER_RELAY_TIMEOUT",
    "XIAOHONGSHU_API_BASE",
}
OPTIONAL_ENV_IGNORE = {
    "AISA_API_KEY",
    "CLAUDE_PLUGIN_ROOT",
}
OPTIONAL_ENV_ORDER = {
    "LAST30DAYS_PLANNER_MODEL": 10,
    "LAST30DAYS_RERANK_MODEL": 20,
    "LAST30DAYS_FUN_MODEL": 30,
    "LAST30DAYS_REASONING_PROVIDER": 40,
    "AISA_MODEL": 50,
    "AISA_BASE_URL": 60,
    "INCLUDE_SOURCES": 70,
    "LAST30DAYS_X_BACKEND": 80,
    "LAST30DAYS_YOUTUBE_TRANSCRIPTS": 90,
    "LAST30DAYS_REDDIT_COMMENTS": 100,
    "GH_TOKEN": 110,
    "GITHUB_TOKEN": 120,
    "LAST30DAYS_CONFIG_DIR": 130,
    "LAST30DAYS_DEBUG": 140,
    "TWITTER_RELAY_BASE_URL": 150,
    "TWITTER_RELAY_TIMEOUT": 160,
    "XIAOHONGSHU_API_BASE": 170,
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
    network_targets = infer_network_targets(skill, env_vars)

    if required_bins:
        requirements["bins"] = required_bins
    if env_vars:
        requirements["env"] = env_vars
    if optional_env_vars:
        requirements["optionalEnv"] = optional_env_vars
    if primary_env:
        requirements["primaryEnv"] = primary_env
    if network_targets:
        requirements["networkTargets"] = network_targets
    return requirements


def infer_network_targets(skill: dict[str, object], env_vars: list[str]) -> list[str]:
    targets: list[str] = []
    relay_target = relay_default_url(skill)
    if relay_target:
        targets.append(relay_target)
    elif "AISA_API_KEY" in env_vars:
        targets.append("https://api.aisa.one")

    lower = f"{skill.get('name', '')} {skill.get('path', '')}".lower()
    if "last30days" in lower:
        targets.extend(["https://www.reddit.com", "https://hacker-news.firebaseio.com"])
        if "last30days-zh" not in lower:
            targets.append("https://api.github.com")
        targets.append("https://www.xiaohongshu.com")
    return list(dict.fromkeys(targets))


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


def build_top_level_runtime_fields(runtime: dict[str, object]) -> dict[str, object]:
    fields: dict[str, object] = {}
    requires: dict[str, object] = {}
    if runtime.get("bins"):
        requires["bins"] = runtime["bins"]
    if runtime.get("env"):
        requires["env"] = runtime["env"]
    if requires:
        fields["requires"] = requires
    for key in ("optionalEnv", "primaryEnv", "networkTargets"):
        if runtime.get(key):
            fields[key] = runtime[key]
    return fields


def infer_optional_env_vars(skill_dir: Path, metadata: dict[str, object]) -> list[str]:
    merged: list[str] = []
    for scope in ("aisa", "openclaw"):
        scoped = metadata.get(scope) if isinstance(metadata.get(scope), dict) else {}
        optional_envs = scoped.get("optionalEnv") if isinstance(scoped, dict) else None
        if isinstance(optional_envs, list):
            for env_name in optional_envs:
                if (
                    isinstance(env_name, str)
                    and env_name in OPTIONAL_ENV_ALLOWLIST
                    and env_name not in OPTIONAL_ENV_IGNORE
                    and env_name not in merged
                ):
                    merged.append(env_name)
    if merged:
        return merged

    for path in sorted(skill_dir.rglob("*")):
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
    return sorted(merged, key=lambda name: (OPTIONAL_ENV_ORDER.get(name, 999), name))


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


def build_config_ui_hints(skill: dict[str, object]) -> dict[str, object]:
    env_vars = [env_name for env_name in skill.get("env_vars", []) if isinstance(env_name, str)]
    optional_env_vars = [env_name for env_name in skill.get("optional_env_vars", []) if isinstance(env_name, str)]
    hints: dict[str, object] = {}
    for env_name in env_vars + optional_env_vars:
        field_hint: dict[str, object] = {
            "label": humanize_env_name(env_name),
            "help": (
                f"Required runtime secret for {env_name}."
                if env_name in env_vars
                else f"Optional advanced runtime setting for {env_name}."
            ),
        }
        if env_name.endswith("_API_KEY") or env_name in {"AISA_API_KEY"}:
            field_hint["sensitive"] = True
        if env_name in optional_env_vars:
            field_hint["advanced"] = True
        hints[env_name] = field_hint
    if skill.get("emoji"):
        hints["emoji"] = skill["emoji"]
    return hints


def build_provider_auth_fields(skill: dict[str, object]) -> dict[str, object]:
    env_vars = [env_name for env_name in skill.get("env_vars", []) if isinstance(env_name, str)]
    if "AISA_API_KEY" not in env_vars:
        return {}
    return {
        "providers": ["aisa"],
        "providerAuthEnvVars": {
            "aisa": ["AISA_API_KEY"],
        },
        "providerAuthChoices": [
            {
                "provider": "aisa",
                "method": "api-key",
                "choiceId": "aisa-api-key",
                "choiceLabel": "AISA API key",
                "choiceHint": "Used only to authorize requests to the AIsa API service.",
                "groupId": "aisa",
                "groupLabel": "AIsa",
                "optionKey": "aisaApiKey",
                "cliFlag": "--aisa-api-key",
                "cliOption": "--aisa-api-key <key>",
                "cliDescription": "AISA_API_KEY used by the packaged skill runtime.",
                "onboardingScopes": ["text-inference"],
                "assistantPriority": 0,
            }
        ],
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_root_skill_manifest(
    plugin_dir: Path,
    skill: dict[str, object],
    slug: str,
    runtime_requirements: dict[str, object],
    runtime_metadata: dict[str, object],
) -> None:
    frontmatter: dict[str, object] = {
        "name": slug,
        "description": plugin_description(skill),
        "version": skill["version"],
        "license": skill["license"],
        "requires": {
            "bins": runtime_requirements.get("bins", []),
            "env": runtime_requirements.get("env", []),
        },
        "metadata": runtime_metadata,
    }
    if runtime_requirements.get("primaryEnv"):
        frontmatter["primaryEnv"] = runtime_requirements["primaryEnv"]
    if runtime_requirements.get("optionalEnv"):
        frontmatter["optionalEnv"] = runtime_requirements["optionalEnv"]
    if runtime_requirements.get("networkTargets"):
        frontmatter["networkTargets"] = runtime_requirements["networkTargets"]

    body = "\n".join(
        [
            f"# {base.prettify_skill_name(str(skill['name']))} Plugin",
            "",
            "This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.",
            "",
            f"- Packaged skill: `skills/{skill['path']}/`",
            "- Native manifest: `openclaw.plugin.json`",
            "- Claude-compatible fallback: `.claude-plugin/plugin.json`",
        ]
    )
    (plugin_dir / "SKILL.md").write_text(base.dump_skill(frontmatter, body), encoding="utf-8")


def zip_plugin(source_dir: Path, zip_path: Path) -> None:
    write_deterministic_zip(source_dir, zip_path, compresslevel=1)


def build_plugin(skill: dict[str, object]) -> dict[str, str]:
    skill_name = skill["name"]
    slug = plugin_slug(skill_name)
    plugin_dir = PLUGIN_ROOT / slug
    runtime_requirements = build_runtime_requirements(skill)
    runtime_metadata = build_runtime_metadata(skill)
    top_level_runtime_fields = build_top_level_runtime_fields(runtime_requirements)
    config_schema = build_config_schema(skill)
    config_ui_hints = build_config_ui_hints(skill)
    provider_auth_fields = build_provider_auth_fields(skill)
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
        **top_level_runtime_fields,
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
        **provider_auth_fields,
        **top_level_runtime_fields,
    }
    if config_ui_hints:
        openclaw_manifest["uiHints"] = config_ui_hints
    write_json(plugin_dir / "openclaw.plugin.json", openclaw_manifest)
    write_root_skill_manifest(plugin_dir, skill, slug, runtime_requirements, runtime_metadata)

    index_js = [
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
    (plugin_dir / "index.js").write_text("\n".join(index_js) + "\n", encoding="utf-8")

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
        "configSchema": config_schema,
        "runtimeRequirements": runtime_requirements,
        "metadata": runtime_metadata,
        **top_level_runtime_fields,
        "aisa": runtime_metadata["aisa"],
        "openclaw": {
            "extensions": ["./index.js"],
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

    network_targets = runtime_requirements.get("networkTargets")
    if isinstance(network_targets, list) and network_targets:
        network_line = f"- Network targets: `{', '.join(str(target) for target in network_targets)}`"
    elif relay_default_url(skill):
        network_line = f"- Network target: `{relay_default_url(skill)}`"
    elif "AISA_API_KEY" in skill.get("env_vars", []):
        network_line = "- Network target: `https://api.aisa.one`"
    else:
        network_line = "- Network target: see the packaged skill's runtime docs"

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
        network_line,
        "",
        "## What It Ships",
        "",
        f"- Bundle plugin id: `{slug}`",
        f"- Native manifest: `openclaw.plugin.json`",
        f"- Native entrypoint: `index.js`",
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
        "- Packaging mode: native-first dual format (`openclaw.plugin.json` + `index.js` + `package.json` + optional `.claude-plugin/plugin.json` + embedded `skills/`)",
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
