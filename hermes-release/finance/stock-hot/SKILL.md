---
name: stock-hot
description: Hot Scanner — find the most trending and high-momentum stocks and crypto right now via AIsa API. Top gainers, losers, most active by volume, crypto highlights, news catalysts, and top 5 watchlist picks. Use when the user asks about trending stocks, what's hot, market movers, or momentum plays.
metadata:
  hermes:
    tags:
    - finance
    - market
    - stock
    - aisa
    related_skills:
    - market
    - prediction-market
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# Hot Scanner — AIsa Edition

Scan for the most trending and high-momentum stocks and cryptocurrencies using the AIsa API.

## Usage

```bash
python3 scripts/hot_scanner.py
python3 scripts/hot_scanner.py --focus stocks
python3 scripts/hot_scanner.py --focus crypto
python3 scripts/hot_scanner.py --output json
```

### Arguments

- `--focus`: Filter by `stocks`, `crypto`, or `both` (default)
- `--output json`: Append structured JSON summary

## Output Sections

- **Top Stock Movers**: Gainers (>3%), losers, most active by volume
- **Crypto Highlights**: BTC price, dominance, trending coins, gainers/losers
- **News-Driven Movers**: 5-8 items with ticker mentions from last 6 hours
- **Top 5 Watchlist Picks**: With risk level assessment
- **Quick Take**: 2-3 sentence market summary

**NOT FINANCIAL ADVICE.** For informational purposes only.

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow is stateful, re-run a read/list/status command to verify the new state.
