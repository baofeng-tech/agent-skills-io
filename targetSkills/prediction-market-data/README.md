# Prediction Market Data

Access current odds, prices, and market data from prediction markets such as Polymarket and Kalshi. This skill also supports historical orderbook data, candlestick data, trade history, wallet positions, wallet PnL, and cross-platform sports market matching.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible
harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**,
**Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and
others that implement the
[Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Use When

Use this skill when you need to:
- search Polymarket or Kalshi markets
- check live prices or implied probabilities
- inspect historical trades, orderbooks, or candlesticks
- review wallet activity, positions, or PnL
- compare matching sports markets across platforms

## Features

- **Polymarket**: search markets, live prices, trade history, orderbooks, candlesticks, wallet positions, wallet info, and PnL
- **Kalshi**: search markets, live prices, trade history, and orderbooks
- **Cross-platform**: match equivalent sports markets across Polymarket and Kalshi

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

Many price and history endpoints require an ID from a prior market search:

- **Polymarket `token_id`**: from `side_a.id` or `side_b.id` in the `/polymarket/markets` response
- **Polymarket `condition_id`**: from `condition_id` in the `/polymarket/markets` response
- **Kalshi `market_ticker`**: from `market_ticker` in the `/kalshi/markets` response

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the
complete catalog of endpoints this skill can call.
