# YouTube SERP 📺

Search YouTube result pages through AISA to find ranking videos, channels, and trends for content research, competitor tracking, and regional discovery.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **YouTube SERP search** for topic and keyword research
- **Country and language filters** for regional comparisons
- **Competitor research** using query-based discovery
- **Trend discovery** from current search rankings
- **Structured API output** for downstream analysis workflows

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

## Common Use Cases

1. **Content research** - Find what is ranking for a topic
2. **Competitor tracking** - Inspect search results around competitor topics or brands
3. **Trend discovery** - Check what is surfacing now for emerging queries
4. **Keyword research** - Compare result pages across search terms
5. **Regional analysis** - Review country and language differences

## Documentation

See [SKILL.md](SKILL.md) for full usage details, parameters, and response examples.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
