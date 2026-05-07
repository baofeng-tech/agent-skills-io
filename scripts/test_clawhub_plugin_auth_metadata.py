#!/usr/bin/env python3
"""Lock ClawHub/OpenClaw plugin auth metadata for AISA-backed packages."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = REPO_ROOT / "clawhub-plugin-release" / "plugins"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def required_envs(manifest: dict[str, object]) -> list[str]:
    config_schema = manifest.get("configSchema")
    if not isinstance(config_schema, dict):
        return []
    required = config_schema.get("required")
    return [item for item in required if isinstance(item, str)] if isinstance(required, list) else []


def assert_aisa_auth_metadata(plugin_dir: Path) -> None:
    manifest_path = plugin_dir / "openclaw.plugin.json"
    manifest = load_json(manifest_path)
    if "AISA_API_KEY" not in required_envs(manifest):
        return

    providers = manifest.get("providers")
    assert isinstance(providers, list) and "aisa" in providers, f"{manifest_path}: missing providers.aisa"

    provider_auth_env_vars = manifest.get("providerAuthEnvVars")
    assert isinstance(provider_auth_env_vars, dict), f"{manifest_path}: missing providerAuthEnvVars"
    assert provider_auth_env_vars.get("aisa") == ["AISA_API_KEY"], (
        f"{manifest_path}: providerAuthEnvVars.aisa must declare AISA_API_KEY"
    )

    provider_auth_choices = manifest.get("providerAuthChoices")
    assert isinstance(provider_auth_choices, list) and any(
        isinstance(choice, dict)
        and choice.get("provider") == "aisa"
        and choice.get("choiceId") == "aisa-api-key"
        and choice.get("method") == "api-key"
        for choice in provider_auth_choices
    ), f"{manifest_path}: missing AISA api-key auth choice"

    config_ui_hints = manifest.get("configUiHints")
    assert isinstance(config_ui_hints, dict), f"{manifest_path}: missing configUiHints"
    aisa_hint = config_ui_hints.get("AISA_API_KEY")
    assert isinstance(aisa_hint, dict) and aisa_hint.get("sensitive") is True, (
        f"{manifest_path}: AISA_API_KEY must be marked sensitive"
    )

    bundled_skills = manifest.get("bundledSkills")
    assert isinstance(bundled_skills, list) and bundled_skills, (
        f"{manifest_path}: missing bundledSkills capability metadata"
    )

    commands = manifest.get("commands")
    assert isinstance(commands, list) and commands, f"{manifest_path}: missing command metadata"

    environment = manifest.get("environment")
    assert isinstance(environment, dict), f"{manifest_path}: missing environment metadata"
    runtime_requirements = manifest.get("runtimeRequirements")
    expected_bins = (
        runtime_requirements.get("bins")
        if isinstance(runtime_requirements, dict) and isinstance(runtime_requirements.get("bins"), list)
        else []
    )
    if expected_bins:
        assert environment.get("binaries"), f"{manifest_path}: environment must declare binaries"
    assert environment.get("externalServices"), (
        f"{manifest_path}: environment must declare external services"
    )


def main() -> None:
    plugin_dirs = sorted(path for path in PLUGIN_ROOT.iterdir() if path.is_dir())
    assert plugin_dirs, "No generated ClawHub plugins found"
    for plugin_dir in plugin_dirs:
        assert_aisa_auth_metadata(plugin_dir)
    print(f"Validated auth metadata for {len(plugin_dirs)} ClawHub plugin(s).")


if __name__ == "__main__":
    main()
