# MarketPulse (Equity Market Data) 📊

Query real-time and historical equity market data, including prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates.

Use this skill when you need broad stock research coverage from one AIsa-backed surface.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Stock Prices**: Historical price series across multiple intervals
- **Company News**: Recent news by ticker
- **Financial Statements**: Income statements, balance sheets, and cash flow
- **Segmented Revenues**: Revenue by business segment and geography
- **Financial Metrics**: Snapshot and historical metrics
- **Analyst Estimates**: EPS estimate data
- **Earnings Press Releases**: Company earnings release coverage
- **Insider Trading**: Insider transaction data
- **Institutional Ownership**: Institutional holdings data
- **SEC Filings**: Filing history plus filing item extraction
- **Stock Screener**: Filter equities by financial criteria
- **Line-Item Search**: Query specific financial line items across tickers
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

See [SKILL.md](SKILL.md) for full usage details, curl examples, and endpoint coverage.

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
