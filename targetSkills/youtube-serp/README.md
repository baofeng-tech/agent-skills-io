# YouTube SERP 📺

Search YouTube SERP results through AIsa for ranked video discovery, competitor research, trend monitoring, and regional content analysis.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **YouTube SERP Search**: Find top-ranking videos for a query
- **Country and Language Filters**: Compare results across regions and interfaces
- **Competitor Research**: Inspect videos and channels appearing for brand or topic searches
- **Trend Discovery**: Review what is ranking now for emerging topics

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

## Typical Uses

1. **Content Research** - See what videos and channels rank for a topic
2. **Competitor Tracking** - Monitor search visibility around competitor names or themes
3. **Trend Discovery** - Review current YouTube search results for fast-moving topics
4. **Keyword Research** - Inspect titles and channels across top results
5. **Regional Analysis** - Compare result differences by country and language

## Documentation

See [SKILL.md](SKILL.md) for full usage and parameter details.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for broader endpoint documentation.
