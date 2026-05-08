# Twitter Autopilot 🐦

Twitter/X research and automation for agents, powered by AIsa.

This skill supports **read/search**, **engagement**, and **posting** workflows for Twitter/X.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Read & Search**: Access user info, tweets, advanced search, trends, followers, lists, communities, and Spaces without user login.
- **Engagement via Relay**: Like/unlike tweets and follow/unfollow users through the local OAuth relay workflow.
- **Posting via OAuth**: Publish text and media posts, including reply and quote-style posting flows, after user authorization.

## Installation

```bash
export AISA_API_KEY="your-key"
```

## Quick Start

### Read & Search
```bash
# Get user info and search tweets
python3 scripts/twitter_client.py user-info --username elonmusk
python3 scripts/twitter_client.py search --query "AI agents"
python3 scripts/twitter_client.py trends
```

### Post & Write (Requires OAuth)
```bash
# Publish a text post
python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa!"

# Publish a post with media
python3 scripts/twitter_oauth_client.py post --text "Check out this image" --media-file ./photo.png
```

### Engagement (Requires OAuth Relay)
```bash
# Like the latest tweet from a user
python3 scripts/twitter_engagement_client.py like-latest --user "@elonmusk"

# Query recent tweets for indexed follow-up actions
python3 scripts/twitter_engagement_client.py list-tweets --user "@elonmusk" --limit 10

# Follow a user
python3 scripts/twitter_engagement_client.py follow-user --user "@elonmusk"
```

> For detailed engagement workflows, see [`./references/engage_twitter.md`](./references/engage_twitter.md). For publishing, authorization, and threading details, see [`./references/post_twitter.md`](./references/post_twitter.md).

## Get API Key

Sign up at [aisa.one](https://aisa.one)

## Links

- [AIsa](https://aisa.one)
- [API Reference](https://aisa.one/docs/api-reference/)

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference/) for the complete catalog of endpoints this skill can call.
