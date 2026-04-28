# ClawHub Plugin Release Audit

- Generated plugins: 56
- Packaging mode: native-first dual format (`openclaw.plugin.json` + `index.ts` + `package.json` + optional `.claude-plugin/plugin.json` + embedded `skills/`)
- Zip rule: archives are written root-flat with required files at archive root.

## aisa-multi-search-engine-plugin

- Skill: `aisa-multi-search-engine`
- Directory: `clawhub-plugin-release/plugins/aisa-multi-search-engine-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-multi-search-engine-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-multi-search-engine`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Multi-source search engine powered by AIsa API. Combines Tavily web search, Scholar academic search, Smart hybrid search, and Perplexity deep research — all through a single AIsa API key. Includes confidence scoring and AI synthesis. Use when: the user needs web search, research, source discovery, or content extraction.

## aisa-provider-plugin

- Skill: `aisa-provider`
- Directory: `clawhub-plugin-release/plugins/aisa-provider-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-provider-plugin.zip`
- Description: Requires AISA_API_KEY. Native-first ClawHub plugin for `aisa-provider`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Configure AIsa as a first-class model provider for OpenClaw, enabling production access to major Chinese AI models (Qwen, DeepSeek, Kimi K2.5, Doubao) through official partnerships with Alibaba Cloud, BytePlus, and Moonshot. Use this skill when the user wants to set up Chinese AI models, configure AIsa API access, compare pricing between AIsa and other providers (OpenRouter, Bailian), switch between Qwen/DeepSeek/Kimi models, or troubleshoot AIsa provider configuration in OpenClaw. Also use when the user mentions AISA_API_KEY, asks about Chinese LLM pricing, Kimi K2.5 setup, or needs help with Qwen Key Account setup.

## aisa-tavily-plugin

- Skill: `aisa-tavily`
- Directory: `clawhub-plugin-release/plugins/aisa-tavily-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-tavily-plugin.zip`
- Description: Requires node, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-tavily`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. AI-optimized web search via AIsa's Tavily API proxy. Returns concise, relevant results for AI agents through AIsa's unified API gateway. Use when: the user needs web search, research, source discovery, or content extraction.

## aisa-twitter-api-plugin

- Skill: `aisa-twitter-api`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-api-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-api-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-twitter-api`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Twitter/X command center for research, monitoring, watchlists, and approved posting through AIsa. Use when: the user needs one flagship skill for trend tracking, competitor monitoring, or publish-ready Twitter workflows without sharing passwords. Supports search, watchlists, and OAuth-gated posting.

## aisa-twitter-api-command-center-plugin

- Skill: `aisa-twitter-api-command-center`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-api-command-center-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-api-command-center-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-twitter-api-command-center`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa. Use when: the user needs one flagship Twitter skill for trend tracking, competitor monitoring, or publish-ready workflows. Supports search, watchlists, and approved posting.

## aisa-twitter-command-center-plugin

- Skill: `aisa-twitter-command-center`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-command-center-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-command-center-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-twitter-command-center`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth. Use when the user asks for Twitter research, monitoring, or posting without sharing passwords.

## aisa-twitter-engagement-suite-plugin

- Skill: `aisa-twitter-engagement-suite`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-engagement-suite-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-engagement-suite-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-twitter-engagement-suite`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.

## aisa-twitter-post-engage-plugin

- Skill: `aisa-twitter-post-engage`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-post-engage-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-post-engage-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-twitter-post-engage`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.

## aisa-twitter-research-engage-relay-plugin

- Skill: `aisa-twitter-research-engage-relay`
- Directory: `clawhub-plugin-release/plugins/aisa-twitter-research-engage-relay-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-twitter-research-engage-relay-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-twitter-research-engage-relay`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa. Use when: the user already knows which account, tweet, or campaign to act on and needs explicit engagement workflows. Supports read context, engagement actions, and approved posting.

## aisa-youtube-search-plugin

- Skill: `aisa-youtube-search`
- Directory: `clawhub-plugin-release/plugins/aisa-youtube-search-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-youtube-search-plugin.zip`
- Description: Requires AISA_API_KEY. Native-first ClawHub plugin for `aisa-youtube-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, and playlists through the AIsa YouTube relay with one API key. Use when the user asks for YouTube discovery, query expansion, or pagination without managing Google credentials.

## aisa-youtube-serp-scout-plugin

- Skill: `aisa-youtube-serp-scout`
- Directory: `clawhub-plugin-release/plugins/aisa-youtube-serp-scout-plugin`
- Zip: `clawhub-plugin-release/zips/aisa-youtube-serp-scout-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `aisa-youtube-serp-scout`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, and trends through the AIsa YouTube SERP client. Use when the user asks for content research, competitor tracking, or trend discovery without managing Google credentials. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.

## cn-llm-plugin

- Skill: `cn-llm`
- Directory: `clawhub-plugin-release/plugins/cn-llm-plugin`
- Zip: `clawhub-plugin-release/zips/cn-llm-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `cn-llm`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. China LLM Gateway - Unified interface for Chinese LLMs including Qwen, DeepSeek, GLM, Baichuan. OpenAI compatible, one API Key for all models. Use when: the user needs model routing, provider setup, or Chinese LLM access guidance.

## crypto-market-data-plugin

- Skill: `crypto-market-data`
- Directory: `clawhub-plugin-release/plugins/crypto-market-data-plugin`
- Zip: `clawhub-plugin-release/zips/crypto-market-data-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `crypto-market-data`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query real-time and historical cryptocurrency market data via CoinGecko — simple prices, coin details, historical charts, OHLC candles, token prices by contract address, market-cap rankings, exchange data and tickers, categories, trending searches, and crypto news. Use for crypto research, price tracking, on-chain token lookup, portfolio analysis, and market-cap screening. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## last30days-plugin

- Skill: `last30days`
- Directory: `clawhub-plugin-release/plugins/last30days-plugin`
- Zip: `clawhub-plugin-release/zips/last30days-plugin.zip`
- Description: Requires python3, bash, and AISA_API_KEY. Native-first ClawHub plugin for `last30days`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Research the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search. Returns a ranked, clustered brief with citations. Use when the task needs recent social evidence, competitor comparisons, launch reactions, trend scans, or person/company profiles.

## last30days-zh-plugin

- Skill: `last30days-zh`
- Directory: `clawhub-plugin-release/plugins/last30days-zh-plugin`
- Zip: `clawhub-plugin-release/zips/last30days-zh-plugin.zip`
- Description: Requires python3, bash, and AISA_API_KEY. Native-first ClawHub plugin for `last30days-zh`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. 聚合最近 30 天的 Reddit、X/Twitter、YouTube、TikTok、Instagram、Hacker News、Polymarket 和 web search 结果. Use when: the user needs recent multi-source research across the last 30 days.

## llm-router-plugin

- Skill: `llm-router`
- Directory: `clawhub-plugin-release/plugins/llm-router-plugin`
- Zip: `clawhub-plugin-release/zips/llm-router-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `llm-router`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key. Use when: the user needs model routing, provider setup, or Chinese LLM access guidance.

## market-plugin

- Skill: `market`
- Directory: `clawhub-plugin-release/plugins/market-plugin`
- Zip: `clawhub-plugin-release/zips/market-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `market`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query real-time and historical financial data across equities and crypto—prices, market moves, metrics, and trends for analysis, alerts, and reporting. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## marketpulse-plugin

- Skill: `marketpulse`
- Directory: `clawhub-plugin-release/plugins/marketpulse-plugin`
- Zip: `clawhub-plugin-release/zips/marketpulse-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `marketpulse`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query real-time and historical financial data for equities—prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## media-gen-plugin

- Skill: `media-gen`
- Directory: `clawhub-plugin-release/plugins/media-gen-plugin`
- Zip: `clawhub-plugin-release/zips/media-gen-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `media-gen`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Generate images and videos with AIsa. Four image models (Google Gemini 3 Pro Image, Alibaba Wan 2.7 image + image-pro, ByteDance Seedream) and four Wan video variants (wan2.6/2.7 × t2v/i2v). One API key; the client routes each model to the correct endpoint automatically. Use when: the user needs AI image or video generation workflows.

## multi-search-plugin

- Skill: `multi-search`
- Directory: `clawhub-plugin-release/plugins/multi-search-plugin`
- Zip: `clawhub-plugin-release/zips/multi-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `multi-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Parallel multi-source search combining Web, Scholar, Smart, and Tavily results with confidence scoring and AI synthesis. Best for comprehensive research requiring cross-source validation. Use when: the user needs web search, research, source discovery, or content extraction.

## multi-source-search-plugin

- Skill: `multi-source-search`
- Directory: `clawhub-plugin-release/plugins/multi-source-search-plugin`
- Zip: `clawhub-plugin-release/zips/multi-source-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `multi-source-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Confidence-scored multi-source retrieval across web, scholar, Tavily, and Perplexity-backed research. Use when: the user needs cross-source verification, consensus checks, or one report that compares multiple search surfaces. Supports parallel retrieval, confidence scoring, and synthesis-ready outputs.

## openclaw-aisa-youtube-aisa-plugin

- Skill: `openclaw-aisa-youtube-aisa`
- Directory: `clawhub-plugin-release/plugins/openclaw-aisa-youtube-aisa-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-aisa-youtube-aisa-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-aisa-youtube-aisa`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search YouTube videos, channels, and trends through the AISA YouTube SERP client. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.

## openclaw-media-gen-plugin

- Skill: `openclaw-media-gen`
- Directory: `clawhub-plugin-release/plugins/openclaw-media-gen-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-media-gen-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-media-gen`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Generate images and videos with AIsa. Four image models (Google Gemini 3 Pro Image, Alibaba Wan 2.7 image + image-pro, ByteDance Seedream) and four Wan video variants (wan2.6/2.7 × t2v/i2v). One API key; the client routes each model to the correct endpoint automatically. Use when: the user needs AI image or video generation workflows.

## openclaw-search-plugin

- Skill: `openclaw-search`
- Directory: `clawhub-plugin-release/plugins/openclaw-search-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Intelligent search for agents. Multi-source retrieval with confidence scoring - web, academic, and Tavily in one unified API. Use when: the user needs web search, research, source discovery, or content extraction.

## openclaw-twitter-plugin

- Skill: `openclaw-twitter`
- Directory: `clawhub-plugin-release/plugins/openclaw-twitter-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-twitter-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-twitter`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AISA relay, then publish approved posts with OAuth. Use when: the user asks for Twitter/X research, monitoring, or posting without sharing passwords. Supports read APIs, authorization links, and media-aware posting.

## openclaw-twitter-post-engage-plugin

- Skill: `openclaw-twitter-post-engage`
- Directory: `clawhub-plugin-release/plugins/openclaw-twitter-post-engage-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-twitter-post-engage-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-twitter-post-engage`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AISA relay. Use when: the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords. Supports read APIs, OAuth-gated posting, and follow or like operations.

## openclaw-youtube-plugin

- Skill: `openclaw-youtube`
- Directory: `clawhub-plugin-release/plugins/openclaw-youtube-plugin`
- Zip: `clawhub-plugin-release/zips/openclaw-youtube-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `openclaw-youtube`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.

## perplexity-research-plugin

- Skill: `perplexity-research`
- Directory: `clawhub-plugin-release/plugins/perplexity-research-plugin`
- Zip: `clawhub-plugin-release/zips/perplexity-research-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `perplexity-research`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Deep research using Perplexity Sonar models via AIsa API. Provides synthesized answers with citations. Supports 4 models from fast to exhaustive deep research. Use when: the user needs web search, research, source discovery, or content extraction.

## perplexity-search-plugin

- Skill: `perplexity-search`
- Directory: `clawhub-plugin-release/plugins/perplexity-search-plugin`
- Zip: `clawhub-plugin-release/zips/perplexity-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `perplexity-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Perplexity Sonar search and answer generation through AIsa. Use when the task is specifically to call Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, or Sonar Deep Research for citation-backed web answers, analytical reasoning, or long-form research reports.

## prediction-market-plugin

- Skill: `prediction-market`
- Directory: `clawhub-plugin-release/plugins/prediction-market-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Prediction markets data - Polymarket, Kalshi markets, prices, positions, and trades. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## prediction-market-arbitrage-plugin

- Skill: `prediction-market-arbitrage`
- Directory: `clawhub-plugin-release/plugins/prediction-market-arbitrage-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-arbitrage-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-arbitrage`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Find and analyze arbitrage opportunities across prediction markets like Polymarket and Kalshi. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## prediction-market-arbitrage-api-plugin

- Skill: `prediction-market-arbitrage-api`
- Directory: `clawhub-plugin-release/plugins/prediction-market-arbitrage-api-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-arbitrage-api-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-arbitrage-api`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Find arbitrage opportunities across Polymarket and Kalshi prediction markets via AIsa API. Scan sports markets for cross-platform price discrepancies, compare real-time odds, verify orderbook liquidity. Use when user asks about: prediction market arbitrage, cross-platform price differences, sports betting arbitrage, odds comparison, risk-free profit, market inefficiencies.

## prediction-market-arbitrage-zh-plugin

- Skill: `prediction-market-arbitrage-zh`
- Directory: `clawhub-plugin-release/plugins/prediction-market-arbitrage-zh-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-arbitrage-zh-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-arbitrage-zh`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. 通过 AIsa API 发现 Polymarket 和 Kalshi 预测市场的套利机会。扫描体育市场跨平台价差、比较实时赔率、验证订单簿流动性。适用场景：预测市场套利、跨平台价差、体育博彩套利、赔率对比、无风险利润、市场低效。 Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## prediction-market-data-plugin

- Skill: `prediction-market-data`
- Directory: `clawhub-plugin-release/plugins/prediction-market-data-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-data-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-data`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Prediction markets data - Polymarket, Kalshi markets, prices, positions, and trades. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## prediction-market-data-zh-plugin

- Skill: `prediction-market-data-zh`
- Directory: `clawhub-plugin-release/plugins/prediction-market-data-zh-plugin`
- Zip: `clawhub-plugin-release/zips/prediction-market-data-zh-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `prediction-market-data-zh`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. 通过 AIsa API 查询跨平台预测市场数据。支持 Polymarket 和 Kalshi 的市场行情、价格、订单簿、K线、持仓和交易记录。适用场景：查询预测市场赔率、选举博彩、事件概率、市场情绪、Polymarket 价格、Kalshi 价格、体育博彩赔率、钱包盈亏、跨平台市场对比。 Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## scholar-search-plugin

- Skill: `scholar-search`
- Directory: `clawhub-plugin-release/plugins/scholar-search-plugin`
- Zip: `clawhub-plugin-release/zips/scholar-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `scholar-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search academic papers and scholarly articles via AIsa Scholar endpoint. Supports year range filtering for targeted research. Use when: the user needs web search, research, source discovery, or content extraction.

## search-plugin

- Skill: `search`
- Directory: `clawhub-plugin-release/plugins/search-plugin`
- Zip: `clawhub-plugin-release/zips/search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search command center for web, academic, Tavily, and Perplexity-backed research through one AIsa API key. Use when: the user needs one flagship skill for live search, source discovery, or citation-ready research. Supports fast lookup, answer generation, and deep research reports.

## smart-search-plugin

- Skill: `smart-search`
- Directory: `clawhub-plugin-release/plugins/smart-search-plugin`
- Zip: `clawhub-plugin-release/zips/smart-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `smart-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Intelligent hybrid search combining web and academic sources via AIsa Smart Search endpoint. Best when you need both web and scholarly results. Use when: the user needs web search, research, source discovery, or content extraction.

## stock-analysis-plugin

- Skill: `stock-analysis`
- Directory: `clawhub-plugin-release/plugins/stock-analysis-plugin`
- Zip: `clawhub-plugin-release/zips/stock-analysis-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-analysis`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Analyze stocks and cryptocurrencies with 8-dimension scoring via AIsa API. Provides BUY/HOLD/SELL signals with confidence levels, entry/target/stop prices, and risk flags. Supports single or multi-ticker analysis with optional fast mode and JSON output. Use when the user asks to analyze a stock, check a ticker, or compare investments.

## stock-dividend-plugin

- Skill: `stock-dividend`
- Directory: `clawhub-plugin-release/plugins/stock-dividend-plugin`
- Zip: `clawhub-plugin-release/zips/stock-dividend-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-dividend`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Analyze dividend metrics for stocks via AIsa API. Provides yield, payout ratio, growth CAGR, safety score (0-100), income rating, and Dividend Aristocrat/King status. Use when the user asks about dividends, income investing, or dividend safety.

## stock-hot-plugin

- Skill: `stock-hot`
- Directory: `clawhub-plugin-release/plugins/stock-hot-plugin`
- Zip: `clawhub-plugin-release/zips/stock-hot-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-hot`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Hot Scanner — find the most trending and high-momentum stocks and crypto right now via AIsa API. Top gainers, losers, most active by volume, crypto highlights, news catalysts, and top 5 watchlist picks. Use when the user asks about trending stocks, what's hot, market movers, or momentum plays.

## stock-portfolio-plugin

- Skill: `stock-portfolio`
- Directory: `clawhub-plugin-release/plugins/stock-portfolio-plugin`
- Zip: `clawhub-plugin-release/zips/stock-portfolio-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-portfolio`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Manage investment portfolios with live P&L tracking via AIsa API. Create, add, update, remove positions, rename, and show portfolio summary with real-time profit/loss. Use when the user wants to track investments, manage a portfolio, check P&L, or add/remove holdings.

## stock-rumors-plugin

- Skill: `stock-rumors`
- Directory: `clawhub-plugin-release/plugins/stock-rumors-plugin`
- Zip: `clawhub-plugin-release/zips/stock-rumors-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `stock-rumors`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Rumor Scanner — find early signals including M&A rumors, insider activity, analyst upgrades/downgrades, social whispers, and SEC/regulatory activity via AIsa API. Ranked by impact score. Use when the user asks about rumors, insider trading, M&A activity, analyst changes, or early market signals.

## stock-watchlist-plugin

- Skill: `stock-watchlist`
- Directory: `clawhub-plugin-release/plugins/stock-watchlist-plugin`
- Zip: `clawhub-plugin-release/zips/stock-watchlist-plugin.zip`
- Description: Requires AISA_API_KEY. Native-first ClawHub plugin for `stock-watchlist`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Manage a stock/crypto watchlist with price target and stop-loss alerts via AIsa API. Add, remove, list, and check tickers with live price alerts. Use when the user wants to track stocks, set price alerts, manage a watchlist, or check triggered alerts.

## tavily-extract-plugin

- Skill: `tavily-extract`
- Directory: `clawhub-plugin-release/plugins/tavily-extract-plugin`
- Zip: `clawhub-plugin-release/zips/tavily-extract-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `tavily-extract`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Extract clean, readable content from one or more URLs using Tavily Extract via AIsa API. Useful for reading full articles without visiting the page. Use when: the user needs web search, research, source discovery, or content extraction.

## tavily-search-plugin

- Skill: `tavily-search`
- Directory: `clawhub-plugin-release/plugins/tavily-search-plugin`
- Zip: `clawhub-plugin-release/zips/tavily-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `tavily-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Advanced web search via Tavily through AIsa API. Supports search depth, topic filtering (general/news/finance), time ranges, domain inclusion/exclusion, and LLM-generated answers. Use when: the user needs web search, research, source discovery, or content extraction.

## twitter-plugin

- Skill: `twitter`
- Directory: `clawhub-plugin-release/plugins/twitter-plugin`
- Zip: `clawhub-plugin-release/zips/twitter-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `twitter`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.

## twitter-autopilot-plugin

- Skill: `twitter-autopilot`
- Directory: `clawhub-plugin-release/plugins/twitter-autopilot-plugin`
- Zip: `clawhub-plugin-release/zips/twitter-autopilot-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `twitter-autopilot`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.

## twitter-command-center-search-post-plugin

- Skill: `twitter-command-center-search-post`
- Directory: `clawhub-plugin-release/plugins/twitter-command-center-search-post-plugin`
- Zip: `clawhub-plugin-release/zips/twitter-command-center-search-post-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `twitter-command-center-search-post`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, or posting without sharing account passwords.

## twitter-command-center-search-post-interact-plugin

- Skill: `twitter-command-center-search-post-interact`
- Directory: `clawhub-plugin-release/plugins/twitter-command-center-search-post-interact-plugin`
- Zip: `clawhub-plugin-release/zips/twitter-command-center-search-post-interact-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `twitter-command-center-search-post-interact`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.

## us-stock-analyst-plugin

- Skill: `us-stock-analyst`
- Directory: `clawhub-plugin-release/plugins/us-stock-analyst-plugin`
- Zip: `clawhub-plugin-release/zips/us-stock-analyst-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `us-stock-analyst`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Professional US stock analysis with financial data, news, social sentiment, and multi-model AI. Comprehensive reports at $0.02-0.10 per analysis. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.

## web-search-plugin

- Skill: `web-search`
- Directory: `clawhub-plugin-release/plugins/web-search-plugin`
- Zip: `clawhub-plugin-release/zips/web-search-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `web-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search the web using AIsa Scholar Web endpoint. Returns structured web results with titles, URLs, and snippets. Use when: the user needs web search, research, source discovery, or content extraction.

## x-intelligence-automation-plugin

- Skill: `x-intelligence-automation`
- Directory: `clawhub-plugin-release/plugins/x-intelligence-automation-plugin`
- Zip: `clawhub-plugin-release/zips/x-intelligence-automation-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `x-intelligence-automation`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.

## youtube-plugin

- Skill: `youtube`
- Directory: `clawhub-plugin-release/plugins/youtube-plugin`
- Zip: `clawhub-plugin-release/zips/youtube-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `youtube`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.

## youtube-search-plugin

- Skill: `youtube-search`
- Directory: `clawhub-plugin-release/plugins/youtube-search-plugin`
- Zip: `clawhub-plugin-release/zips/youtube-search-plugin.zip`
- Description: Requires AISA_API_KEY. Native-first ClawHub plugin for `youtube-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. YouTube Search API via AIsa unified endpoint. Search YouTube videos, channels, and playlists with a single AIsa API key — no Google API key or OAuth required. Use this skill when users want to search YouTube content. For other AIsa capabilities (LLM, financial data, Twitter, web search), see the aisa-core skill. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.

## youtube-serp-plugin

- Skill: `youtube-serp`
- Directory: `clawhub-plugin-release/plugins/youtube-serp-plugin`
- Zip: `clawhub-plugin-release/zips/youtube-serp-plugin.zip`
- Description: Requires python3, and AISA_API_KEY. Native-first ClawHub plugin for `youtube-serp`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. YouTube SERP for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
