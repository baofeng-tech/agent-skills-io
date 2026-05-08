# AIsa Prediction Market Toolkit 📈⚖️

A toolkit for accessing prediction market data and analyzing cross-platform arbitrage opportunities with AIsa.

This skill directory provides documentation and examples for working with prediction markets such as **Polymarket** and **Kalshi** through a unified API surface.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and other tools that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Files

### Skill
- `SKILL.md`: The cross-platform skill definition for prediction-market arbitrage lookups.

## Setup

This skill requires an AIsa API key.

```bash
export AISA_API_KEY="your-key-here"
```

## Using the Skill

Load `SKILL.md` into the agent context.

Important details:
- The repository contains `SKILL.md`.
- The cURL examples in `SKILL.md` use product placeholders such as `{token_id}` and `{market_ticker}` by design.
- Before executing any `curl` command, the runner must verify that every `{...}` placeholder has been replaced with a concrete value.
- If a final command still contains `{token_id}` or any other brace placeholder, do not execute it. Fail fast and report a missing-parameter error.

## ID Lookup Workflow

Most endpoints require IDs fetched from a markets endpoint first:

1. `token_id`: from `side_a.id` or `side_b.id` in `/polymarket/markets`
2. `condition_id`: from `condition_id` in `/polymarket/markets`
3. `market_ticker`: from `market_ticker` in `/kalshi/markets`

## Pricing

| API Operation | Cost |
|---------------|------|
| Prediction market read query | $0.01 |

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
