---
name: aisa-twitter-post-engage
description: 'Post-launch Twitter/X follow-through for search, approved posting, and lightweight engagement through the AIsa relay. Use when: the user already has a draft, campaign, launch tweet, or reply target and needs one focused skill to publish and then handle early interactions without sharing passwords. Supports posting, reply context, likes, and follows after explicit approval.'
license: Apache-2.0
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.0
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills
  tags: twitter,x,search,aisa
  platforms: agentskills.io,agentskill.sh,github
  primary_env: AISA_API_KEY
allowed-tools: Read Bash Grep
---

# AIsa Twitter Post-Launch Follow-Through

Publish on X/Twitter through the AIsa relay, then handle the first wave of replies, likes, and follow actions with explicit approval.

## When to use

- The user already has a draft, campaign, announcement, or reply target and needs post-and-follow-through support.
- The workflow needs one package that covers read context, publishing, and lightweight engagement after the post goes live.
- The task can use a Python client with `AISA_API_KEY` and explicit OAuth approval.

## When NOT to use

- The user mainly needs broad Twitter/X research or recurring monitoring; use `aisa-twitter-api` or `aisa-twitter-command-center`.
- The task is a larger ongoing engagement program better handled by `aisa-twitter-engagement-suite`.
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

All network calls go to `https://api.aisa.one/apis/v1/...`.

## Capabilities

- Read user, tweet, trend, list, community, and Spaces data.
- Publish text, image, and video posts after explicit OAuth approval.
- Like, unlike, follow, and unfollow through the engagement client once authorization exists.
- Move from pre-post research into immediate post-launch follow-through without switching skills.

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

## Security Notes

- This workflow is relay-based and sends API requests, OAuth approvals, and approved media uploads to `api.aisa.one`.
- Required secret: `AISA_API_KEY`.
- This package does not require password sharing or browser-cookie extraction.
