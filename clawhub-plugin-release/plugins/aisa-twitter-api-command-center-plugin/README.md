# AIsa Twitter API Command Center Plugin

ClawHub/OpenClaw native-first plugin wrapper for the packaged AIsa skill.

## Runtime Requirements

- Required bins: `python3`
- Required env vars: `AISA_API_KEY`
- Optional env vars: `TWITTER_RELAY_BASE_URL, TWITTER_RELAY_TIMEOUT`
- Primary env: `AISA_API_KEY`
- Network target: configured relay, default `https://api.aisa.one/apis/v1/twitter`

## What It Ships

- Bundle plugin id: `aisa-twitter-api-command-center-plugin`
- Native manifest: `openclaw.plugin.json`
- Native entrypoint: `index.ts`
- Embedded skill: `skills/aisa-twitter-api-command-center/SKILL.md`
- Format: native OpenClaw plugin plus Claude-compatible bundle fallback

## Why This Format

- Uses the OpenClaw-native manifest path that current plugin docs expect.
- Keeps the packaged skill payload intact under `skills/` for ClawHub/OpenClaw skill loading.
- Retains `.claude-plugin/plugin.json` so Claude-compatible marketplace tooling still recognizes the package.
- Reuses the already-hardened `clawhub-release/` skill payload.

## Install After Publishing

```bash
openclaw plugins install clawhub:aisa-twitter-api-command-center-plugin
```

## Publish Locally

```bash
clawhub package publish ./plugins/aisa-twitter-api-command-center-plugin --dry-run
clawhub package publish ./plugins/aisa-twitter-api-command-center-plugin
```

## Notes

- Runtime requirements and guardrails remain inside `skills/aisa-twitter-api-command-center/SKILL.md`.
- If both native and bundle markers exist, OpenClaw prefers the native plugin path.
- This package keeps side effects explicit and relies on the packaged skill's repo-local defaults where applicable.
- OAuth, approved posting, and engagement actions default to `https://api.aisa.one/apis/v1/twitter` unless `TWITTER_RELAY_BASE_URL` is set.
- Media files are uploaded only when the user explicitly attached them, and they are sent to the configured relay first.
