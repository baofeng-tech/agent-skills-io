# MarketPulse (Equity Market Data) 📊

MarketPulse provides stock-focused financial data from AIsa for research, screening, and company analysis.

It covers prices, news, financial statements, financial metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, line-item search, and macro interest rates.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Use When

Use this skill when you need to:

- inspect historical or intraday stock prices
- pull company news and earnings-related context
- analyze financial statements, metrics, and analyst expectations
- review insider trades, institutional ownership, and SEC filings
- run stock screens or line-item queries across multiple tickers
- fetch macro interest-rate snapshots or history

## Features

- **Stock Prices**: Historical and intraday price data
- **Company News**: Recent news by ticker
- **Financial Statements**: Income statements, balance sheets, and cash flow
- **Segmented Revenues**: Revenue by segment and geography
- **Financial Metrics**: Snapshot and historical metrics
- **Analyst Estimates**: Earnings estimate data
- **Earnings Press Releases**: Earnings release retrieval
- **Insider Trading**: Insider transaction data
- **Institutional Ownership**: Holdings data by ticker or investor
- **SEC Filings**: Filings plus filing item extraction
- **Company Facts**: Company facts by ticker or CIK
- **Stock Screener**: Filter equities by financial criteria
- **Line-Item Search**: Query selected financial line items across tickers
- **Macro Interest Rates**: Snapshot and historical central-bank rate data

## Quick Start

```bash
export AISA_API_KEY="your-key"

# Stock prices
python3 scripts/market_client.py stock prices --ticker AAPL --start 2025-01-01 --end 2025-01-31

# Earnings press releases
python3 scripts/market_client.py stock earnings --ticker AAPL
```

## Notes

- The earnings press releases endpoint has narrower ticker coverage than the broader financial dataset.
- Unsupported earnings tickers return `{"error":"Invalid ticker"}`.
- See [earnings-press-releases-tickers.md](./earnings-press-releases-tickers.md) for the supported list referenced by the skill.

## Documentation

See [SKILL.md](SKILL.md) for complete usage examples, endpoint coverage, and command references.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
