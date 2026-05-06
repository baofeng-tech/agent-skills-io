---
name: stock-dividend-plugin
description: Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `stock-dividend`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Analyze dividend metrics for stocks via AIsa API. Provides yield, payout ratio, growth CAGR, safety score (0-100), income rating, and Dividend Aristocrat/King status. Use when the user asks about dividends, income investing, or dividend safety.
version: 1.0.0
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
    optionalEnv:
    - AISA_BASE_URL
    - AISA_MODEL
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
optionalEnv:
- AISA_BASE_URL
- AISA_MODEL
networkTargets:
- https://api.aisa.one
---

# Stock Dividend Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/stock-dividend/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
