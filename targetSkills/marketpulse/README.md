# MarketPulse (Equity Market Data) 📊

Query real-time and historical equity market data including prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Use when

- you need price history or company news for a public stock
- you want financial statements, metrics, or analyst estimates for research
- you want SEC filings, insider trades, or institutional ownership data
- you want to screen stocks or compare line items across tickers
- you need macro interest-rate context alongside equity analysis

## Features

- **Stock Data**: Historical prices and interval-based market data
- **Company News**: Latest news by ticker
- **Financial Statements**: Income statements, balance sheets, and cash flow
- **Segmented Revenues**: Revenue by segment and geography
- **Financial Metrics**: Snapshot and historical metrics
- **Analyst Estimates**: EPS forecast data
- **Earnings Press Releases**: Quarterly earnings releases
- **Insider Trading**: Insider transaction data
- **Institutional Ownership**: Holdings data by ticker or investor
- **SEC Filings**: 10-K, 10-Q, 8-K, and filing item extraction
- **Stock Screener**: Filter stocks by financial criteria
- **Line-Item Search**: Pull selected financial line items across multiple tickers
- **Macro Interest Rates**: Snapshot and historical central-bank rates

## Quick start

```bash
export AISA_API_KEY="your-key"

# Stock prices
python3 scripts/market_client.py stock prices --ticker AAPL --start 2025-01-01 --end 2025-01-31

# Earnings press releases
python3 scripts/market_client.py stock earnings --ticker AAPL
```

## Documentation

See [SKILL.md](SKILL.md) for full usage, curl examples, and endpoint coverage.

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
