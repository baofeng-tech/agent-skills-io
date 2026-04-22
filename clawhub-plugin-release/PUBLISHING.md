# Publishing ClawHub Bundle Plugins

1. Build `targetSkills/` and `clawhub-release/` first.
2. Run `python3 scripts/build_clawhub_plugin_release.py`.
3. Dry-run each plugin with `clawhub package publish <dir> --dry-run`.
4. Publish the approved plugin directories with `clawhub package publish <dir>`.
5. Prefer publishing from a Git-backed repo so ClawHub can keep source attribution.

## Why Native-First Dual Format

- Current OpenClaw docs treat `openclaw.plugin.json` as the native plugin contract and prefer it over bundle markers.
- Keeping `.claude-plugin/plugin.json` alongside the native manifest preserves Claude-marketplace compatibility without giving up native ClawHub structure.
- The packaged skill still lives under `skills/`, so the runtime surface remains skill-first and conservative.
