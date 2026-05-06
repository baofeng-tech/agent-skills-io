# YouTube SERP 📺

Search YouTube SERP results through AIsa for video research, channel discovery, trend analysis, and competitor tracking.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- Search top-ranking YouTube videos for a query
- Filter results by country and interface language
- Research channels and competitor content
- Explore trending topics and search visibility

## Quick Start

```bash
export AISA_API_KEY="your-key"

# Basic search
python3 scripts/youtube_client.py search --query "AI agents tutorial"

# Search with country filter
python3 scripts/youtube_client.py search --query "machine learning" --country us

# Search with language filter
python3 scripts/youtube_client.py search --query "python tutorial" --lang en

# Combined country and language filters
python3 scripts/youtube_client.py search --query "GPT-5" --country us --lang en
```

## Use Cases

1. **Content Research** — Find what is ranking to inform content planning
2. **Competitor Tracking** — Monitor how competitors appear in YouTube search
3. **Trend Discovery** — Identify popular topics and search patterns
4. **Keyword Research** — Explore queries and ranking results in a niche
5. **Audience Research** — Compare results across countries and languages

## Documentation

See [SKILL.md](SKILL.md) for full usage details, API examples, and parameter reference.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
