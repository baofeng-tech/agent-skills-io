---
name: youtube-serp-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `youtube-serp`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube result pages through AISA to find ranking videos, channels, and trends for content research, competitor tracking, and regional discovery. Use when: you need YouTube SERP data for a topic, market, or channel niche.'
version: 1.0.0
license: MIT
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
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one
---

# Youtube Serp Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/youtube-serp/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
