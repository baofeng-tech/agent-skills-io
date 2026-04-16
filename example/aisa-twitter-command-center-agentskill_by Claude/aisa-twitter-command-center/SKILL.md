---
name: aisa-twitter-command-center
description: >-
  Search and read X (Twitter) data via AIsa API: user profiles, timelines,
  mentions, followers, tweet search, trends, lists, communities, and Spaces.
  Publish tweets through OAuth relay — no passwords or cookies needed.
  Use when asked about Twitter/X data, social listening, influencer monitoring,
  trending topics, competitor intel, or posting to X.
license: Apache-2.0
compatibility: Requires curl or python3, and an AISA_API_KEY from aisa.one
metadata:
  author: aisa
  version: "1.0.0"
  tags: twitter, x, social-media, social-listening, monitoring, oauth, aisa
  homepage: https://aisa.one
  repository: https://github.com/AIsaONE/agent-skills
---

# Twitter Command Center

Twitter/X data access and automation for AI agents. Powered by AIsa.

One API key. Full Twitter intelligence. No scraping, no cookies, no proxies.

## Setup

```bash
export AISA_API_KEY="your-key"
```

Get a key at [aisa.one](https://aisa.one). Pay-as-you-go, ~$0.0004 per read query.

## Typical Workflow

1. User asks about Twitter data → skill activates
2. Agent picks the right endpoint from the reference table below
3. Agent runs `curl` or the bundled Python client
4. Agent presents structured results

## Read Operations

All read endpoints use `GET` with `Authorization: Bearer $AISA_API_KEY`.

### Users

```bash
# Profile
curl "https://api.aisa.one/apis/v1/twitter/user/info?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Recent tweets
curl "https://api.aisa.one/apis/v1/twitter/user/last_tweets?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Mentions
curl "https://api.aisa.one/apis/v1/twitter/user/mentions?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Followers
curl "https://api.aisa.one/apis/v1/twitter/user/followers?userName=elonmusk" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search users
curl "https://api.aisa.one/apis/v1/twitter/user/search?query=AI+researcher" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Check follow relationship
curl "https://api.aisa.one/apis/v1/twitter/user/check_follow_relationship?source_user_name=elonmusk&target_user_name=BillGates" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Tweets

```bash
# Search tweets (queryType is required: Latest or Top)
curl "https://api.aisa.one/apis/v1/twitter/tweet/advanced_search?query=AI+agents&queryType=Latest" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get tweet by ID
curl "https://api.aisa.one/apis/v1/twitter/tweets?tweet_ids=1895096451033985024" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Replies / quotes / retweeters / thread
curl "https://api.aisa.one/apis/v1/twitter/tweet/replies?tweetId=1895096451033985024" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Trends, Lists, Communities & Spaces

```bash
# Worldwide trends
curl "https://api.aisa.one/apis/v1/twitter/trends?woeid=1" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Community info
curl "https://api.aisa.one/apis/v1/twitter/community/info?community_id=1708485837274263614" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Space detail
curl "https://api.aisa.one/apis/v1/twitter/spaces/detail?space_id=1dRJZlbLkjexB" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## Posting (OAuth Relay)

No passwords or cookies. Uses AIsa's OAuth relay.

**Important:** Post endpoints use `aisa_api_key` in the JSON body, NOT the `Authorization` header.

```bash
# 1. Get authorization URL — user opens this in browser
curl -X POST "https://api.aisa.one/apis/v1/twitter/auth_twitter" \
  -H "Content-Type: application/json" \
  -d "{\"aisa_api_key\":\"$AISA_API_KEY\"}"

# 2. After user authorizes in browser, publish
curl -X POST "https://api.aisa.one/apis/v1/twitter/post_twitter" \
  -H "Content-Type: application/json" \
  -d "{\"aisa_api_key\":\"$AISA_API_KEY\",\"content\":\"Hello from my AI agent!\"}"
```

## Gotchas

- **queryType is required** for tweet search — must be `Latest` or `Top`. Omitting it returns an error.
- **Post endpoints use body auth**, not Bearer header. Send `aisa_api_key` in JSON body.
- **verifiedFollowers** requires `user_id` (numeric), not `userName`.
- **Do not claim a post succeeded** until `post_twitter` returns success.
- **Never ask for Twitter passwords** — only use the OAuth relay flow.
- Every response includes `usage.cost` and `usage.credits_remaining`.

## Python Client

A bundled client is available at `scripts/twitter_client.py`:

```bash
# User operations
python3 scripts/twitter_client.py user-info --username elonmusk
python3 scripts/twitter_client.py tweets --username elonmusk
python3 scripts/twitter_client.py search --query "AI agents"
python3 scripts/twitter_client.py trends --woeid 1

# Posting
python3 scripts/twitter_client.py authorize
python3 scripts/twitter_client.py post --text "Hello from my agent"
```

See [references/api-endpoints.md](references/api-endpoints.md) for the full endpoint reference with all parameters.
