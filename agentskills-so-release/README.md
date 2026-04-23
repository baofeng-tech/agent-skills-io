# AgentSkills.so Release

Agent Skills open-standard release layer generated from `targetSkills/`.

## Purpose

- Produce a GitHub-ready root-level skill catalog for `agentskills.so` style indexing.
- Keep frontmatter close to the published Agent Skills spec: `name`, `description`, `license`, `compatibility`, flat `metadata`, and optional `allowed-tools`.
- Emit per-skill root-flat ZIP artifacts for manual import flows.

## Layout

- `<skill>/`: publishable skill directory
- `zips/<skill>.zip`: root-flat archive with `SKILL.md` at archive root

## Recommended Publish Flow

1. Push this directory to the public repository `https://github.com/baofeng-tech/agent-skills-so`.
2. Keep every skill directory at the repo root.
3. Preserve `index.json`, `index.md`, and `well-known-skills-index.json` at repo root so crawlers see a stable catalog signal.
4. Submit or share the repo URL with marketplaces that index Agent Skills from GitHub.
5. Use the generated ZIPs for platforms that support direct skill upload/import.

## Generated Skills

- `aisa-multi-search-engine`
- `aisa-provider`
- `aisa-tavily`
- `aisa-twitter-api`
- `aisa-twitter-command-center`
- `aisa-twitter-engagement-suite`
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
