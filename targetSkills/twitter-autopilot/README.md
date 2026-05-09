# Twitter Autopilot 🐦

Twitter/X research and account actions for autonomous agents, powered by AIsa.

This skill supports three main workflows:

- **Read and search** Twitter/X data without user login
- **Engage** with tweets and users after OAuth authorization
- **Publish** posts and replies after OAuth authorization

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## What it does

### Read & search

Use `scripts/twitter_client.py` to:

- get user info and account metadata
- fetch recent tweets, mentions, followers, and followings
- search tweets and users
- inspect replies, quotes, retweeters, and thread context
- review trends, lists, communities, and Spaces

These read operations do not require Twitter/X login.

### Engagement via relay

Use `scripts/twitter_engagement_client.py` for authenticated actions such as:

- liking or unliking tweets
- following or unfollowing users
- listing recent tweets to support follow-up actions

These actions require user OAuth authorization and have real side effects on Twitter/X.

### Publishing

Publishing flows are documented in [`./references/post_twitter.md`](./references/post_twitter.md).

Use them when the user wants to publish, reply, or quote-post on X/Twitter after completing OAuth authorization in the browser.

## Installation

```bash
export AISA_API_KEY="your-key"
```

## Quick start

### Read & search

```bash
# Get user info and search tweets
python scripts/twitter_client.py user-info --username elonmusk
python scripts/twitter_client.py search --query "AI agents"
python scripts/twitter_client.py trends --woeid 1
```

### Engagement (requires OAuth)

```bash
# Like the latest tweet from a user
python scripts/twitter_engagement_client.py like-latest --user "@elonmusk"

# Query recent tweets for indexed follow-up actions
python scripts/twitter_engagement_client.py list-tweets --user "@elonmusk" --limit 10

# Follow a user
python scripts/twitter_engagement_client.py follow-user --user "@elonmusk"
```

### Publish (requires OAuth)

```bash
# Publish a text post
python scripts/twitter_oauth_client.py post --text "Hello from AIsa!"

# Publish a post with media
python scripts/twitter_oauth_client.py post --text "Check out this image" --media-file ./photo.png
```

> For engagement workflows, see [`./references/engage_twitter.md`](./references/engage_twitter.md). For publishing, authorization, and threading guidance, see [`./references/post_twitter.md`](./references/post_twitter.md).

## Get an API key

Sign up at [aisa.one](https://aisa.one).

## Links

- [AIsa](https://aisa.one)
- [API Reference](https://aisa.one/docs/api-reference/)

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
