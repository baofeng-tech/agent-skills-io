# AIsa Twitter Command Center

An [Agent Skill](https://agentskills.io) for searching, monitoring, and publishing on X/Twitter.

Works with **Hermes Agent**, **Claude Code**, **OpenAI Codex**, **Cursor**, and any agent that supports the [agentskills.io](https://agentskills.io/specification) open standard.

## What it does

Full Twitter/X data access through a single API key. No scraping, no passwords, no proxies.

**Read (no login required):**

- User profiles, timelines, mentions, followers, followings
- Tweet search (Latest / Top), replies, quotes, retweeters, threads
- Trending topics, Lists, Communities, Spaces

**Write (OAuth relay):**

- Publish tweets after one-time browser authorization

## Install

### Hermes Agent

```bash
hermes skills install github:AIsaONE/agent-skills/aisa-twitter-command-center
```

### skills.sh

```bash
npx skills add AIsaONE/agent-skills
```

### Claude Code

```bash
# Copy to your skills directory
cp -r aisa-twitter-command-center ~/.claude/skills/
```

### Manual (any agent)

Copy the `aisa-twitter-command-center/` directory to your agent's skills folder.

## Setup

```bash
export AISA_API_KEY="your-key"
```

Get your API key at [aisa.one](https://aisa.one). Pay-as-you-go pricing, ~$0.0004 per read query.

## Structure

```
aisa-twitter-command-center/
├── SKILL.md                          # Main instructions
├── scripts/
│   ├── twitter_client.py             # Full-featured CLI client
│   └── twitter_oauth_client.py       # OAuth posting helper
└── references/
    └── api-endpoints.md              # Complete endpoint reference
```

## Usage Examples

Just ask your agent naturally:

- "What's trending on Twitter right now?"
- "Get @anthropic's latest tweets"
- "Search for tweets about AI agents"
- "Who are the top followers of @elonmusk?"
- "Post this to X: we shipped v2.0"

## More AIsa Skills

AIsa provides a unified API for many services. Check out our other skills:

- **[Prediction Market](https://github.com/AIsaONE/agent-skills/tree/main/aisa-prediction-market)** — Polymarket + Kalshi
- **[Web & Academic Search](https://github.com/AIsaONE/agent-skills/tree/main/aisa-search)** — Multi-source search with confidence scoring
- **[Financial Market Data](https://github.com/AIsaONE/agent-skills/tree/main/aisa-market-pulse)** — Stocks + Crypto
- **[YouTube Search](https://github.com/AIsaONE/agent-skills/tree/main/aisa-youtube-search)** — Video discovery

All powered by a single `AISA_API_KEY`.

## License

Apache-2.0
