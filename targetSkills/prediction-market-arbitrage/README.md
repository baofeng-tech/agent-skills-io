# Prediction Market Arbitrage ⚖️

A neutral AIsa skill for finding and evaluating arbitrage opportunities across prediction markets such as Polymarket and Kalshi.

This directory focuses on the arbitrage workflow: matching equivalent markets, comparing cross-platform prices, and checking whether liquidity is sufficient to make a spread actionable.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and other implementations of the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Files

- `SKILL.md`: canonical skill definition and endpoint usage guide
- `scripts/`: local runtime helpers for prediction-market queries and arbitrage analysis, if included in this directory
- `references/`: supporting reference material, if included in this directory

## Setup

```bash
export AISA_API_KEY="your-key-here"
```

## Typical Workflow

1. Query markets or matching markets to identify the same event across platforms.
2. Extract the correct IDs from those responses.
3. Fetch market prices from each platform.
4. Check orderbook depth before treating a spread as actionable.

## ID Lookup Notes

Most downstream endpoints require IDs discovered from an earlier markets response:

1. `token_id`: from `side_a.id` or `side_b.id` in `/polymarket/markets`
2. `market_ticker`: from `market_ticker` in `/kalshi/markets`

## Important Placeholder Rule

The cURL examples in `SKILL.md` use product placeholders such as `{token_id}` and `{market_ticker}` by design.

Before executing any `curl` command:
- verify that every `{...}` placeholder has been replaced with a concrete value
- if a final command still contains brace placeholders, do not execute it
- fail fast and report a missing-parameter error instead

This avoids accidental `curl` globbing behavior on literal brace placeholders.

## Pricing

| API Operation | Cost |
|---------------|------|
| Prediction market read query | $0.01 |

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference/) for the complete endpoint catalog behind this skill.
