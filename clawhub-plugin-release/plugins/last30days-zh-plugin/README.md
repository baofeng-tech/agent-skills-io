# Last30days Zh Plugin

ClawHub/OpenClaw native-first plugin wrapper for the packaged AIsa skill.

## Runtime Requirements

- Required bins: `python3, bash`
- Required env vars: `AISA_API_KEY`
- Optional env vars: none
- Primary env: `AISA_API_KEY`
- Network target: `https://api.aisa.one`

## What It Ships

- Bundle plugin id: `last30days-zh-plugin`
- Native manifest: `openclaw.plugin.json`
- Native entrypoint: `index.ts`
- Embedded skill: `skills/last30days-zh/SKILL.md`
- Format: native OpenClaw plugin plus Claude-compatible bundle fallback

## Why This Format

- Uses the OpenClaw-native manifest path that current plugin docs expect.
- Keeps the packaged skill payload intact under `skills/` for ClawHub/OpenClaw skill loading.
- Retains `.claude-plugin/plugin.json` so Claude-compatible marketplace tooling still recognizes the package.
- Reuses the already-hardened `clawhub-release/` skill payload.

## Install After Publishing

```bash
openclaw plugins install clawhub:last30days-zh-plugin
```

## Publish Locally

```bash
clawhub package publish ./plugins/last30days-zh-plugin --dry-run
clawhub package publish ./plugins/last30days-zh-plugin
```

## Notes

- Runtime requirements and guardrails remain inside `skills/last30days-zh/SKILL.md`.
- If both native and bundle markers exist, OpenClaw prefers the native plugin path.
- This package keeps side effects explicit and relies on the packaged skill's repo-local defaults where applicable.
