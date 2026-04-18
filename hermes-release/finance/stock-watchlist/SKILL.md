---
name: stock-watchlist
description: Manage a stock/crypto watchlist with price target and stop-loss alerts via AIsa API. Add, remove, list, and check tickers with live price alerts. Use when the user wants to track stocks, set price alerts, manage a watchlist, or check triggered alerts.
metadata:
  hermes:
    tags:
    - finance
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

# Watchlist Management — AIsa Edition

Manage a watchlist with price target and stop-loss alerts using the AIsa API.

## Usage

```bash
# Add a ticker with price target and stop-loss
python3 scripts/watchlist.py add AAPL --target 220 --stop 160

# Add with signal-change alert
python3 scripts/watchlist.py add AAPL --alert-on signal

# List all watchlist items
python3 scripts/watchlist.py list

# Check live prices and trigger alerts
python3 scripts/watchlist.py check

# Check with notification
python3 scripts/watchlist.py check --notify

# Remove a ticker
python3 scripts/watchlist.py remove AAPL
```

### Actions

| Action | Description |
|--------|-------------|
| `add TICKER` | Add ticker with optional `--target`, `--stop`, `--alert-on signal` |
| `remove TICKER` | Remove ticker from watchlist |
| `list` | Show all watchlist items |
| `check` | Fetch live prices and check alerts |

## Data Storage

Watchlist data is stored in `./.claude-skill-data/watchlist.json` for persistence across sessions.

**NOT FINANCIAL ADVICE.** For informational purposes only.

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow is stateful, re-run a read/list/status command to verify the new state.
