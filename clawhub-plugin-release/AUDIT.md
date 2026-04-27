# ClawHub Plugin Release Audit

- Generated plugins: 54
- Packaging mode: native-first dual format (`openclaw.plugin.json` + `index.ts` + `package.json` + optional `.claude-plugin/plugin.json` + embedded `skills/`)
- Zip rule: archives are written root-flat with required files at archive root.

## aisa-multi-search-engine-plugin

- Skill: `aisa-multi-search-engine`
- Directory: `clawhub-plugin-release/plugins/aisa-multi-search-engine-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-multi-search-engine-plugin.zip`
- Description: Requires python3, node, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-multi-search-engine`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## aisa-provider-plugin

- Skill: `aisa-provider`
- Directory: `clawhub-plugin-release/plugins/aisa-provider-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-provider-plugin.zip`
- Description: Requires AISA_API_KEY. Native-first ClawHub plugin for `aisa-provider`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Use AIsa for model routing, provider setup, and Chinese LLM access. Use when: the user needs model configuration, provider guidance, or routing workflows. Supports setup and model operations.

## aisa-tavily-plugin

- Skill: `aisa-tavily`
- Directory: `clawhub-plugin-release/plugins/aisa-tavily-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-tavily-plugin.zip`
- Description: Requires node, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-tavily`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## aisa-twitter-api-plugin

- Skill: `aisa-twitter-api`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-api-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-api-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `aisa-twitter-api`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa. Use when: the user needs one flagship Twitter skill for trend tracking, competitor monitoring, or publish-ready workflows. Supports search, watchlists, and approved posting.

## aisa-twitter-command-center-plugin

- Skill: `aisa-twitter-command-center`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-command-center-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-command-center-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `aisa-twitter-command-center`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run Twitter/X watchlists, competitor monitoring, trend scans, and OAuth-gated follow-through through AIsa. Use when: the user needs a monitoring-first Twitter desk for recurring account sweeps, launch reactions, or trend tracking. Supports search, monitoring, and approved posting after review.

## aisa-twitter-engagement-suite-plugin

- Skill: `aisa-twitter-engagement-suite`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-engagement-suite-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-engagement-suite-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `aisa-twitter-engagement-suite`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa. Use when: the user already knows which account, tweet, or campaign to act on and needs explicit engagement workflows. Supports read context, engagement actions, and approved posting.

## aisa-twitter-post-engage-plugin

- Skill: `aisa-twitter-post-engage`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-post-engage-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-post-engage-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `aisa-twitter-post-engage`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run Twitter/X post-launch follow-through through AIsa. Use when: the user already has a draft, launch tweet, or reply target and needs one skill to publish and then manage early interactions. Supports posting, reply context, and lightweight engagement.

## aisa-youtube-search-plugin

- Skill: `aisa-youtube-search`
- Directory: `clawhub-plugin-release/plugins/aisa-youtube-search-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-youtube-search-plugin.zip`
- Description: Requires AISA_API_KEY. Native-first ClawHub plugin for `aisa-youtube-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.

## aisa-youtube-serp-scout-plugin

- Skill: `aisa-youtube-serp-scout`
- Directory: `clawhub-plugin-release/plugins/aisa-youtube-serp-scout-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-youtube-serp-scout-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-youtube-serp-scout`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.

## cn-llm-plugin

- Skill: `cn-llm`
- Directory: `clawhub-plugin-release/plugins/cn-llm-plugin`
- Zip: `clawhub-plugin-release/zips/cn-llm-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `cn-llm`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Use AIsa for model routing, provider setup, and Chinese LLM access. Use when: the user needs model configuration, provider guidance, or routing workflows. Supports setup and model operations.

## crypto-market-data-plugin

- Skill: `crypto-market-data`
- Directory: `clawhub-plugin-release/plugins/crypto-market-data-plugin`
- Zip: `clawhub-plugin-release/zips/crypto-market-data-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `crypto-market-data`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## last30days-plugin

- Skill: `last30days`
- Directory: `clawhub-plugin-release/plugins/last30days-plugin`
- Zip: `clawhub-plugin-release/zips/last30days-plugin.zip`
- Description: Requires python3, bash, and AISA_API_KEY. Native-first ClawHub plugin for `last30days`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## last30days-zh-plugin

- Skill: `last30days-zh`
- Directory: `clawhub-plugin-release/plugins/last30days-zh-plugin`
- Zip: `clawhub-plugin-release/zips/last30days-zh-plugin.zip`
- Description: Requires python3, bash, and AISA_API_KEY. Native-first ClawHub plugin for `last30days-zh`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. 通过 AIsa 执行网页、多源或近 30 天研究检索。触发条件：当用户需要搜索、研究、比对或趋势归纳时使用。支持多源检索与结构化输出。

## llm-router-plugin

- Skill: `llm-router`
- Directory: `clawhub-plugin-release/plugins/llm-router-plugin`
- Zip: `clawhub-plugin-release/zips/llm-router-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `llm-router`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Use AIsa for model routing, provider setup, and Chinese LLM access. Use when: the user needs model configuration, provider guidance, or routing workflows. Supports setup and model operations.

## market-plugin

- Skill: `market`
- Directory: `clawhub-plugin-release/plugins/market-plugin`
- Zip: `clawhub-plugin-release/zips/market-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `market`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## marketpulse-plugin

- Skill: `marketpulse`
- Directory: `clawhub-plugin-release/plugins/marketpulse-plugin`
- Zip: `clawhub-plugin-release/zips/marketpulse-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `marketpulse`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## media-gen-plugin

- Skill: `media-gen`
- Directory: `clawhub-plugin-release/plugins/media-gen-plugin`
- Zip: `clawhub-plugin-release/zips/media-gen-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `media-gen`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Generate AI images or videos through AIsa. Use when: the user needs creative generation, asset drafts, or media workflows. Supports image and video generation.

## multi-search-plugin

- Skill: `multi-search`
- Directory: `clawhub-plugin-release/plugins/multi-search-plugin`
- Zip: `clawhub-plugin-release/zips/multi-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `multi-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## multi-source-search-plugin

- Skill: `multi-source-search`
- Directory: `clawhub-plugin-release/plugins/multi-source-search-plugin`
- Zip: `clawhub-plugin-release/zips/multi-source-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `multi-source-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run confidence-scored multi-source retrieval through AIsa. Use when: the user needs cross-source verification, consensus checks, or one report that compares multiple search surfaces. Supports parallel retrieval, confidence scoring, and synthesis-ready outputs.

## openclaw-aisa-youtube-aisa-plugin

- Skill: `openclaw-aisa-youtube-aisa`
- Directory: `clawhub-plugin-release/plugins/openclaw-aisa-youtube-aisa-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-aisa-youtube-aisa-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-aisa-youtube-aisa`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.

## openclaw-media-gen-plugin

- Skill: `openclaw-media-gen`
- Directory: `clawhub-plugin-release/plugins/openclaw-media-gen-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-media-gen-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-media-gen`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Generate AI images or videos through AIsa. Use when: the user needs creative generation, asset drafts, or media workflows. Supports image and video generation.

## openclaw-search-plugin

- Skill: `openclaw-search`
- Directory: `clawhub-plugin-release/plugins/openclaw-search-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## openclaw-twitter-plugin

- Skill: `openclaw-twitter`
- Directory: `clawhub-plugin-release/plugins/openclaw-twitter-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-twitter-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `openclaw-twitter`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## openclaw-twitter-post-engage-plugin

- Skill: `openclaw-twitter-post-engage`
- Directory: `clawhub-plugin-release/plugins/openclaw-twitter-post-engage-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-twitter-post-engage-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `openclaw-twitter-post-engage`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## openclaw-youtube-plugin

- Skill: `openclaw-youtube`
- Directory: `clawhub-plugin-release/plugins/openclaw-youtube-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-youtube-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-youtube`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.

## perplexity-research-plugin

- Skill: `perplexity-research`
- Directory: `clawhub-plugin-release/plugins/perplexity-research-plugin`
- Zip: `clawhub-plugin-release/zips/perplexity-research-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `perplexity-research`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## perplexity-search-plugin

- Skill: `perplexity-search`
- Directory: `clawhub-plugin-release/plugins/perplexity-search-plugin`
- Zip: `clawhub-plugin-release/zips/perplexity-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `perplexity-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## prediction-market-plugin

- Skill: `prediction-market`
- Directory: `clawhub-plugin-release/plugins/prediction-market-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## prediction-market-arbitrage-plugin

- Skill: `prediction-market-arbitrage`
- Directory: `clawhub-plugin-release/plugins/prediction-market-arbitrage-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-arbitrage-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-arbitrage`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## prediction-market-arbitrage-api-plugin

- Skill: `prediction-market-arbitrage-api`
- Directory: `clawhub-plugin-release/plugins/prediction-market-arbitrage-api-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-arbitrage-api-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-arbitrage-api`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## prediction-market-arbitrage-zh-plugin

- Skill: `prediction-market-arbitrage-zh`
- Directory: `clawhub-plugin-release/plugins/prediction-market-arbitrage-zh-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-arbitrage-zh-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-arbitrage-zh`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. 通过 AIsa 查询股票、加密、预测市场与投资分析数据。触发条件：当用户需要市场研究、筛选、价格走势或组合分析时使用。支持研究与分析输出。

## prediction-market-data-plugin

- Skill: `prediction-market-data`
- Directory: `clawhub-plugin-release/plugins/prediction-market-data-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-data-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-data`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## prediction-market-data-zh-plugin

- Skill: `prediction-market-data-zh`
- Directory: `clawhub-plugin-release/plugins/prediction-market-data-zh-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-data-zh-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-data-zh`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. 通过 AIsa 查询股票、加密、预测市场与投资分析数据。触发条件：当用户需要市场研究、筛选、价格走势或组合分析时使用。支持研究与分析输出。

## scholar-search-plugin

- Skill: `scholar-search`
- Directory: `clawhub-plugin-release/plugins/scholar-search-plugin`
- Zip: `clawhub-plugin-release/zips/scholar-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `scholar-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## search-plugin

- Skill: `search`
- Directory: `clawhub-plugin-release/plugins/search-plugin`
- Zip: `clawhub-plugin-release/zips/search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, scholar, Tavily, and deep research through one AIsa search command center. Use when: the user needs one flagship skill for live search, source discovery, or citation-ready research. Supports fast lookup, answer generation, and deep research reports.

## smart-search-plugin

- Skill: `smart-search`
- Directory: `clawhub-plugin-release/plugins/smart-search-plugin`
- Zip: `clawhub-plugin-release/zips/smart-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `smart-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## stock-analysis-plugin

- Skill: `stock-analysis`
- Directory: `clawhub-plugin-release/plugins/stock-analysis-plugin`
- Zip: `clawhub-plugin-release/zips/stock-analysis-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-analysis`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## stock-dividend-plugin

- Skill: `stock-dividend`
- Directory: `clawhub-plugin-release/plugins/stock-dividend-plugin`
- Zip: `clawhub-plugin-release/zips/stock-dividend-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-dividend`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## stock-hot-plugin

- Skill: `stock-hot`
- Directory: `clawhub-plugin-release/plugins/stock-hot-plugin`
- Zip: `clawhub-plugin-release/zips/stock-hot-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-hot`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## stock-portfolio-plugin

- Skill: `stock-portfolio`
- Directory: `clawhub-plugin-release/plugins/stock-portfolio-plugin`
- Zip: `clawhub-plugin-release/zips/stock-portfolio-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-portfolio`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## stock-rumors-plugin

- Skill: `stock-rumors`
- Directory: `clawhub-plugin-release/plugins/stock-rumors-plugin`
- Zip: `clawhub-plugin-release/zips/stock-rumors-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-rumors`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## stock-watchlist-plugin

- Skill: `stock-watchlist`
- Directory: `clawhub-plugin-release/plugins/stock-watchlist-plugin`
- Zip: `clawhub-plugin-release/zips/stock-watchlist-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-watchlist`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## tavily-extract-plugin

- Skill: `tavily-extract`
- Directory: `clawhub-plugin-release/plugins/tavily-extract-plugin`
- Zip: `clawhub-plugin-release/zips/tavily-extract-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `tavily-extract`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## tavily-search-plugin

- Skill: `tavily-search`
- Directory: `clawhub-plugin-release/plugins/tavily-search-plugin`
- Zip: `clawhub-plugin-release/zips/tavily-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `tavily-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## twitter-plugin

- Skill: `twitter`
- Directory: `clawhub-plugin-release/plugins/twitter-plugin`
- Zip: `clawhub-plugin-release/zips/twitter-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `twitter`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## twitter-autopilot-plugin

- Skill: `twitter-autopilot`
- Directory: `clawhub-plugin-release/plugins/twitter-autopilot-plugin`
- Zip: `clawhub-plugin-release/zips/twitter-autopilot-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `twitter-autopilot`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## twitter-command-center-search-post-plugin

- Skill: `twitter-command-center-search-post`
- Directory: `clawhub-plugin-release/plugins/twitter-command-center-search-post-plugin`
- Zip: `clawhub-plugin-release/zips/twitter-command-center-search-post-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `twitter-command-center-search-post`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## twitter-command-center-search-post-interact-plugin

- Skill: `twitter-command-center-search-post-interact`
- Directory: `clawhub-plugin-release/plugins/twitter-command-center-search-post-interact-plugin`
- Zip: `clawhub-plugin-release/zips/twitter-command-center-search-post-interact-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `twitter-command-center-search-post-interact`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## us-stock-analyst-plugin

- Skill: `us-stock-analyst`
- Directory: `clawhub-plugin-release/plugins/us-stock-analyst-plugin`
- Zip: `clawhub-plugin-release/zips/us-stock-analyst-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `us-stock-analyst`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.

## web-search-plugin

- Skill: `web-search`
- Directory: `clawhub-plugin-release/plugins/web-search-plugin`
- Zip: `clawhub-plugin-release/zips/web-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `web-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## x-intelligence-automation-plugin

- Skill: `x-intelligence-automation`
- Directory: `clawhub-plugin-release/plugins/x-intelligence-automation-plugin`
- Zip: `clawhub-plugin-release/zips/x-intelligence-automation-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `x-intelligence-automation`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## youtube-plugin

- Skill: `youtube`
- Directory: `clawhub-plugin-release/plugins/youtube-plugin`
- Zip: `clawhub-plugin-release/zips/youtube-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `youtube`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.

## youtube-search-plugin

- Skill: `youtube-search`
- Directory: `clawhub-plugin-release/plugins/youtube-search-plugin`
- Zip: `clawhub-plugin-release/zips/youtube-search-plugin.zip`
- Description: Requires AISA_API_KEY. Uses a configurable AIsa relay for Twitter/X research, OAuth-gated posting, and user-approved media uploads. Native-first ClawHub plugin for `youtube-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.

## youtube-serp-plugin

- Skill: `youtube-serp`
- Directory: `clawhub-plugin-release/plugins/youtube-serp-plugin`
- Zip: `clawhub-plugin-release/zips/youtube-serp-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `youtube-serp`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.
