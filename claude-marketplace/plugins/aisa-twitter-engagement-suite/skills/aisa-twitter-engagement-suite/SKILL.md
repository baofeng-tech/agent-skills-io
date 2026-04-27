---
name: aisa-twitter-engagement-suite
description: 'Engagement-focused Twitter/X workflow for research, approved posting, likes, follows, and related actions through the AIsa relay. Use when: the user already knows which tweets or accounts to act on and needs explicit OAuth-gated engagement without sharing passwords. Supports read context, posting, and follow-through actions; all writes and uploads go to api.aisa.one.'
license: MIT-0
allowed-tools: Read Bash Grep
when_to_use: the user already knows which tweets or accounts to act on and needs explicit OAuth-gated engagement without sharing passwords. Supports read context, posting, and follow-through actions; all writes and uploads go to api.aisa.one
---

# AIsa Twitter Engagement Suite

Run explicit Twitter/X engagement workflows through the AIsa relay after the user decides what to post, like, follow, or reply to.

## When to use

- The user wants to like, unlike, follow, unfollow, or post on Twitter/X after explicit approval.
- The task already has a likely target account, tweet, or campaign and needs follow-through actions.
- The workflow can use a Python client with `AISA_API_KEY` and explicit OAuth approval.

## When NOT to use

- The user mainly needs one flagship Twitter/X surface for broad research or monitoring; use `aisa-twitter-api`.
- The task is primarily watchlists, trend scanning, or recurring monitoring better handled by `aisa-twitter-command-center`.
- The workflow must avoid relay-based network calls or media upload through `api.aisa.one`.

## Quick Reference

- Required environment variable: `AISA_API_KEY`
- Relay target: `https://api.aisa.one`
- Read client: `scripts/twitter_client.py`
- Post client: `scripts/twitter_oauth_client.py`
- Engage client: `scripts/twitter_engagement_client.py`
- References: `references/post_twitter.md`, `references/engage_twitter.md`

## Setup

```bash
export AISA_API_KEY="your-key"
```

All writes, OAuth approvals, and approved media uploads go to `https://api.aisa.one/apis/v1/...`.

## Common Commands

```bash
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_engagement_client.py like-latest --user "@elonmusk"
```

## Capabilities

- Research Twitter/X accounts, tweets, trends, lists, communities, and Spaces.
- Publish text, image, and video posts after explicit OAuth approval.
- Like, unlike, follow, and unfollow after authorization exists.

## Guardrails

- Do not ask for passwords, browser cookies, or undocumented secrets.
- Do not claim a like, follow, reply, or post succeeded until the relay returns success.
- Do not treat engagement as silent or automatic; all write actions require explicit approval.

## Security Notes

- This workflow is relay-based and sends API requests, OAuth approvals, and approved media uploads to `api.aisa.one`.
- Required secret: `AISA_API_KEY`.
- This package does not require password sharing or browser-cookie extraction.
