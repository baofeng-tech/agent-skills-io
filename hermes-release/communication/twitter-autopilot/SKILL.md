---
name: twitter-autopilot
description: 'Search and read X (Twitter) data via AIsa API: user profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publish posts, like/unlike tweets, and follow/unfollow users through OAuth relay — no passwords or cookies needed. Use when asked about Twitter/X data, social listening, influencer monitoring, trending topics, competitor intel, posting to X, or engaging with tweets.'
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
    - aisa-twitter-command-center
    - aisa-twitter-post-engage
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# twitter-autopilot

Search and read X (Twitter) data via AIsa API: user profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publish posts, like/unlike tweets, and follow/unfollow users through OAuth relay — no passwords or cookies needed. Use when asked about Twitter/X data, social listening, influencer monitoring, trending topics, competitor intel, posting to X, or engaging with tweets.

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
- `python3 scripts/twitter_engagement_client.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
