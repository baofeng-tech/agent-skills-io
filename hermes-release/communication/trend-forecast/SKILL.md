---
name: trend-forecast
description: 'Multi-signal trend forecasting for autonomous agents. Combines prediction market odds, Twitter/X social sentiment, news velocity, and stock market data into a unified trend analysis with confidence scoring. Powered by AIsa — one API key, five data streams. Use when: the user needs X/Twitter research, monitoring, posting, or engagement workflows.'
version: 1.0.0
metadata:
  aisa:
    emoji: 🛠
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  hermes:
    tags:
    - communication
    - twitter
    - x
    - search
    - research
    - market
    - stock
    - prediction
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# trend-forecast

Multi-signal trend forecasting for autonomous agents. Combines prediction market odds, Twitter/X social sentiment, news velocity, and stock market data into a unified trend analysis with confidence scoring. Powered by AIsa — one API key, five data streams. Use when: the user needs X/Twitter research, monitoring, posting, or engagement workflows.

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Quick Reference

- `python3 scripts/aisa_client.py --help`
- `python3 scripts/trend_forecast.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
