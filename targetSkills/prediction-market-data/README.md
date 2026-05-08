# Prediction Market Data

Get current odds, prices, and market data from prediction markets such as Polymarket and Kalshi. This skill also supports historical orderbook data, candlestick charts, trade history, Polymarket wallet activity, positions, P&L, and cross-platform sports market matching.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible
harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**,
**Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and
others that implement the
[Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Polymarket**: Search markets, get live prices, inspect trade history, orderbooks, candlesticks, wallet positions, wallet details, and P&L
- **Kalshi**: Search markets, get live prices, inspect trade history, and orderbooks
- **Cross-platform sports matching**: Find equivalent sports markets across Polymarket and Kalshi

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

Many downstream endpoints require an identifier returned by a market search first:

- **Polymarket `token_id`**: returned as `side_a.id` or `side_b.id`
- **Polymarket `condition_id`**: returned on each market object
- **Kalshi `market_ticker`**: returned on each Kalshi market object

A common workflow is to query `markets` first, then use the returned ID in a `price`, `orderbooks`, or `candlesticks` request.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the
complete catalog of endpoints this skill can call.
