# ClawHub Release

ClawHub-oriented packaged copy of all `targetSkills/` mother skills.

## Principles

- Keep `targetSkills/` as the mother-skill source layer.
- Generate `clawhub-release/` as the upload-focused runtime layer.
- Keep original ClawHub slugs separate from ClawHub-only breakout siblings declared in `targets/clawhub-breakout-variants.json`.
- Keep canonical `metadata.aisa`, then duplicate the minimal `metadata.openclaw` hints only where helpful for upload compatibility.
- Prefer runtime-only files, repo-local defaults, and explicit auth flows.

## Skills

- `aisa-multi-search-engine`
- `aisa-provider`
- `aisa-tavily`
- `aisa-twitter-api`
- `aisa-twitter-api-command-center`
- `aisa-twitter-command-center`
- `aisa-twitter-engagement-suite`
- `aisa-twitter-research-engage-relay`
- `aisa-twitter-post-engage`
- `aisa-youtube-search`
- `aisa-youtube-serp-scout`
- `cn-llm`
- `crypto-market-data`
- `last30days`
- `last30days-zh`
- `llm-router`
- `market`
- `marketpulse`
- `media-gen`
- `multi-search`
- `multi-source-search`
- `openclaw-aisa-youtube-aisa`
- `openclaw-media-gen`
- `openclaw-search`
- `openclaw-twitter`
- `openclaw-twitter-post-engage`
- `openclaw-youtube`
- `perplexity-research`
- `perplexity-search`
- `prediction-market`
- `prediction-market-arbitrage`
- `prediction-market-arbitrage-api`
- `prediction-market-arbitrage-zh`
- `prediction-market-data`
- `prediction-market-data-zh`
- `scholar-search`
- `search`
- `smart-search`
- `stock-analysis`
- `stock-dividend`
- `stock-hot`
- `stock-portfolio`
- `stock-rumors`
- `stock-watchlist`
- `tavily-extract`
- `tavily-search`
- `twitter`
- `twitter-autopilot`
- `twitter-command-center-search-post`
- `twitter-command-center-search-post-interact`
- `us-stock-analyst`
- `web-search`
- `x-intelligence-automation`
- `youtube`
- `youtube-search`
- `youtube-serp`
