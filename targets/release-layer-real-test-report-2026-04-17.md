# Release Layer Real Test Report

Date:

- 2026-04-17

Credential source:

- [example/accounts](/mnt/d/workplace/agent-skills-io/example/accounts:1)

Python used for real runtime validation:

- `/usr/local/python3.12/bin/python3.12`

Tested release layers:

- [claude-release](</mnt/d/workplace/agent-skills-io/claude-release>)
- [hermes-release](</mnt/d/workplace/agent-skills-io/hermes-release>)

## 1. Full-Test Definition

This report treats "full testing" as:

1. all generated skills pass structure validation
2. real-data smoke tests are run against representative unique implementations
3. high-risk write flows are tested separately with real credentials

Why:

- many of the 51 skills are wrappers around the same runtime implementation
- structure still needs to be checked for every generated skill
- runtime should be tested against each unique implementation family, not just every directory name

## 2. Structure Validation

Result:

- Claude release structure errors: `0`
- Hermes release structure errors: `0`

Reference JSON:

- [targets/release-layer-test-report-2026-04-17.json](/mnt/d/workplace/agent-skills-io/targets/release-layer-test-report-2026-04-17.json:1)

## 3. Real Runtime Tests

### A. Claude Twitter search

Command:

```bash
cd claude-release/aisa-twitter-command-center
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/twitter_client.py search --query OpenAI --type Latest
```

Result:

- PASS

Observed output:

- returned real tweet search results
- sample tweet ids included fresh 2026-04-17 timeline data

### B. Hermes Twitter search

Command:

```bash
cd hermes-release/communication/aisa-twitter-command-center
AISA_API_KEY=... ../../../.tmp-py312-release/bin/python scripts/twitter_client.py search --query OpenAI --type Latest
```

Result:

- PASS

Observed output:

- returned real X/Twitter results from the Hermes-oriented package path

### C. Claude YouTube search

Command:

```bash
cd claude-release/aisa-youtube-serp-scout
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/youtube_client.py search --query OpenAI
```

Result:

- PASS

Observed output:

- returned real YouTube channel/search data
- `OpenAI` channel appeared in results

### D. Claude search aggregation

Command:

```bash
cd claude-release/search
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/search_client.py web --query "OpenAI latest" --count 1
```

Result:

- PASS

Observed output:

- returned `https://openai.com/news/`

### E. Claude prediction market

Command:

```bash
cd claude-release/prediction-market
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/prediction_market_client.py polymarket markets --limit 1
```

Result:

- PASS

Observed output:

- returned a live Polymarket market entry with slug, condition id, volume, and pagination

### F. Claude LLM router

Command:

```bash
cd claude-release/llm-router
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/llm_router_client.py models
```

Result:

- PASS

Observed output:

- returned live provider/model lists for OpenAI, Anthropic, Google, Alibaba, and others

### G. Claude last30days provider test

Command:

```bash
cd claude-release/last30days
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/test-aisa-provider.py
```

Result:

- PASS

Observed output:

- returned `{"ok": true, "provider": "aisa"}`

### H. Claude last30days-zh provider test

Command:

```bash
cd claude-release/last30days-zh
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/test-aisa-provider.py
```

Result:

- PASS

Observed output:

- returned `{"ok": true, "provider": "aisa"}`

### I. Claude stock-watchlist

Command:

```bash
cd claude-release/stock-watchlist
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/watchlist.py list
```

Result:

- PASS

Observed output:

- real CLI executed successfully
- current state: empty watchlist

### J. Claude stock-portfolio stateful test

Commands:

```bash
cd claude-release/stock-portfolio
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/portfolio.py create "Release Test Portfolio"
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/portfolio.py list
```

Result:

- PASS

Observed output:

- created `Release Test Portfolio`
- follow-up list showed the new portfolio as active

### K. Claude Twitter OAuth authorize

Command:

```bash
cd claude-release/aisa-twitter-command-center
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/twitter_oauth_client.py authorize
```

Result:

- PASS

Observed output:

- returned a real `authorization_url`
- proves the write flow can still initiate a valid X/Twitter OAuth handshake

### L. Claude Twitter real write

Command:

```bash
cd claude-release/aisa-twitter-command-center
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/twitter_oauth_client.py post --text "AIsa Claude/Hermes release real-write validation 2026-04-17 21:00 CST"
```

Result:

- PASS

Observed output:

- `tweet_id: 2045136296637771853`
- publish timestamp returned from the API

### M. Stock-analysis

Claude command:

```bash
cd claude-release/stock-analysis
AISA_API_KEY=... ../../.tmp-py312-release/bin/python scripts/analyze_stock.py AAPL --fast --output json
```

Result:

- PASS

Observed output:

- returned valid JSON against live upstream output
- sample fields included `ticker`, `score`, `signal`, `confidence`, `price`, `target`, `stop`, `risk_flags`, and `summary`

Hermes command:

```bash
cd hermes-release/finance/stock-analysis
AISA_API_KEY=... ../../../.tmp-py312-release/bin/python scripts/analyze_stock.py AAPL --fast --output json
```

Result:

- PASS

Observed output:

- returned valid JSON from the Hermes-oriented package path
- same live AAPL analysis contract succeeded after release-layer regeneration

## 4. Real-Test Summary

Confirmed real-data PASS cases:

- Twitter search
- Twitter OAuth authorize
- Twitter real write
- YouTube search
- Search aggregation
- Prediction market
- LLM router model listing
- `last30days`
- `last30days-zh`
- `stock-watchlist`
- `stock-portfolio`
- `stock-analysis`

Remaining real-data issue:

- no currently confirmed live failure remains in the representative set covered by this report

## 5. Notes

- Earlier failures seen under Python 3.8/3.9 for `stock-portfolio` were environment-related, not packaging-related.
- Python 3.12 materially improved the realism of the release-layer validation.
- `stock-analysis` was stabilized by tightening the JSON-only prompt contract and making the parser tolerant of fenced or bare JSON objects from live model output.
- The JSON summary file remains useful for machine-readable status; this Markdown report is the human-readable companion.
