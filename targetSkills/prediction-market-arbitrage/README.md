# AIsa Prediction Market Toolkit 📈⚖️

A toolkit for accessing prediction market data and finding cross-platform arbitrage opportunities with a unified AIsa API.

This skill directory is centered on matching and comparing markets across **Polymarket** and **Kalshi**, then checking whether a visible spread may be actionable after looking at liquidity.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and other harnesses that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Included files

### Skill
- `SKILL.md`: Cross-platform skill instructions for prediction-market arbitrage lookups.

### Scripts
- `scripts/prediction_market_client.py`: CLI and Python wrapper for Polymarket, Kalshi, and cross-platform market-matching endpoints.
- `scripts/arbitrage_finder.py`: CLI that scans matching markets, compares prices, calculates spreads, and checks liquidity.

## Setup

Both the skill and the Python scripts require an AIsa API key.

```bash
export AISA_API_KEY="your-key-here"
```

## Using the Python scripts

Run the scripts from the repository root with the `scripts/` path prefix.

### Prediction market client

```bash
# Search for open election markets
python scripts/prediction_market_client.py polymarket markets --search "election" --status open

# Get current price for a specific token
python scripts/prediction_market_client.py polymarket price <token_id>

# Get wallet portfolio and PnL
python scripts/prediction_market_client.py polymarket positions <wallet_address>
python scripts/prediction_market_client.py polymarket pnl <wallet_address> --granularity day

# Search for Fed rate markets
python scripts/prediction_market_client.py kalshi markets --search "fed rate" --status open

# Get orderbook for a market
python scripts/prediction_market_client.py kalshi orderbooks --ticker <ticker>
```

### Arbitrage finder

```bash
# Scan all NBA games on March 30, 2025, showing only spreads > 2% and liquidity > $500
python scripts/arbitrage_finder.py scan nba --date 2025-03-30 --min-spread 2.0 --min-liquidity 500

# Check a specific event using its Polymarket slug
python scripts/arbitrage_finder.py match --polymarket-slug nba-lakers-vs-celtics

# Or using its Kalshi ticker
python scripts/arbitrage_finder.py match --kalshi-ticker KXNBA-25-LAL-BOS
```

## Using the skill

Load `SKILL.md` into the agent context.

Important details:
- The cURL examples in `SKILL.md` use product placeholders such as `{token_id}` and `{market_ticker}` by design.
- Before executing any `curl` command, the runner must verify that every `{...}` placeholder has been replaced with a concrete value.
- If a final command still contains `{token_id}` or any other brace placeholder, do not execute it. Fail fast and report a missing-parameter error.

## ID lookup workflow

Most endpoints require IDs fetched from a markets endpoint first:

1. `token_id`: from `side_a.id` or `side_b.id` in `/polymarket/markets`
2. `condition_id`: from `condition_id` in `/polymarket/markets`
3. `market_ticker`: from `market_ticker` in `/kalshi/markets`

## Pricing

| API Operation | Cost |
|---------------|------|
| Prediction market read query | $0.01 |

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
