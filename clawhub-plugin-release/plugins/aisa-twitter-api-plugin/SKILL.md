---
name: aisa-twitter-api-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one/apis/v1/twitter. Native-first ClawHub plugin for `aisa-twitter-api`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Twitter/X command center for research, monitoring, watchlists, and approved posting through AIsa. Use when: the user needs one flagship skill for trend tracking, competitor monitoring, or publish-ready Twitter workflows without sharing passwords. Supports search, watchlists, and OAuth-gated posting.'
version: 1.0.5
license: Apache-2.0
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one/apis/v1/twitter
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one/apis/v1/twitter
---

# AIsa Twitter API Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/aisa-twitter-api/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
