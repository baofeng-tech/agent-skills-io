---
name: aisa-twitter-command-center
description: 'Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay as a watchlist and trend desk. Use when: the user needs competitor monitoring, recurring watchlists, trend scanning, or profile sweeps without sharing passwords. Supports approved posting as follow-through, but prioritizes monitoring over engagement automation.'
license: Apache-2.0
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
    - aisa
    related_skills:
    - aisa-twitter-post-engage
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# aisa-twitter-command-center

Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay as a watchlist and trend desk. Use when: the user needs competitor monitoring, recurring watchlists, trend scanning, or profile sweeps without sharing passwords. Supports approved posting as follow-through, but prioritizes monitoring over engagement automation.

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Quick Reference

- `python3 scripts/twitter_client.py --help`
- `python3 scripts/twitter_oauth_client.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
