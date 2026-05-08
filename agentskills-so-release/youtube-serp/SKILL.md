---
name: youtube-serp
description: 'Search YouTube SERPs through AIsa to find top-ranking videos, channels, and localized results for content research, trend discovery, and competitor tracking. Use when: you need YouTube search rankings, regional filtering, or topic validation from an agent workflow.'
license: MIT
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries curl, python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.0
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills-so
  tags: youtube,search,research,video,aisa
  platforms: agentskills.io,agentskills.so,github
  primary_env: AISA_API_KEY
allowed-tools: Read Bash Grep
---

# YouTube SERP 📺

Search YouTube SERPs through AIsa for videos, channels, and localized ranking results.

Use this skill when you need to:
- research which videos rank for a topic
- compare competitor visibility on YouTube
- check region- or language-specific search results
- validate content ideas with current search demand

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

### Content Research
```text
Find top-ranking YouTube videos about "AI agents tutorial" to see what content is already winning.
```

### Competitor Tracking
```text
Search YouTube for videos about "machine learning" and help me spot likely competitor channels.
```

### Trend Discovery
```text
What are the top YouTube results for "GPT-5" right now?
```

### Topic Validation
```text
Find popular YouTube videos on "autonomous driving" so I can assess audience interest.
```

### Channel Discovery
```text
Search YouTube for channels creating content about "crypto trading".
```

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Core Capabilities

### Basic YouTube Search

```bash
# Search for videos
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+agents+tutorial" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Search with Country Filter

```bash
# Search in specific country (US)
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=machine+learning&gl=us" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search in Japan
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&gl=jp&hl=ja" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Search with Language Filter

```bash
# Search with interface language
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=python+tutorial&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Chinese interface
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=编程教程&hl=zh-CN&gl=cn" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Pagination with Filter Token

```bash
# Use sp parameter for pagination or advanced filters
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

# Competitor research
python3 scripts/youtube_client.py search --query "OpenAI tutorial"

# Trend discovery
python3 scripts/youtube_client.py search --query "AI trends 2025"
```

## Common Use Cases

### 1. Content Gap Analysis

Find what content is already ranking so you can identify gaps in your strategy:

```python
# Search for top videos in your niche
results = client.search("AI automation tutorial")
# Analyze titles, views, and channels to find opportunities
```

### 2. Competitor Monitoring

Track what adjacent or competing brands are publishing:

```python
# Search for competitor brand + topic
results = client.search("OpenAI GPT tutorial")
# Monitor ranking changes over time
```

### 3. Keyword Research

Discover which topics and phrases are surfacing in YouTube search:

```python
# Search broad topics to see what's popular
results = client.search("artificial intelligence 2025")
# Extract common keywords from top-ranking titles
```

### 4. Audience Research

Understand what audiences in different regions are watching:

```python
# Search in specific regions
results = client.search("coding tutorial", country="jp", lang="ja")
# Analyze regional content preferences
```

### 5. SEO Analysis

Review which videos rank for target keywords:

```python
# Track ranking positions for target keywords
keywords = ["AI tutorial", "machine learning basics", "Python AI"]
for kw in keywords:
    results = client.search(kw)
    # Record top 10 videos and their channels
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
| gl | string | No | Country code, such as `us`, `jp`, `uk`, `cn` |
| hl | string | No | Interface language, such as `en`, `ja`, `zh-CN` |
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
4. Set `AISA_API_KEY`, for example: `export AISA_API_KEY="your-key"`

## Full API Reference

See [API Reference](https://aisa.one/docs/api-reference/) for complete endpoint documentation.
