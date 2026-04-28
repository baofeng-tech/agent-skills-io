# ClawHub Plugin Release

ClawHub native-first plugin packaging layer generated from `clawhub-release/`.

## Purpose

- Wrap every packaged AIsa skill as an installable ClawHub/OpenClaw plugin.
- Prefer the OpenClaw native manifest path while keeping Claude-compatible bundle metadata for cross-marketplace reuse.
- Produce ready-to-publish directories plus root-flat zip artifacts.

## Layout

- `plugins/<skill>-plugin/`: publishable plugin directory
- `zips/<skill>-plugin.zip`: root-flat upload/archive artifact

## Publish Loop

```bash
for dir in clawhub-plugin-release/plugins/*; do
  [ -d "$dir" ] || continue
  clawhub package publish "$dir" --dry-run
done
```

## Generated Plugins

- `aisa-multi-search-engine-plugin` → `aisa-multi-search-engine`
- `aisa-provider-plugin` → `aisa-provider`
- `aisa-tavily-plugin` → `aisa-tavily`
- `aisa-twitter-api-plugin` → `aisa-twitter-api`
- `aisa-twitter-api-command-center-plugin` → `aisa-twitter-api-command-center`
- `aisa-twitter-command-center-plugin` → `aisa-twitter-command-center`
- `aisa-twitter-engagement-suite-plugin` → `aisa-twitter-engagement-suite`
- `aisa-twitter-post-engage-plugin` → `aisa-twitter-post-engage`
- `aisa-twitter-research-engage-relay-plugin` → `aisa-twitter-research-engage-relay`
- `aisa-youtube-search-plugin` → `aisa-youtube-search`
- `aisa-youtube-serp-scout-plugin` → `aisa-youtube-serp-scout`
- `cn-llm-plugin` → `cn-llm`
- `crypto-market-data-plugin` → `crypto-market-data`
- `last30days-plugin` → `last30days`
- `last30days-zh-plugin` → `last30days-zh`
- `llm-router-plugin` → `llm-router`
- `market-plugin` → `market`
- `marketpulse-plugin` → `marketpulse`
- `media-gen-plugin` → `media-gen`
- `multi-search-plugin` → `multi-search`
- `multi-source-search-plugin` → `multi-source-search`
- `openclaw-aisa-youtube-aisa-plugin` → `openclaw-aisa-youtube-aisa`
- `openclaw-media-gen-plugin` → `openclaw-media-gen`
- `openclaw-search-plugin` → `openclaw-search`
- `openclaw-twitter-plugin` → `openclaw-twitter`
- `openclaw-twitter-post-engage-plugin` → `openclaw-twitter-post-engage`
- `openclaw-youtube-plugin` → `openclaw-youtube`
- `perplexity-research-plugin` → `perplexity-research`
- `perplexity-search-plugin` → `perplexity-search`
- `prediction-market-plugin` → `prediction-market`
- `prediction-market-arbitrage-plugin` → `prediction-market-arbitrage`
- `prediction-market-arbitrage-api-plugin` → `prediction-market-arbitrage-api`
- `prediction-market-arbitrage-zh-plugin` → `prediction-market-arbitrage-zh`
- `prediction-market-data-plugin` → `prediction-market-data`
- `prediction-market-data-zh-plugin` → `prediction-market-data-zh`
- `scholar-search-plugin` → `scholar-search`
- `search-plugin` → `search`
- `smart-search-plugin` → `smart-search`
- `stock-analysis-plugin` → `stock-analysis`
- `stock-dividend-plugin` → `stock-dividend`
- `stock-hot-plugin` → `stock-hot`
- `stock-portfolio-plugin` → `stock-portfolio`
- `stock-rumors-plugin` → `stock-rumors`
- `stock-watchlist-plugin` → `stock-watchlist`
- `tavily-extract-plugin` → `tavily-extract`
- `tavily-search-plugin` → `tavily-search`
- `twitter-plugin` → `twitter`
- `twitter-autopilot-plugin` → `twitter-autopilot`
- `twitter-command-center-search-post-plugin` → `twitter-command-center-search-post`
- `twitter-command-center-search-post-interact-plugin` → `twitter-command-center-search-post-interact`
- `us-stock-analyst-plugin` → `us-stock-analyst`
- `web-search-plugin` → `web-search`
- `x-intelligence-automation-plugin` → `x-intelligence-automation`
- `youtube-plugin` → `youtube`
- `youtube-search-plugin` → `youtube-search`
- `youtube-serp-plugin` → `youtube-serp`
