---
name: aisa-twitter-api
description: 'Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa. Use when: the user needs one flagship Twitter skill for trend tracking, competitor monitoring, or publish-ready workflows. Supports search, watchlists, and approved posting.'
author: AIsa
version: 1.0.0
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 🐦
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    optionalEnv:
    - TWITTER_RELAY_BASE_URL
    - TWITTER_RELAY_TIMEOUT
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 🐦
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    optionalEnv:
    - TWITTER_RELAY_BASE_URL
    - TWITTER_RELAY_TIMEOUT
    primaryEnv: AISA_API_KEY
---

# AIsa Twitter API Command Center

Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa. Use when: the user needs one flagship Twitter skill for trend tracking, competitor monitoring, or publish-ready workflows. Supports search, watchlists, and approved posting.

## When to use

- The user needs one flagship Twitter/X skill for research, monitoring, watchlists, or posting.
- The user wants to move between search, monitoring, and publish-ready workflows without switching skills.
- The user wants approved posting without sharing passwords.

## High-Intent Workflows

- Research a creator, competitor, or narrative shift.
- Monitor a keyword, watchlist, or launch reaction.
- Authorize and publish a post only after explicit approval.

## Quick Reference

- `python3 scripts/twitter_client.py --help`
- `python3 scripts/twitter_oauth_client.py --help`

## Setup

- `AISA_API_KEY` is required for AIsa-backed API access.
- Use repo-relative `scripts/` paths from the shipped package.
- Prefer explicit CLI auth flags when a script exposes them.
- Optional: set `TWITTER_RELAY_BASE_URL` to override the default relay `https://api.aisa.one/apis/v1/twitter`.
- Optional: set `TWITTER_RELAY_TIMEOUT` to tune relay request timeouts in seconds.
- OAuth requests and any user-approved media uploads use the configured AIsa relay and default to `https://api.aisa.one/apis/v1/twitter`.
- Provide only `AISA_API_KEY`; do not use passwords, cookies, or browser credential export.

## Example Requests

- Research what AI agent builders are saying on X this week
- Track what changed across a competitor watchlist today
- Authorize and publish a short product update with an image

## Guardrails

- Do not ask for passwords, cookies, or browser credentials.
- Do not market growth actions as this package's primary lane.
- Do not claim posting succeeded until the API confirms it.
- Only upload local files the user explicitly attached, and make it clear those files are sent to the configured AIsa relay first.
