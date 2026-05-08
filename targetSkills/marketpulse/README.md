# MarketPulse (Equity Market Data) 📊

Query real-time and historical equity market data through AIsa, including prices, company news, financial statements, financial metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates.

Use this skill when you need broad stock research coverage from a single AIsa-powered market data skill.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and other tools that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Stock Prices**: Historical and intraday price series
- **Company News**: Latest news by ticker
- **Financial Statements**: Income statements, balance sheets, and cash flow statements
- **Segmented Revenues**: Revenue broken out by business segment and geography
- **Financial Metrics**: Snapshot and historical metrics
- **Analyst Estimates**: EPS forecast data
- **Earnings Press Releases**: Earnings release retrieval for supported tickers
- **Insider Trading**: Insider transaction history
- **Institutional Ownership**: Ownership data by ticker or investor
- **SEC Filings**: Filing retrieval plus filing item extraction
- **Company Facts**: Company fact data by ticker or CIK
- **Stock Screener**: Metric-based stock filtering
- **Line-Item Search**: Pull specific financial line items across multiple tickers
- **Macro Interest Rates**: Snapshot and historical central-bank rate data

## Quick Start

```bash
export AISA_API_KEY="your-key"

# Stock prices
python3 scripts/market_client.py stock prices --ticker AAPL --start 2025-01-01 --end 2025-01-31

# Earnings press releases
python3 scripts/market_client.py stock earnings --ticker AAPL
```

## Documentation

See [SKILL.md](SKILL.md) for the full skill guide, curl examples, Python client commands, endpoint coverage, and pricing notes.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
