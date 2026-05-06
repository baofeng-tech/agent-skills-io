# Prediction Market Arbitrage ⚖️

A neutral AIsa skill for finding and analyzing arbitrage opportunities across prediction markets such as **Polymarket** and **Kalshi**.

This directory is centered on cross-platform market matching, price comparison, and liquidity checks so agents can evaluate whether an apparent spread is actually tradable.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and other tools that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Files

- `SKILL.md`: Canonical skill definition for prediction-market arbitrage analysis.

## Setup

Set your AIsa API key before using the documented API calls:

```bash
export AISA_API_KEY="your-key-here"
```

## What This Skill Covers

- matching equivalent markets across platforms
- comparing prices between Polymarket and Kalshi
- checking orderbook liquidity before evaluating an arbitrage trade
- looking up the IDs needed for downstream price and orderbook endpoints

## Typical Workflow

1. Query a markets or matching-markets endpoint.
2. Extract the required identifier.
3. Fetch current prices from each platform.
4. Check orderbook depth to determine whether the spread is actionable.

## ID Lookup Workflow

Most downstream endpoints require IDs fetched from a markets endpoint first:

1. `token_id`: from `side_a.id` or `side_b.id` in `/polymarket/markets`
2. `market_ticker`: from `market_ticker` in `/kalshi/markets`

## Placeholder Safety

The cURL examples in `SKILL.md` use product placeholders such as `{token_id}` and `{market_ticker}` by design.

Before executing any `curl` command:
- verify that every `{...}` placeholder has been replaced with a concrete value
- if a final command still contains `{token_id}` or any other brace placeholder, do not execute it
- fail fast and report a missing-parameter error instead

This avoids accidental execution of literal brace placeholders, which `curl` may interpret as URL globbing syntax.

## Pricing

| API Operation | Cost |
|---------------|------|
| Prediction market read query | $0.01 |

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference/) for the complete catalog of endpoints this skill can call.
