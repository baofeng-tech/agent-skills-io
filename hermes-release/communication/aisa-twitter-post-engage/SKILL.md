---
name: aisa-twitter-post-engage
description: Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.
license: Apache-2.0
metadata:
  hermes:
    tags:
    - communication
    - twitter
    - x
    - search
    - research
    - aisa
    related_skills:
    - aisa-twitter-command-center
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# AIsa Twitter Post Engage

Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay.

## When to Use

- The user wants Twitter/X research plus posting, liking, unliking, following, or unfollowing workflows.
- The task can use a Python client with `AISA_API_KEY` and explicit OAuth approval.
- The workflow needs a single package that covers read, post, and engagement actions.

## Pitfalls

- The user needs cookie extraction, password login, or a fully local Twitter client.
- The workflow must avoid relay-based network calls or media upload through `api.aisa.one`.
- The task needs undocumented secrets or browser-derived auth values.

## Quick Reference

- Required environment variable: `AISA_API_KEY`
- Read client: `scripts/twitter_client.py`
- Post client: `scripts/twitter_oauth_client.py`
- Engage client: `scripts/twitter_engagement_client.py`
- References: `references/post_twitter.md`, `references/engage_twitter.md`

## Setup

```bash
export AISA_API_KEY="your-key"
```

All network calls go to `https://api.aisa.one/apis/v1/...`.

## Capabilities

- Read user, tweet, trend, list, community, and Spaces data.
- Publish text, image, and video posts after explicit OAuth approval.
- Like, unlike, follow, and unfollow through the engagement client once authorization exists.

## Common Commands

```bash
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa"
python3 scripts/twitter_engagement_client.py like-latest --user "@elonmusk"
python3 scripts/twitter_engagement_client.py follow-user --user "@elonmusk"
```

## Workflow

- Use `references/post_twitter.md` for post, reply, quote, and media-upload actions.
- Use `references/engage_twitter.md` for likes, unlikes, follows, and unfollows.
- Obtain OAuth authorization before any write action.

## Guardrails

- Do not ask for passwords, browser cookies, or undocumented secrets.
- Do not guess target accounts or tweet IDs when multiple candidates exist.
- Do not claim engagement or posting succeeded unless the relay request returns success.

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow is stateful, re-run a read/list/status command to verify the new state.
