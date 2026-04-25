---
name: aisa-twitter-post-engage
description: 'Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.'
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

# AIsa Twitter Post Engage

Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## When to use

- The user needs Twitter/X research, monitoring, posting, or engagement workflows.
- The user wants profiles, timelines, trends, lists, communities, or Spaces.
- The user wants approved posting without sharing passwords.

## High-Intent Workflows

- Research an account or conversation thread.
- Monitor a keyword, trend, or competitor.
- Authorize and publish a post after explicit approval.

## Quick Reference

- `python3 scripts/twitter_client.py --help`
- `python3 scripts/twitter_engagement_client.py --help`
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

- Research recent AI agent conversations on X
- Search how users are reacting to a product launch on Twitter
- Authorize and publish a short product update post

## Guardrails

- Do not ask for passwords, cookies, or browser credentials.
- Do not claim posting succeeded until the API confirms it.
- Return authorization links instead of relying on auto-open behavior.
- Only upload local files the user explicitly attached, and make it clear those files are sent to the configured AIsa relay first.
