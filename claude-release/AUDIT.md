# Claude Release Audit

This report summarizes structural cleanup and residual publishing risk for the generated Claude release layer.

## Summary

- Skills converted: 59
- Skills with residual risk notes: 15

## Per Skill

### aisa-multi-search-engine

- Source: `targetSkills/aisa-multi-search-engine`
- Output: `claude-release/aisa-multi-search-engine`
- Description: Multi-source search engine powered by AIsa API. Combines Tavily web search, Scholar academic search, Smart hybrid search, and Perplexity deep research — all through a single AIsa API key. Includes confidence scoring and AI synthesis. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### aisa-provider

- Source: `targetSkills/aisa-provider`
- Output: `claude-release/aisa-provider`
- Description: Configure AIsa as a first-class model provider for OpenClaw, enabling production access to major Chinese AI models (Qwen, DeepSeek, Kimi K2.5, Doubao) through official partnerships with Alibaba Cloud, BytePlus, and Moonshot. Use this skill when the user wants to set up Chinese AI models, configure AIsa API access, compare pricing between AIsa and other providers (OpenRouter, Bailian), switch between Qwen/DeepSeek/Kimi models, or troubleshoot AIsa provider configuration in OpenClaw. Also use when the user mentions AISA_API_KEY, asks about Chinese LLM pricing, Kimi K2.5 setup, or needs help with Qwen Key Account setup.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: rewrote 3 markdown file(s) to reduce OpenClaw-specific release wording
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### aisa-tavily

- Source: `targetSkills/aisa-tavily`
- Output: `claude-release/aisa-tavily`
- Description: Search the web and extract public page content through AIsa's Tavily-backed API relay. Use when: the user needs web search, source discovery, current news lookup, or public URL content extraction. Supports concise result sets, deeper research, and news-focused queries.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### aisa-twitter-api

- Source: `targetSkills/aisa-twitter-api`
- Output: `claude-release/aisa-twitter-api`
- Description: Twitter/X research, monitoring, watchlists, and OAuth-approved posting through AIsa. Use when: the user needs one flagship Twitter skill for trend tracking, competitor monitoring, timeline analysis, or approved posting without sharing passwords. Supports relay-based reads, watchlists, search, and OAuth-gated text or media posting.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: rewrote 1 markdown file(s) to reduce OpenClaw-specific release wording
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### aisa-twitter-command-center

- Source: `targetSkills/aisa-twitter-command-center`
- Output: `claude-release/aisa-twitter-command-center`
- Description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth. Use when the user asks for Twitter research, monitoring, or posting without sharing passwords.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: rewrote 1 markdown file(s) to reduce OpenClaw-specific release wording
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### aisa-twitter-engagement-suite

- Source: `targetSkills/aisa-twitter-engagement-suite`
- Output: `claude-release/aisa-twitter-engagement-suite`
- Description: Research Twitter/X profiles, tweets, and trends, then run approved engagement and posting actions through the AIsa relay. Use when: the user needs Twitter/X research plus likes, follows, unfollows, posting, or post-action follow-through without sharing passwords. Supports relay-based reads, OAuth-approved writes, and media-capable posting flows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: rewrote 1 markdown file(s) to reduce OpenClaw-specific release wording
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### aisa-twitter-post-engage

- Source: `targetSkills/aisa-twitter-post-engage`
- Output: `claude-release/aisa-twitter-post-engage`
- Description: Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: rewrote 1 markdown file(s) to reduce OpenClaw-specific release wording
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### aisa-youtube-search

- Source: `targetSkills/aisa-youtube-search`
- Output: `claude-release/aisa-youtube-search`
- Description: Search YouTube videos, channels, and playlists through the AIsa YouTube relay with one API key. Use when the user asks for YouTube discovery, query expansion, or pagination without managing Google credentials.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README

### aisa-youtube-serp-scout

- Source: `targetSkills/aisa-youtube-serp-scout`
- Output: `claude-release/aisa-youtube-serp-scout`
- Description: Search YouTube videos, channels, and trends through the AIsa YouTube SERP client. Use when the user asks for content research, competitor tracking, or trend discovery without managing Google credentials. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### cn-llm

- Source: `targetSkills/cn-llm`
- Output: `claude-release/cn-llm`
- Description: China LLM Gateway - Unified interface for Chinese LLMs including Qwen, DeepSeek, GLM, Baichuan. OpenAI compatible, one API Key for all models. Use when: the user needs model routing, provider setup, or Chinese LLM access guidance.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### crypto-market-data

- Source: `targetSkills/crypto-market-data`
- Output: `claude-release/crypto-market-data`
- Description: Query real-time and historical cryptocurrency market data via CoinGecko through AIsa — simple prices, coin details, historical charts, OHLC candles, token prices by contract address, market-cap rankings, exchange data and tickers, categories, trending searches, and crypto news. Use when you need crypto market research, price tracking, token lookup, portfolio analysis, or market-cap screening. Use when: the user needs market data, stock analysis, dividend research, or read-only financial data workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### gmail-lead-desk

- Source: `targetSkills/gmail-lead-desk`
- Output: `claude-release/gmail-lead-desk`
- Description: Gmail Lead Desk — standalone sales/CS Gmail skill via the AISA gateway: OAuth connect, scan unread leads, summarize threads, draft template replies (default draft-only), archive with labels. Keywords: Gmail Lead Desk, Gmail, lead desk, sales, customer support, follow-up, unread, inquiry summary, draft reply, archive, OAuth, AISA, connected account, thread_id. Use when: the user needs this workflow's domain-specific automation or guidance.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### last30days

- Source: `targetSkills/last30days`
- Output: `claude-release/last30days`
- Description: Research the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search. Returns a ranked, clustered brief with citations. Use when the task needs recent social evidence, competitor comparisons, launch reactions, trend scans, or person/company profiles.
- Change: removed 2 non-runtime generated/test files from the release bundle
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: switched default local storage to repo-local path in scripts/lib/env.py
- Change: updated config path messaging in scripts/lib/ui.py
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: Large runtime surface remains; verify Python 3.12+ and AISA-only flow before public publishing.

### last30days-zh

- Source: `targetSkills/last30days-zh`
- Output: `claude-release/last30days-zh`
- Description: 聚合最近 30 天的 Reddit、X/Twitter、YouTube、TikTok、Instagram、Hacker News、Polymarket 和 web search 结果. Use when: the user needs recent multi-source research across the last 30 days.
- Change: removed 2 non-runtime generated/test files from the release bundle
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: Large runtime surface remains; verify Python 3.12+ and AISA-only flow before public publishing.

### llm-router

- Source: `targetSkills/llm-router`
- Output: `claude-release/llm-router`
- Description: Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key. Use when: the user needs model routing, provider setup, or Chinese LLM access guidance.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### market

- Source: `targetSkills/market`
- Output: `claude-release/market`
- Description: Query real-time and historical financial data across equities and crypto—prices, market moves, metrics, and trends for analysis, alerts, and reporting. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### marketpulse

- Source: `targetSkills/marketpulse`
- Output: `claude-release/marketpulse`
- Description: Query real-time and historical equity market data—prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates. Use when you need broad public-market research from a single AIsa-backed skill. Use when: the user needs market data, stock analysis, dividend research, or read-only financial data workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### media-gen

- Source: `targetSkills/media-gen`
- Output: `claude-release/media-gen`
- Description: Generate images and videos with AIsa. Supports Gemini, Wan, and Seedream image generation plus Wan text-to-video and image-to-video models. One API key; the bundled client routes each model to the correct endpoint automatically. Use when: you need a neutral AIsa media-generation skill that spans multiple model families without changing credentials or request flow.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### multi-search

- Source: `targetSkills/multi-search`
- Output: `claude-release/multi-search`
- Description: Parallel multi-source search combining Web, Scholar, Smart, and Tavily results with confidence scoring and AI synthesis. Best for comprehensive research requiring cross-source validation. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### multi-source-search

- Source: `targetSkills/multi-source-search`
- Output: `claude-release/multi-source-search`
- Description: Multi-source search for agents across web, scholar, Tavily, and Perplexity Sonar endpoints. Use when you need structured retrieval, citation-backed answers, or broad research coverage from one AIsa API key.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### notion-workspace

- Source: `targetSkills/notion-workspace`
- Output: `claude-release/notion-workspace`
- Description: Manage Notion workspace: search pages and databases, read markdown, create pages, insert rows, triggers, MCP. Powered by AISA gateway (Notion toolkit). Requires AISA_API_KEY and curl. Keywords: notion, workspace, page, database, block, markdown, wiki, task board, insert row, OAuth. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### openclaw-aisa-youtube-aisa

- Source: `targetSkills/openclaw-aisa-youtube-aisa`
- Output: `claude-release/openclaw-aisa-youtube-aisa`
- Description: Search YouTube videos, channels, and trends through the AISA YouTube SERP client. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### openclaw-media-gen

- Source: `targetSkills/openclaw-media-gen`
- Output: `claude-release/openclaw-media-gen`
- Description: Generate images and videos with AIsa. Four image models (Google Gemini 3 Pro Image, Alibaba Wan 2.7 image + image-pro, ByteDance Seedream) and four Wan video variants (wan2.6/2.7 × t2v/i2v). One API key; the client routes each model to the correct endpoint automatically. Use when: the user needs AI image or video generation workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### openclaw-search

- Source: `targetSkills/openclaw-search`
- Output: `claude-release/openclaw-search`
- Description: Intelligent search for agents. Multi-source retrieval with confidence scoring - web, academic, and Tavily in one unified API. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### openclaw-twitter

- Source: `targetSkills/openclaw-twitter`
- Output: `claude-release/openclaw-twitter`
- Description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AISA relay, then publish approved posts with OAuth. Use when: the user asks for Twitter/X research, monitoring, or posting without sharing passwords. Supports read APIs, authorization links, and media-aware posting.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: rewrote 1 markdown file(s) to reduce OpenClaw-specific release wording
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### openclaw-twitter-post-engage

- Source: `targetSkills/openclaw-twitter-post-engage`
- Output: `claude-release/openclaw-twitter-post-engage`
- Description: Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AISA relay. Use when: the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords. Supports read APIs, OAuth-gated posting, and follow or like operations.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: rewrote 2 markdown file(s) to reduce OpenClaw-specific release wording
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### openclaw-youtube

- Source: `targetSkills/openclaw-youtube`
- Output: `claude-release/openclaw-youtube`
- Description: YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### perplexity-research

- Source: `targetSkills/perplexity-research`
- Output: `claude-release/perplexity-research`
- Description: Deep research using Perplexity Sonar models via AIsa API. Provides synthesized answers with citations. Supports 4 models from fast to exhaustive deep research. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### perplexity-search

- Source: `targetSkills/perplexity-search`
- Output: `claude-release/perplexity-search`
- Description: Perplexity Sonar search and answer generation through AIsa. Use when the task is specifically to call Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, or Sonar Deep Research for citation-backed web answers, analytical reasoning, or long-form research reports.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### prediction-market

- Source: `targetSkills/prediction-market`
- Output: `claude-release/prediction-market`
- Description: Prediction markets data - Polymarket, Kalshi markets, prices, positions, and trades. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### prediction-market-arbitrage

- Source: `targetSkills/prediction-market-arbitrage`
- Output: `claude-release/prediction-market-arbitrage`
- Description: Find and analyze arbitrage opportunities across prediction markets like Polymarket and Kalshi. Use when you need to match equivalent markets, compare prices, and verify whether a spread looks actionable.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### prediction-market-arbitrage-api

- Source: `targetSkills/prediction-market-arbitrage-api`
- Output: `claude-release/prediction-market-arbitrage-api`
- Description: Find arbitrage opportunities across Polymarket and Kalshi prediction markets via AIsa API. Scan sports markets for cross-platform price discrepancies, compare real-time odds, verify orderbook liquidity. Use when user asks about: prediction market arbitrage, cross-platform price differences, sports betting arbitrage, odds comparison, risk-free profit, market inefficiencies.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### prediction-market-arbitrage-zh

- Source: `targetSkills/prediction-market-arbitrage-zh`
- Output: `claude-release/prediction-market-arbitrage-zh`
- Description: 通过 AIsa API 发现 Polymarket 和 Kalshi 预测市场的套利机会。扫描体育市场跨平台价差、比较实时赔率、验证订单簿流动性。适用场景：预测市场套利、跨平台价差、体育博彩套利、赔率对比、无风险利润、市场低效。 Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### prediction-market-data

- Source: `targetSkills/prediction-market-data`
- Output: `claude-release/prediction-market-data`
- Description: Access prediction market data from Polymarket and Kalshi, including markets, prices, trades, orderbooks, positions, and cross-platform market matching. Use when you need current odds, historical market data, or wallet-level prediction market analysis.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### prediction-market-data-zh

- Source: `targetSkills/prediction-market-data-zh`
- Output: `claude-release/prediction-market-data-zh`
- Description: 通过 AIsa API 查询跨平台预测市场数据。支持 Polymarket 和 Kalshi 的市场行情、价格、订单簿、K线、持仓和交易记录。适用场景：查询预测市场赔率、选举博彩、事件概率、市场情绪、Polymarket 价格、Kalshi 价格、体育博彩赔率、钱包盈亏、跨平台市场对比。 Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### saas-gateway

- Source: `targetSkills/saas-gateway`
- Output: `claude-release/saas-gateway`
- Description: Unified SaaS integration gateway via api.aisa.one (AISA gateway, v3.1): manage OAuth auth for third-party SaaS apps (Gmail/Slack/GitHub/Notion etc.), tool execution, tool-router sessions, triggers, webhooks, MCP servers, and usage stats. Use when connecting third-party SaaS accounts, running cross-SaaS tools, managing MCP servers, setting up triggers, or checking usage. Keywords: SaaS gateway, connect app, OAuth link, run tool, auth config, tool router, MCP server, trigger, webhook, connected account, usage stats
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### scholar-search

- Source: `targetSkills/scholar-search`
- Output: `claude-release/scholar-search`
- Description: Search academic papers and scholarly articles via AIsa Scholar endpoint. Supports year range filtering for targeted research. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### search

- Source: `targetSkills/search`
- Output: `claude-release/search`
- Description: Search command center for web, academic, Tavily, and Perplexity-backed research through one AIsa API key. Use when: the user needs one flagship skill for live search, source discovery, or citation-ready research. Supports fast lookup, answer generation, and deep research reports.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### seo-keyword-research

- Source: `targetSkills/seo-keyword-research`
- Output: `claude-release/seo-keyword-research`
- Description: Use this skill when a user asks for SEO keyword research, keyword discovery, search volume analysis, keyword difficulty, search intent mapping, topic clusters, content opportunities, competitor keyword gaps, or a keyword strategy for a domain, URL, product, market, or seed topic. When a website is provided, crawl and interpret the site first, then use AIsa API access to DataForSEO keyword, SERP, trend, Labs, and OnPage endpoints plus AIsa LLM reasoning to find non-brand keyword opportunities. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### smart-search

- Source: `targetSkills/smart-search`
- Output: `claude-release/smart-search`
- Description: Intelligent hybrid search combining web and academic sources via AIsa Smart Search endpoint. Best when you need both web and scholarly results. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### stock-analysis

- Source: `targetSkills/stock-analysis`
- Output: `claude-release/stock-analysis`
- Description: Analyze stocks and cryptocurrencies with 8-dimension scoring via AIsa API. Provides BUY/HOLD/SELL signals with confidence levels, entry/target/stop prices, and risk flags. Supports single or multi-ticker analysis with optional fast mode and JSON output. Use when the user asks to analyze a stock, check a ticker, or compare investments.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### stock-dividend

- Source: `targetSkills/stock-dividend`
- Output: `claude-release/stock-dividend`
- Description: Analyze read-only dividend metrics for stocks via AIsa API. Provides yield, payout ratio, growth CAGR, safety score, income rating, and Dividend Aristocrat/King status without placing trades, making purchases, or managing brokerage accounts. Use when: the user needs market data, stock analysis, dividend research, or read-only financial data workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### stock-hot

- Source: `targetSkills/stock-hot`
- Output: `claude-release/stock-hot`
- Description: Hot Scanner — find the most trending and high-momentum stocks and crypto right now via AIsa API. Top gainers, losers, most active by volume, crypto highlights, news catalysts, and top 5 watchlist picks. Use when the user asks about trending stocks, what's hot, market movers, or momentum plays.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### stock-portfolio

- Source: `targetSkills/stock-portfolio`
- Output: `claude-release/stock-portfolio`
- Description: Manage investment portfolios with live P&L tracking via AIsa API. Create, add, update, remove positions, rename, and show portfolio summary with real-time profit/loss. Use when the user wants to track investments, manage a portfolio, check P&L, or add/remove holdings.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: switched default local storage to repo-local path in scripts/portfolio.py
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: Local persistence is still present, but defaults are repo-local instead of home-directory paths.

### stock-rumors

- Source: `targetSkills/stock-rumors`
- Output: `claude-release/stock-rumors`
- Description: Rumor Scanner — find early signals including M&A rumors, insider activity, analyst upgrades/downgrades, social whispers, and SEC/regulatory activity via AIsa API. Ranked by impact score. Use when the user asks about rumors, insider trading, M&A activity, analyst changes, or early market signals.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### stock-watchlist

- Source: `targetSkills/stock-watchlist`
- Output: `claude-release/stock-watchlist`
- Description: Manage a stock/crypto watchlist with price target and stop-loss alerts via AIsa API. Add, remove, list, and check tickers with live price alerts. Use when the user wants to track stocks, set price alerts, manage a watchlist, or check triggered alerts.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: replaced source README with a Claude-oriented release README
- Residual risk: Local persistence is still present, but defaults are repo-local instead of home-directory paths.

### tavily-extract

- Source: `targetSkills/tavily-extract`
- Output: `claude-release/tavily-extract`
- Description: Extract clean, readable content from one or more URLs using Tavily Extract via AIsa API. Useful for reading full articles without visiting the page. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### tavily-search

- Source: `targetSkills/tavily-search`
- Output: `claude-release/tavily-search`
- Description: Advanced web search via Tavily through AIsa API. Supports search depth, topic filtering (general/news/finance), time ranges, domain inclusion/exclusion, and LLM-generated answers. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### trend-forecast

- Source: `targetSkills/trend-forecast`
- Output: `claude-release/trend-forecast`
- Description: Multi-signal trend forecasting for autonomous agents. Combines prediction market odds, Twitter/X social sentiment, news velocity, and stock market data into a unified trend analysis with confidence scoring. Powered by AIsa — one API key, five data streams. Use when: the user needs X/Twitter research, monitoring, posting, or engagement workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### twitter

- Source: `targetSkills/twitter`
- Output: `claude-release/twitter`
- Description: Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### twitter-autopilot

- Source: `targetSkills/twitter-autopilot`
- Output: `claude-release/twitter-autopilot`
- Description: Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks for Twitter/X research, social listening, posting, or account interactions without sharing account passwords.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### twitter-command-center-search-post

- Source: `targetSkills/twitter-command-center-search-post`
- Output: `claude-release/twitter-command-center-search-post`
- Description: Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, or posting without sharing account passwords.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### twitter-command-center-search-post-interact

- Source: `targetSkills/twitter-command-center-search-post-interact`
- Output: `claude-release/twitter-command-center-search-post-interact`
- Description: Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### us-stock-analyst

- Source: `targetSkills/us-stock-analyst`
- Output: `claude-release/us-stock-analyst`
- Description: Professional US stock analysis with financial data, news, social sentiment, and multi-model AI. Comprehensive reports at $0.02-0.10 per analysis. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### web-search

- Source: `targetSkills/web-search`
- Output: `claude-release/web-search`
- Description: Search the web using AIsa Scholar Web endpoint. Returns structured web results with titles, URLs, and snippets. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### x-intelligence-automation

- Source: `targetSkills/x-intelligence-automation`
- Output: `claude-release/x-intelligence-automation`
- Description: Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: rewrote 1 markdown file(s) to reduce OpenClaw-specific release wording
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
- Residual risk: OAuth flow still requires the user to open the returned authorization URL manually.

### youtube

- Source: `targetSkills/youtube`
- Output: `claude-release/youtube`
- Description: YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only

### youtube-search

- Source: `targetSkills/youtube-search`
- Output: `claude-release/youtube-search`
- Description: YouTube Search API via AIsa unified endpoint. Search YouTube videos, channels, and playlists with a single AIsa API key — no Google API key or OAuth required. Use this skill when users want to search YouTube content. For other AIsa capabilities (LLM, financial data, Twitter, web search), see the aisa-core skill. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README

### youtube-serp

- Source: `targetSkills/youtube-serp`
- Output: `claude-release/youtube-serp`
- Description: Search YouTube SERP results through AISA for video research, channel discovery, trend checking, and competitor tracking. Use when: you need ranked YouTube results for a query, optionally filtered by country or language.
- Change: rewrote SKILL.md frontmatter for Claude-friendly search and invocation
- Change: stripped platform-specific metadata from release frontmatter
- Change: inferred allowed-tools for Claude Code compatibility
- Change: ensured description carries explicit trigger phrasing for search and selection
- Change: replaced source README with a Claude-oriented release README
- Change: copied runtime scripts/references only
