---
name: aisa-twitter-command-center
description: 'Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay as a watchlist and trend desk. Use when: the user needs competitor monitoring, recurring watchlists, trend scanning, or profile sweeps without sharing passwords. Supports approved posting as follow-through, but prioritizes monitoring over engagement automation.'
license: Apache-2.0
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  aisa:
    emoji: 🐦
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
---

# AIsa Twitter Watchlist Desk

Track watchlists, competitor moves, and trend shifts on X/Twitter through the AIsa relay, then follow through with approved posting when needed.

## When to use

- The user wants recurring Twitter/X monitoring, competitor tracking, or watchlist-style research.
- The user wants to inspect profiles, timelines, mentions, trends, replies, quotes, lists, communities, or Spaces on a repeated basis.
- The user may need to draft or publish a post after the monitoring pass, with explicit OAuth approval.

## When NOT to use

- The user needs one flagship all-purpose Twitter skill; use `aisa-twitter-api`.
- The main job is likes, follows, or ongoing engagement operations better handled by `aisa-twitter-engagement-suite`.
- The workflow must avoid relay-based calls to `api.aisa.one`.

## Quick Reference

- Required environment variable: `AISA_API_KEY`
- Relay target: `https://api.aisa.one`
- Read client: `scripts/twitter_client.py`
- OAuth and posting client: `scripts/twitter_oauth_client.py`
- Posting guide: `references/post_twitter.md`

## Setup

```bash
export AISA_API_KEY="your-key"
```

All network calls go to `https://api.aisa.one/apis/v1/...`.

## Capabilities

- Read user data, timelines, mentions, followers, followings, and related profile information.
- Search tweets and users, inspect replies, quotes, retweeters, thread context, trends, lists, communities, and Spaces.
- Monitor recurring watchlists, launches, and creator or competitor activity.
- Publish text, image, and video posts after explicit OAuth approval when monitoring turns into action.
- Return an authorization link when posting access has not been approved yet.

## Common Commands

```bash
python3 scripts/twitter_client.py user-info --username elonmusk
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_client.py trends --woeid 1
python3 scripts/twitter_oauth_client.py status
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa"
```

## Posting Workflow

When the user asks to send, publish, reply, or quote on X/Twitter:

1. Check whether `AISA_API_KEY` is configured.
2. If the user intent is to publish, attempt the publish workflow.
3. If authorization has not been completed, return the OAuth authorization link first.
4. Use `--media-file` only for user-provided local workspace files.
5. Do not claim the post succeeded until the publish command actually succeeds.

## Guardrails

- Do not ask for Twitter passwords or browser cookies.
- Do not invent captions, tweet URLs, or attachment files.
- Do not default to browser opening unless the user explicitly wants local browser launch.
- Do not claim external posting succeeded until the API confirms success.

## Security Notes

- The workflow is relay-based and sends API requests, OAuth requests, and approved media uploads to `api.aisa.one`.
- Required secret: `AISA_API_KEY`.
- This workflow does not require passwords, browser cookie extraction, or direct account credential sharing.

## References

- See `references/post_twitter.md` for detailed posting examples and OAuth guidance.
