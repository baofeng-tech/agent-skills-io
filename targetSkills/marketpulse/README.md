# MarketPulse (Equity Market Data) 📊

Query real-time and historical equity market data—prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates.

## Use when

- You need broad public-market data from a single skill.
- You want price history, company news, or filing history for a ticker.
- You need financial statements, metrics, analyst estimates, or revenue segmentation.
- You want to review insider trades or institutional ownership.
- You need stock screening, line-item comparison, or macro interest-rate context.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Stock Prices**: Historical and intraday price data
- **Company News**: Latest news by ticker
- **Financial Statements**: Income statements, balance sheets, and cash flow statements
- **Segmented Revenues**: Revenue by business segment and geography
- **Financial Metrics**: Snapshot and historical metrics
- **Analyst Estimates**: Earnings-per-share estimate data
- **Earnings Press Releases**: Quarterly earnings release coverage
- **Insider Trading**: Insider transaction data
- **Institutional Ownership**: Holdings and ownership data
- **SEC Filings**: Filing history plus filing item extraction
- **Company Facts**: Company facts by ticker or CIK
- **Stock Screener**: Filter stocks by financial criteria
- **Line-Item Search**: Pull specific financial line items across tickers
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

See [SKILL.md](SKILL.md) for the full command surface, curl examples, endpoint list, and pricing notes.

## API Reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
