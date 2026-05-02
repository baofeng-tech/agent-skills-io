# AISA API Regression Follow-up - 2026-05-03

## Scope

Follow-up to `targets/aisa-api-regression-report-2026-05-02.json` and the 54-skill AISA API regression where 72 read-only checks produced 17 failures.

This pass used `AIsa-team/agent-skills@main` as the read-only upstream runtime baseline and regenerated the local multi-platform release layers after source fixes.

## Why The Previous Run Failed

The failures were not one single deterministic regression.

- Most failures were external HTTPS/TLS instability to `api.aisa.one`.
  - Python `urllib` surfaced this as `[SSL: UNEXPECTED_EOF_WHILE_READING]`.
  - Node `fetch` surfaced this as `Client network socket disconnected before secure TLS connection was established`.
  - A direct unauthenticated `curl https://api.aisa.one/apis/v1` probe reproduced the same TLS EOF without using any skill code or API key: 6 of 10 attempts failed during TLS handshake, while successful attempts returned the expected unauthenticated `401`.
- The two old stock failures were a real local robustness issue:
  - `stock-dividend` and `stock-hot` asked the model to append a fenced JSON block.
  - The model sometimes returned a normal report without that block, so the old regex-only extractor raised `No JSON block found in model output`.
- The OpenAI SDK stock scripts could also emit `Connection error.` for the same transient network class, but the regression harness did not previously retry that marker.

## Upstream Execution-file Comparison

Fetched upstream into `refs/remotes/aisa/main` from:

- `https://github.com/AIsa-team/agent-skills.git`

Exact upstream skill-family execution files checked:

- `crypto-market-data/scripts/coingecko_client.py`
- `marketpulse/scripts/market_client.py`
- `multi-source-search/scripts/search_client.py`
- `prediction-market-arbitrage/scripts/arbitrage_finder.py`
- `prediction-market-arbitrage/scripts/prediction_market_client.py`
- `twitter-autopilot/scripts/twitter_client.py`
- `twitter-autopilot/scripts/twitter_engagement_client.py`
- `twitter-autopilot/scripts/twitter_oauth_client.py`
- `youtube-serp/scripts/youtube_client.py`

Result: all exact same upstream skill-family scripts matched the corresponding `targetSkills/` files byte-for-byte, so no upstream runtime restore was needed for those families.

Several local release-family variants, such as `market`, `smart-search`, `openclaw-twitter-post-engage`, `twitter`, `x-intelligence-automation`, and prediction-market API/ZH variants, do not have exact same-name upstream skill directories. They remain local adapted source variants; their remaining failures in this pass followed the same transient TLS/connection pattern rather than a stable script mismatch.

## Fixes Applied

- Hardened JSON mode in:
  - `targetSkills/stock-dividend/scripts/dividends.py`
  - `targetSkills/stock-hot/scripts/hot_scanner.py`
  - `targetSkills/stock-rumors/scripts/rumor_scanner.py`
- The stock JSON mode now requests pure JSON with `response_format={"type": "json_object"}` and uses the same balanced JSON extraction pattern already used by `stock-analysis`.
- Added `Connection error` and `APIConnectionError` to `scripts/test_aisa_api_skills.py` transient markers so OpenAI SDK connection drops get retried like TLS EOF failures.
- Rebuilt all generated platform layers from `targetSkills/`.

## Validation

- `python3 -m py_compile` passed for the modified stock scripts and regression script.
- Targeted stock regression:
  - `stock-dividend`, `stock-hot`, `stock-rumors`: 3 checks, 0 failures.
- Targeted SDK retry regression:
  - `stock-analysis`, `stock-rumors`: 2 checks, 0 failures; `stock-rumors` passed on retry.
- Release layer validation:
  - `python3 scripts/test_release_layers.py` passed.
- Full AISA API regression after fixes:
  - 54 AISA-backed skills
  - 72 read-only checks
  - 64 passed
  - 8 failed
  - 4 docs-only skills
  - Report: `targets/aisa-api-regression-report-2026-05-03.json`

## Remaining Failures

The remaining 8 failures are all classified as transient TLS/connection failures after 4 attempts:

- `aisa-tavily` extract
- `aisa-twitter-engagement-suite` engagement lookup
- `openclaw-twitter-post-engage` Twitter search
- `twitter` engagement lookup
- `twitter-autopilot` engagement lookup
- `twitter-command-center-search-post` Twitter search
- `twitter-command-center-search-post-interact` engagement lookup
- `youtube` search

These failures do not currently point to a local code mismatch. The same run fixed or moved many previous failures without runtime changes, and direct curl probes reproduce TLS EOF outside the skill layer.
