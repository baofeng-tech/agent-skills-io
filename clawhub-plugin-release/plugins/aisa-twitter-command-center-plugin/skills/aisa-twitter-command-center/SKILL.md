---
name: aisa-twitter-command-center
description: 'Run Twitter/X watchlists, competitor monitoring, trend scans, and OAuth-gated follow-through through AIsa. Use when: the user needs a monitoring-first Twitter desk for recurring account sweeps, launch reactions, or trend tracking. Supports search, monitoring, and approved posting after review.'
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

# AIsa Twitter Watchlist Desk

Run Twitter/X watchlists, competitor monitoring, trend scans, and OAuth-gated follow-through through AIsa. Use when: the user needs a monitoring-first Twitter desk for recurring account sweeps, launch reactions, or trend tracking. Supports search, monitoring, and approved posting after review.

## When to use

- The user needs recurring Twitter/X monitoring, watchlists, competitor sweeps, or trend scans.
- The user wants profiles, timelines, trends, lists, communities, or Spaces checked on a repeated basis.
- The user may follow the monitoring pass with an approved post, but monitoring stays primary.

## High-Intent Workflows

- Track what changed across a competitor watchlist today.
- Monitor reactions to a launch, narrative, or keyword over time.
- Review a monitoring pass before deciding whether to publish.

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

- Track a competitor watchlist and summarize what changed today
- Monitor how X is reacting to our launch this week
- Review a trend desk before publishing a follow-up post

## Guardrails

- Do not market this package as the flagship general-purpose Twitter lane.
- Do not treat likes, follows, or replies as the core job of this package.
- Do not claim posting succeeded until the API confirms it.
- Only upload local files the user explicitly attached, and make it clear those files are sent to the configured AIsa relay first.
