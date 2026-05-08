# YouTube SERP 📺

Search YouTube SERPs through AIsa for top-ranking videos, channels, and localized results.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **YouTube SERP Search**: Find top-ranking results for any query
- **Country and Language Filters**: Check regionalized search output
- **Competitor Research**: Review visible channels and topics in search results
- **Trend Discovery**: See what topics and videos are surfacing now

## Quick Start

```bash
export AISA_API_KEY="your-key"

# Basic search
python3 scripts/youtube_client.py search --query "AI agents tutorial"

# Search with country filter
python3 scripts/youtube_client.py search --query "machine learning" --country us

# Search with language filter
python3 scripts/youtube_client.py search --query "python tutorial" --lang en

# Combined filters
python3 scripts/youtube_client.py search --query "GPT-5 news" --country us --lang en
```

## Common Use Cases

1. **Content Research** - Find what is ranking for a topic
2. **Competitor Tracking** - Review search-visible videos and channels in your space
3. **Trend Discovery** - Identify currently surfacing topics
4. **Keyword Research** - Discover popular search phrasing
5. **Audience Research** - Compare regional preferences with `gl` and `hl`

## Documentation

See [SKILL.md](SKILL.md) for usage details, API examples, parameters, and response format.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
