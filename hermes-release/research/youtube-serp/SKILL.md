---
name: youtube-serp
description: 'Search YouTube result pages through AISA to find ranking videos, channels, and trends for content research, competitor tracking, and regional discovery. Use when: you need YouTube SERP data for a topic, market, or channel niche.'
license: MIT
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
    - research
    - youtube
    - search
    - market
    - video
    - aisa
    related_skills:
    - aisa-youtube-search
    - aisa-youtube-serp-scout
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# youtube-serp

Search YouTube result pages through AISA to find ranking videos, channels, and trends for content research, competitor tracking, and regional discovery. Use when: you need YouTube SERP data for a topic, market, or channel niche.

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Quick Reference

- `python3 scripts/youtube_client.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
