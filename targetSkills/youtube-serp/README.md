# YouTube SERP 📺

Search ranked YouTube results through AISA for content research, channel discovery, trend checking, and competitor tracking.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and other tools that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **YouTube SERP Search**: Find ranked videos for any query
- **Country and Language Filters**: Narrow results by region or interface language
- **Content Research**: Inspect what is ranking for a topic
- **Competitor Tracking**: Search branded or channel-adjacent queries
- **Trend Discovery**: Check what is surfacing for emerging topics

## Quick start

```bash
export AISA_API_KEY="your-key"

# Basic search
python3 scripts/youtube_client.py search --query "AI agents tutorial"

# Search with country filter
python3 scripts/youtube_client.py search --query "machine learning" --country us

# Search with language filter
python3 scripts/youtube_client.py search --query "python tutorial" --lang en

# Full options
python3 scripts/youtube_client.py search --query "GPT-5" --country us --lang en
```

## Use cases

1. **Content Research** - Find what is ranking for a topic
2. **Competitor Tracking** - Search branded queries and monitor results
3. **Trend Discovery** - Check emerging topics on YouTube
4. **Keyword Research** - Explore which queries surface which videos
5. **Audience Research** - Compare regional or language-specific results

## Documentation

See [SKILL.md](SKILL.md) for endpoint details, parameters, and example requests.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
