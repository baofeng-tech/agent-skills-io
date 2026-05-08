# Prediction Market Data

Access current odds, prices, and market data from prediction markets such as Polymarket and Kalshi. This skill supports market search, live pricing, historical orderbooks, candlestick data, trade history, wallet activity, positions, P&L, and cross-platform sports market matching.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Polymarket**: search markets, get live prices, review trade history, inspect orderbooks, retrieve candlesticks, and check wallet positions and P&L
- **Kalshi**: search markets, get live prices, review trade history, and inspect orderbooks
- **Cross-platform sports matching**: find equivalent sports markets across Polymarket and Kalshi

## Quick Start

```bash
export AISA_API_KEY="your-key"

# Search Polymarket for election markets
python scripts/prediction_market_client.py polymarket markets --search "election" --status open

# Get current price for a Polymarket token
python scripts/prediction_market_client.py polymarket price <token_id>

# Search Kalshi for Fed rate markets
python scripts/prediction_market_client.py kalshi markets --search "fed rate"

# Get current price for a Kalshi market
python scripts/prediction_market_client.py kalshi price <market_ticker>

# Find matching NBA markets across platforms
python scripts/prediction_market_client.py sports by-date nba --date 2025-03-01
```

## ID Lookup Notes

Some downstream queries require IDs returned by market listing endpoints.

- For **Polymarket price** queries, first call `polymarket markets` and use `side_a.id` or `side_b.id` as the `token_id`.
- For **Polymarket candlesticks**, first call `polymarket markets` and use the returned `condition_id`.
- For **Kalshi price** queries, first call `kalshi markets` and use the returned `market_ticker`.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
