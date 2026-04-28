# ClawHub Release

ClawHub-oriented packaged copy of all `targetSkills/` mother skills.

## Principles

- Keep `targetSkills/` as the mother-skill source layer.
- Generate `clawhub-release/` as the upload-focused runtime layer.
- Keep original ClawHub slugs separate from ClawHub-only breakout siblings declared in `targets/clawhub-breakout-variants.json`.
- Keep canonical `metadata.aisa`, then duplicate the minimal `metadata.openclaw` hints only where helpful for upload compatibility.
- Prefer runtime-only files, repo-local defaults, and explicit auth flows.

## Directory Layout

- The root stays flat because the current publish/test/live-status scripts discover `clawhub-release/*` directly.
- Read `slug-groups.json` or the grouped lists below when you need the human-friendly split between original and breakout slugs.

## Original Slugs (54)

- `aisa-multi-search-engine` <- source `aisa-multi-search-engine`
- `aisa-provider` <- source `aisa-provider`
- `aisa-tavily` <- source `aisa-tavily`
- `aisa-twitter-api` <- source `aisa-twitter-api`
- `aisa-twitter-command-center` <- source `aisa-twitter-command-center`
- `aisa-twitter-engagement-suite` <- source `aisa-twitter-engagement-suite`
- `aisa-twitter-post-engage` <- source `aisa-twitter-post-engage`
- `aisa-youtube-search` <- source `aisa-youtube-search`
- `aisa-youtube-serp-scout` <- source `aisa-youtube-serp-scout`
- `cn-llm` <- source `cn-llm`
- `crypto-market-data` <- source `crypto-market-data`
- `last30days` <- source `last30days`
- `last30days-zh` <- source `last30days-zh`
- `llm-router` <- source `llm-router`
- `market` <- source `market`
- `marketpulse` <- source `marketpulse`
- `media-gen` <- source `media-gen`
- `multi-search` <- source `multi-search`
- `multi-source-search` <- source `multi-source-search`
- `openclaw-aisa-youtube-aisa` <- source `openclaw-aisa-youtube-aisa`
- `openclaw-media-gen` <- source `openclaw-media-gen`
- `openclaw-search` <- source `openclaw-search`
- `openclaw-twitter` <- source `openclaw-twitter`
- `openclaw-twitter-post-engage` <- source `openclaw-twitter-post-engage`
- `openclaw-youtube` <- source `openclaw-youtube`
- `perplexity-research` <- source `perplexity-research`
- `perplexity-search` <- source `perplexity-search`
- `prediction-market` <- source `prediction-market`
- `prediction-market-arbitrage` <- source `prediction-market-arbitrage`
- `prediction-market-arbitrage-api` <- source `prediction-market-arbitrage-api`
- `prediction-market-arbitrage-zh` <- source `prediction-market-arbitrage-zh`
- `prediction-market-data` <- source `prediction-market-data`
- `prediction-market-data-zh` <- source `prediction-market-data-zh`
- `scholar-search` <- source `scholar-search`
- `search` <- source `search`
- `smart-search` <- source `smart-search`
- `stock-analysis` <- source `stock-analysis`
- `stock-dividend` <- source `stock-dividend`
- `stock-hot` <- source `stock-hot`
- `stock-portfolio` <- source `stock-portfolio`
- `stock-rumors` <- source `stock-rumors`
- `stock-watchlist` <- source `stock-watchlist`
- `tavily-extract` <- source `tavily-extract`
- `tavily-search` <- source `tavily-search`
- `twitter` <- source `twitter`
- `twitter-autopilot` <- source `twitter-autopilot`
- `twitter-command-center-search-post` <- source `twitter-command-center-search-post`
- `twitter-command-center-search-post-interact` <- source `twitter-command-center-search-post-interact`
- `us-stock-analyst` <- source `us-stock-analyst`
- `web-search` <- source `web-search`
- `x-intelligence-automation` <- source `x-intelligence-automation`
- `youtube` <- source `youtube`
- `youtube-search` <- source `youtube-search`
- `youtube-serp` <- source `youtube-serp`

## Breakout Slugs (2)

- `aisa-twitter-api-command-center` <- source `aisa-twitter-api` (`twitter_api`)
- `aisa-twitter-research-engage-relay` <- source `aisa-twitter-engagement-suite` (`twitter_engagement`)
