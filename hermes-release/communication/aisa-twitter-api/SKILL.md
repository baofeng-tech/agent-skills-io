---
name: aisa-twitter-api
description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth. Use when the user asks for Twitter research, monitoring, or posting without sharing passwords.
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
    - aisa-twitter-post-engage
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# AIsa Twitter API

Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth.

## When to Use

- The user wants Twitter/X research, monitoring, or content discovery.
- The user wants to inspect profiles, timelines, mentions, trends, replies, quotes, lists, communities, or Spaces.
- The user wants to draft or publish posts after explicit OAuth approval without sharing passwords.

## Pitfalls

- The user needs password-based login, cookie extraction, or browser credential scraping.
- The workflow must avoid relay-based calls to `api.aisa.one`.
- The request is for unsupported engagement actions not covered by this package.

## Quick Reference

- Required environment variable: `AISA_API_KEY`
- Read client: `scripts/twitter_client.py`
- OAuth and posting client: `scripts/twitter_oauth_client.py`
- Posting guide: `references/post_twitter.md`

## Setup

```bash
export AISA_API_KEY="your-key"
```

## Capabilities

- Read user data, timelines, mentions, followers, followings, and related profile information.
- Search tweets and users, inspect replies, quotes, retweeters, thread context, trends, lists, communities, and Spaces.
- Publish text, image, and video posts after explicit OAuth approval.

## Common Commands

```bash
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa"
```

## Guardrails

- Do not ask for Twitter passwords or browser cookies.
- Do not invent captions, tweet URLs, or attachment files.
- Do not claim external posting succeeded until the API confirms success.

## Security Notes

- The workflow is relay-based and sends API requests, OAuth requests, and approved media uploads to `api.aisa.one`.
- Required secret: `AISA_API_KEY`.
- This workflow does not require passwords or browser cookie extraction.

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow is stateful, re-run a read/list/status command to verify the new state.
