# Twitter Autopilot 🐦

Twitter/X intelligence and automation for agents, powered by AIsa.

This skill supports reading, searching, engagement workflows, and posting on Twitter/X.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Read and search**: Access user info, tweets, advanced search, trends, followers, lists, communities, and Spaces without user login.
- **Engagement via local relay**: Like/unlike tweets and follow/unfollow users after user authorization.
- **Posting via OAuth**: Publish text, images, videos, threads, replies, and quotes after user authorization.

## Installation

```bash
export AISA_API_KEY="your-key"
```

## Quick start

### Read and search
```bash
# Get user info and search tweets
python scripts/twitter_client.py user-info --username elonmusk
python scripts/twitter_client.py search --query "AI agents"
python scripts/twitter_client.py trends
```

### Post and publish (requires OAuth)
```bash
# Publish a text post
python scripts/twitter_oauth_client.py post --text "Hello from AIsa!"

# Publish a post with media
python scripts/twitter_oauth_client.py post --text "Check out this image" --media-file ./photo.png
```

### Engagement (requires authorization)
```bash
# Like the latest tweet from a user
python scripts/twitter_engagement_client.py like-latest --user "@elonmusk"

# Query recent tweets for indexed follow-up actions
python scripts/twitter_engagement_client.py list-tweets --user "@elonmusk" --limit 10

# Follow a user
python scripts/twitter_engagement_client.py follow-user --user "@elonmusk"
```

> For detailed engagement steps, see [`./references/engage_twitter.md`](./references/engage_twitter.md). For posting, authorization, and multi-chunk threading, see [`./references/post_twitter.md`](./references/post_twitter.md).

## Get API key

Sign up at [aisa.one](https://aisa.one)

## Links

- [AIsa](https://aisa.one)
- [API Reference](https://aisa.one/docs/api-reference/)

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
