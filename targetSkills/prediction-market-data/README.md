# Prediction Market Data

Access current odds, prices, and market data from prediction markets such
as Polymarket and Kalshi. This skill supports market search, price
lookups, historical orderbooks, candlestick data, trade history, wallet
positions, PnL, and sports market matching across platforms.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible
harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**,
**Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and
others that implement the
[Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Polymarket**: Search markets, fetch live prices, inspect trade
  history, orderbooks, candlesticks, wallet positions, and PnL
- **Kalshi**: Search markets, fetch live prices, inspect trade history,
  and orderbooks
- **Cross-platform**: Match equivalent sports markets across Polymarket
  and Kalshi

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

Most price and history endpoints require IDs returned by a market search.
In practice:

- use `side_a.id` or `side_b.id` from Polymarket market results as the
  `token_id`
- use `condition_id` from Polymarket market results for candlesticks
- use `market_ticker` from Kalshi market results for Kalshi price and
  history endpoints

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the
complete catalog of endpoints this skill can call.
