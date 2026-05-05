---
name: youtube-serp
description: 'Search YouTube result pages through AISA to find ranking videos, channels, and trends for content research, competitor tracking, and regional discovery. Use when: you need YouTube SERP data for a topic, market, or channel niche.'
license: MIT
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries curl, python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.0
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills
  tags: youtube,search,research,market,video,aisa
  platforms: agentskills.io,agentskill.sh,github
  primary_env: AISA_API_KEY
allowed-tools: Read Bash Grep
---

# YouTube SERP 📺

Search YouTube result pages through AISA for content research, competitor tracking, topic discovery, and regional comparisons.

Use when:
- you want the top YouTube results for a query
- you need to compare results across countries or interface languages
- you are researching competitor coverage or creator niches
- you want structured YouTube SERP data for downstream analysis

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- and any other harness that implements the [Agent Skills specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY` from [aisa.one](https://aisa.one).

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Example Requests

### Content research

```text
Find top-ranking YouTube videos about "AI agents tutorial".
```

### Competitor tracking

```text
Search YouTube results for videos about "machine learning" from competitor channels.
```

### Trend discovery

```text
What are the top YouTube results for "GPT-5" right now?
```

### Channel discovery

```text
Find YouTube channels creating content about "crypto trading".
```

## Core Capabilities

### Basic YouTube search

```bash
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+agents+tutorial" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Search with country filter

```bash
# Search in the United States
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=machine+learning&gl=us" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search in Japan
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&gl=jp&hl=ja" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Search with language filter

```bash
# Search with English interface language
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=python+tutorial&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search with Simplified Chinese interface language
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=编程教程&hl=zh-CN&gl=cn" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Pagination or advanced filters with `sp`

```bash
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&sp=<filter_token>" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## Python Client

```bash
# Basic search
python3 scripts/youtube_client.py search --query "AI agents tutorial"

# Search with country
python3 scripts/youtube_client.py search --query "machine learning" --country us

# Search with language
python3 scripts/youtube_client.py search --query "python tutorial" --lang en

# Full options
python3 scripts/youtube_client.py search --query "GPT-5 news" --country us --lang en

# Competitor-oriented research query
python3 scripts/youtube_client.py search --query "OpenAI tutorial"

# Trend discovery query
python3 scripts/youtube_client.py search --query "AI trends 2025"
```

## Common Use Cases

### 1. Content gap analysis

Find what content is ranking well to identify gaps in your strategy:

```python
# Search for top videos in your niche
results = client.search("AI automation tutorial")
# Analyze titles, views, and channels to find opportunities
```

### 2. Competitor monitoring

Track what competitors are publishing:

```python
# Search for competitor brand + topic
results = client.search("OpenAI GPT tutorial")
# Monitor ranking changes over time
```

### 3. Keyword research

Discover what topics are popular in search results:

```python
# Search broad topics to see what's popular
results = client.search("artificial intelligence 2025")
# Extract common keywords from top-ranking titles
```

### 4. Audience research

Understand what your target audience watches in different regions:

```python
# Search in specific regions
results = client.search("coding tutorial", country="jp", lang="ja")
# Analyze regional content preferences
```

### 5. SERP tracking

Analyze how videos rank for specific keywords:

```python
# Track ranking positions for target keywords
keywords = ["AI tutorial", "machine learning basics", "Python AI"]
for kw in keywords:
    results = client.search(kw)
    # Record top results and their channels
```

## API Endpoint Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/youtube/search` | GET | Search YouTube SERP |

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| engine | string | Yes | Must be `youtube` |
| q | string | Yes | Search query |
| gl | string | No | Country code, such as `us`, `jp`, `uk`, or `cn` |
| hl | string | No | Interface language, such as `en`, `ja`, or `zh-CN` |
| sp | string | No | YouTube filter token for pagination or filters |

## Response Format

```json
{
  "search_metadata": {
    "id": "search_id",
    "status": "Success",
    "created_at": "2025-01-15T12:00:00Z",
    "request_time_taken": 1.23,
    "total_time_taken": 1.45
  },
  "search_results": [
    {
      "video_id": "abc123xyz",
      "title": "Complete AI Agents Tutorial 2025",
      "link": "https://www.youtube.com/watch?v=abc123xyz",
      "channel_name": "AI Academy",
      "channel_link": "https://www.youtube.com/@aiacademy",
      "description": "Learn how to build AI agents from scratch...",
      "views": "125K views",
      "published_date": "2 weeks ago",
      "duration": "45:30",
      "thumbnail": "https://i.ytimg.com/vi/abc123xyz/hqdefault.jpg"
    }
  ]
}
```

## Country Codes (`gl`)

| Code | Country |
|------|---------|
| us | United States |
| uk | United Kingdom |
| jp | Japan |
| cn | China |
| de | Germany |
| fr | France |
| kr | South Korea |
| in | India |
| br | Brazil |
| au | Australia |

## Language Codes (`hl`)

| Code | Language |
|------|----------|
| en | English |
| ja | Japanese |
| zh-CN | Chinese (Simplified) |
| zh-TW | Chinese (Traditional) |
| ko | Korean |
| de | German |
| fr | French |
| es | Spanish |
| pt | Portuguese |
| ru | Russian |

## Pricing

| API | Cost |
|-----|------|
| YouTube search | ~$0.002 |

## Get Started

1. Sign up at [aisa.one](https://aisa.one)
2. Get your API key
3. Add credits if needed
4. Set `AISA_API_KEY` in your shell

## Full API Reference

See [API Reference](https://aisa.one/docs/api-reference/) for complete endpoint documentation.
