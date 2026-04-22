# Media Gen Plugin

ClawHub/OpenClaw native-first plugin wrapper for the packaged AIsa skill.

## What It Ships

- Bundle plugin id: `media-gen-plugin`
- Native manifest: `openclaw.plugin.json`
- Native entrypoint: `index.ts`
- Embedded skill: `skills/media-gen/SKILL.md`
- Format: native OpenClaw plugin plus Claude-compatible bundle fallback

## Why This Format

- Uses the OpenClaw-native manifest path that current plugin docs expect.
- Keeps the packaged skill payload intact under `skills/` for ClawHub/OpenClaw skill loading.
- Retains `.claude-plugin/plugin.json` so Claude-compatible marketplace tooling still recognizes the package.
- Reuses the already-hardened `clawhub-release/` skill payload.

## Install After Publishing

```bash
openclaw plugins install clawhub:media-gen-plugin
```

## Publish Locally

```bash
clawhub package publish ./plugins/media-gen-plugin --dry-run
clawhub package publish ./plugins/media-gen-plugin
```

## Notes

- Runtime requirements and guardrails remain inside `skills/media-gen/SKILL.md`.
- If both native and bundle markers exist, OpenClaw prefers the native plugin path.
- This package keeps side effects explicit and relies on the packaged skill's repo-local defaults where applicable.
