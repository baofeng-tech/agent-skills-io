---
name: last30days
description: Research the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search. Returns a ranked, clustered brief with citations. Use when the task needs recent social evidence, competitor comparisons, launch reactions, trend scans, or person/company profiles.
license: MIT
metadata:
  aisa:
    emoji: 🛠
    requires:
      bins:
      - python3
      - bash
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
    - x
    - youtube
    - search
    - market
    related_skills:
    - search
    - aisa-multi-search-engine
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# last30days

Research the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search. Returns a ranked, clustered brief with citations. Use when the task needs recent social evidence, competitor comparisons, launch reactions, trend scans, or person/company profiles.

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Quick Reference

- `bash scripts/run-last30days.sh --help`
- `bash scripts/dev-python.sh --help`
- `python3 scripts/last30days.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
