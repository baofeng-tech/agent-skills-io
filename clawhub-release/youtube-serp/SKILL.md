---
name: youtube-serp
description: Search YouTube SERP results through AIsa for video discovery, competitor research, trend monitoring, and regional content analysis. Use when you need ranked YouTube results, channels, and metadata for a query.
author: AIsa
version: 1.0.0
license: MIT
homepage: https://aisa.one
source: https://github.com/baofeng-tech/agent-skills-io/tree/main/targetSkills/youtube-serp
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: ▶️
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: ▶️
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# YouTube SERP 📺

Search YouTube SERP results through AIsa for ranked video discovery, channel research, trend monitoring, and regional analysis.

Use when you need to:
- find top-ranking YouTube videos for a topic
- monitor competitor or brand visibility in YouTube search
- compare results across countries or interface languages
- inspect titles, channels, views, and published dates for research workflows

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- and other tools that implement the [Agent Skills specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY` from [aisa.one](https://aisa.one).

## Example Requests

### Content research

```text
Find the top-ranking YouTube videos for "AI agents tutorial" and summarize the leading channels.
```

### Competitor tracking

```text
Search YouTube for "OpenAI tutorial" and list the highest-ranking videos and channels.
```

### Trend discovery

```text
What are the top YouTube results for "GPT-5" right now?
```

### Regional analysis

```text
Compare YouTube results for "machine learning" in the US and Japan.
```

## Quick Start

```bash
export AISA_API_KEY="your-key"
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

# Search in Japan with a Japanese interface
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&gl=jp&hl=ja" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Search with language filter

```bash
# English interface
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=python+tutorial&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Chinese interface
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=编程教程&hl=zh-CN&gl=cn" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Pagination or advanced filter token

```bash
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&sp=<filter_token>" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## Python Client

```bash
# Basic search
python3 scripts/youtube_client.py search --query "AI agents tutorial"

# Search with country filter
python3 scripts/youtube_client.py search --query "machine learning" --country us

# Search with language filter
python3 scripts/youtube_client.py search --query "python tutorial" --lang en

# Full options
python3 scripts/youtube_client.py search --query "GPT-5 news" --country us --lang en

# Competitor-style research
python3 scripts/youtube_client.py search --query "OpenAI tutorial"

# Trend discovery
python3 scripts/youtube_client.py search --query "AI trends 2025"
```

## Common Use Cases

### 1. Content gap analysis

Find what is already ranking in your niche to spot positioning gaps.

```python
results = client.search("AI automation tutorial")
# Analyze titles, views, and channels to identify opportunities
```

### 2. Competitor monitoring

Track how competitor-related topics appear in YouTube search.

```python
results = client.search("OpenAI GPT tutorial")
# Monitor ranking changes over time
```

### 3. Keyword research

Discover what topics and phrasing appear in top-ranked results.

```python
results = client.search("artificial intelligence 2025")
# Extract common keywords from top-ranking titles
```

### 4. Audience research

Inspect regional differences in visible content.

```python
results = client.search("coding tutorial", country="jp", lang="ja")
# Analyze regional content preferences
```

### 5. Search visibility analysis

Check which videos and channels rank for target keywords.

```python
keywords = ["AI tutorial", "machine learning basics", "Python AI"]
for kw in keywords:
    results = client.search(kw)
    # Record top results and channels
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
| gl | string | No | Country code such as `us`, `jp`, `uk`, `cn` |
| hl | string | No | Interface language such as `en`, `ja`, `zh-CN` |
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
4. Set `AISA_API_KEY`
5. Call the API directly with `curl` or use `scripts/youtube_client.py`

## Full API Reference

See [AIsa API Reference](https://aisa.one/docs/api-reference/) for broader endpoint documentation.
