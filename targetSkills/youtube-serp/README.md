# YouTube SERP 📺

Search ranked YouTube results through AIsa for content research, channel discovery, competitor tracking, and trend analysis.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **SERP Search**: Find top-ranking YouTube videos for a query
- **Country and Language Filters**: Target specific regions and interfaces
- **Competitor Research**: Inspect videos around brands, creators, or topics
- **Trend Discovery**: Check what is ranking for emerging subjects

## Quick Start

```bash
export AISA_API_KEY="your-key"

# Basic search
python3 scripts/youtube_client.py search --query "AI agents tutorial"

# Search with country filter
python3 scripts/youtube_client.py search --query "machine learning" --country us

# Search with language filter
python3 scripts/youtube_client.py search --query "python tutorial" --lang en

# Full options
python3 scripts/youtube_client.py search --query "GPT-5 news" --country us --lang en
```

## Typical use cases

1. **Content Research** - Find what is ranking to plan new content
2. **Competitor Tracking** - Review results around competitor brands or channels
3. **Trend Discovery** - Identify popular topics and result patterns
4. **Keyword Research** - Explore how topics perform across queries
5. **Audience Research** - Compare results by country and language

## Documentation

See [SKILL.md](SKILL.md) for full usage details, request parameters, and response examples.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the broader endpoint catalog.
