---
name: kol-creator-discovery
description: 'Use this skill when a user needs KOL or influencer research, creator email lookup, similar-creator discovery, outreach-list building, influencer prospecting, or a contact table from TikTok, Instagram, or YouTube profile URLs. It uses AIsa''s WaveInflu APIs to find verified creator emails, match similar YouTube or TikTok creators, enrich each recommended profile with contact emails, and return an outreach-ready Markdown table without inventing missing data. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.'
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
    - aisa
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# kol-creator-discovery

Use this skill when a user needs KOL or influencer research, creator email lookup, similar-creator discovery, outreach-list building, influencer prospecting, or a contact table from TikTok, Instagram, or YouTube profile URLs. It uses AIsa's WaveInflu APIs to find verified creator emails, match similar YouTube or TikTok creators, enrich each recommended profile with contact emails, and return an outreach-ready Markdown table without inventing missing data. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Quick Reference

- `python3 scripts/kol_creator_discovery.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
