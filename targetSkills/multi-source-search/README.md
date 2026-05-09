# Multi-source Search

Multi-source search for autonomous agents with structured retrieval, Tavily utilities, and Perplexity Sonar answer endpoints.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## What it covers

- Web search
- Scholar search
- Hybrid scholar search
- Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, and Sonar Deep Research
- Tavily integration
- Verity-style multi-source retrieval

## Quick Start

```bash
export AISA_API_KEY="your-key"

python3 scripts/search_client.py web --query "AI frameworks"
python3 scripts/search_client.py scholar --query "transformer models"
python3 scripts/search_client.py sonar --query "What changed in AI this week?"
python3 scripts/search_client.py sonar-pro --query "Compare coding agents with citations"
python3 scripts/search_client.py verity --query "Is quantum computing enterprise-ready?"
```

## Notes

- Deprecated `/search/full` and `/search/smart` nodes were removed from this skill.
- Perplexity endpoints are now the recommended answer-generation path.

## Documentation

See [SKILL.md](SKILL.md) for full usage, API examples, and endpoint details.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
