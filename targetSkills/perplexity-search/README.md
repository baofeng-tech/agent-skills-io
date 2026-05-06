# perplexity-search

Perplexity Sonar search and answer generation through AIsa. Use when the task is specifically to call Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, or Sonar Deep Research for citation-backed web answers, analytical reasoning, or long-form research reports.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and other tools that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## What this skill covers

This skill provides access to these AIsa Perplexity endpoints:

- `/perplexity/sonar`
- `/perplexity/sonar-pro`
- `/perplexity/sonar-reasoning-pro`
- `/perplexity/sonar-deep-research`

See [SKILL.md](SKILL.md) for the full agent-facing instructions, including model selection, Python client usage, curl examples, and timeout guidance.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
