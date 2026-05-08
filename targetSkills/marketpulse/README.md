# MarketPulse (Equity Market Data) 📊

Query real-time and historical equity market data through AIsa, including prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates.

## Use when

Use this skill when you need:

- stock price history or intraday market data
- company news and event context
- financial statements and fundamentals
- analyst estimates and financial metrics
- insider or institutional activity
- SEC filings and filing item extraction
- screening across multiple equities
- macro interest-rate context for market analysis

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Features

- **Stock Data**: Historical prices and interval-based market data
- **Company News**: Latest news by ticker
- **Financial Statements**: Income statements, balance sheets, and cash flow statements
- **Segmented Revenues**: Revenue broken out by segment and geography
- **Financial Metrics**: Snapshot and historical company metrics
- **Analyst Estimates**: EPS forecast data
- **Earnings Press Releases**: Quarterly earnings releases
- **Insider Trading**: Insider transaction tracking
- **Institutional Ownership**: Institutional holdings data
- **SEC Filings**: 10-K, 10-Q, 8-K, and more, plus filing item extraction
- **Stock Screener**: Filter equities by financial criteria
- **Line-Item Search**: Pull specific line items across multiple tickers
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

See [SKILL.md](SKILL.md) for the full usage guide, endpoint examples, and command reference.

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill can call.
