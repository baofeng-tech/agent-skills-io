# Saas Gateway Plugin

ClawHub/OpenClaw native-first plugin wrapper for the packaged AIsa skill.

## Runtime Requirements

- Required bins: none
- Required env vars: `AISA_API_KEY`
- Primary env: `AISA_API_KEY`
- Network targets: `https://api.aisa.one`

## What It Ships

- Bundle plugin id: `saas-gateway-plugin`
- Native manifest: `openclaw.plugin.json`
- Native entrypoint: `index.js`
- Embedded skill: `skills/saas-gateway/SKILL.md`
- Format: native OpenClaw plugin plus Claude-compatible bundle fallback

## Why This Format

- Uses the OpenClaw-native manifest path that current plugin docs expect.
- Keeps the packaged skill payload intact under `skills/` for ClawHub/OpenClaw skill loading.
- Retains `.claude-plugin/plugin.json` so Claude-compatible marketplace tooling still recognizes the package.
- Reuses the already-hardened `clawhub-release/` skill payload.

## Provenance

- Source repository: `https://github.com/baofeng-tech/agent-skills-io`
- Embedded skill path: `skills/saas-gateway/SKILL.md`
- The runtime behavior remains inside the packaged skill payload and its public docs.

## Install After Publishing

```bash
openclaw plugins install clawhub:saas-gateway-plugin
```

## Publish Locally

```bash
clawhub package publish ./plugins/saas-gateway-plugin --dry-run
clawhub package publish ./plugins/saas-gateway-plugin
```

## Notes

- Runtime requirements and guardrails remain inside `skills/saas-gateway/SKILL.md`.
- If both native and bundle markers exist, OpenClaw prefers the native plugin path.
- This package keeps side effects explicit and relies on the packaged skill's repo-local defaults where applicable.
