# Hermes Release Audit

- Skills converted: 54

## aisa-multi-search-engine

- Category: `research`
- Path: `hermes-release/research/aisa-multi-search-engine`
- Description: Multi-source search engine powered by AIsa API. Combines Tavily web search, Scholar academic search, Smart hybrid search, and Perplexity deep research — all through a single AIsa API key. Includes confidence scoring and AI synthesis. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## aisa-provider

- Category: `ai`
- Path: `hermes-release/ai/aisa-provider`
- Description: Configure AIsa as a first-class model provider for OpenClaw, enabling production access to major Chinese AI models (Qwen, DeepSeek, Kimi K2.5, Doubao) through official partnerships with Alibaba Cloud, BytePlus, and Moonshot. Use this skill when the user wants to set up Chinese AI models, configure AIsa API access, compare pricing between AIsa and other providers (OpenRouter, Bailian), switch between Qwen/DeepSeek/Kimi models, or troubleshoot AIsa provider configuration in OpenClaw. Also use when the user mentions AISA_API_KEY, asks about Chinese LLM pricing, Kimi K2.5 setup, or needs help with Qwen Key Account setup.
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: replaced source README with a Hermes-oriented release README

## aisa-tavily

- Category: `research`
- Path: `hermes-release/research/aisa-tavily`
- Description: AI-optimized web search via AIsa's Tavily API proxy. Returns concise, relevant results for AI agents through AIsa's unified API gateway. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: replaced source README with a Hermes-oriented release README

## aisa-twitter-api

- Category: `communication`
- Path: `hermes-release/communication/aisa-twitter-api`
- Description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth. Use when the user asks for Twitter research, monitoring, or posting without sharing passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## aisa-twitter-command-center

- Category: `communication`
- Path: `hermes-release/communication/aisa-twitter-command-center`
- Description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth. Use when the user asks for Twitter research, monitoring, or posting without sharing passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## aisa-twitter-engagement-suite

- Category: `communication`
- Path: `hermes-release/communication/aisa-twitter-engagement-suite`
- Description: Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_engagement_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## aisa-twitter-post-engage

- Category: `communication`
- Path: `hermes-release/communication/aisa-twitter-post-engage`
- Description: Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_engagement_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## aisa-youtube-search

- Category: `research`
- Path: `hermes-release/research/aisa-youtube-search`
- Description: Search YouTube videos, channels, and playlists through the AIsa YouTube relay with one API key. Use when the user asks for YouTube discovery, query expansion, or pagination without managing Google credentials.
- Change: replaced source README with a Hermes-oriented release README

## aisa-youtube-serp-scout

- Category: `research`
- Path: `hermes-release/research/aisa-youtube-serp-scout`
- Description: Search YouTube videos, channels, and trends through the AIsa YouTube SERP client. Use when the user asks for content research, competitor tracking, or trend discovery without managing Google credentials. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: patched Hermes runtime auth and storage defaults in scripts/youtube_client.py
- Change: replaced source README with a Hermes-oriented release README

## cn-llm

- Category: `ai`
- Path: `hermes-release/ai/cn-llm`
- Description: China LLM Gateway - Unified interface for Chinese LLMs including Qwen, DeepSeek, GLM, Baichuan. OpenAI compatible, one API Key for all models. Use when: the user needs model routing, provider setup, or Chinese LLM access guidance.
- Change: patched Hermes runtime auth and storage defaults in scripts/cn_llm_client.py
- Change: replaced source README with a Hermes-oriented release README

## crypto-market-data

- Category: `finance`
- Path: `hermes-release/finance/crypto-market-data`
- Description: Query real-time and historical cryptocurrency market data via CoinGecko — simple prices, coin details, historical charts, OHLC candles, token prices by contract address, market-cap rankings, exchange data and tickers, categories, trending searches, and crypto news. Use for crypto research, price tracking, on-chain token lookup, portfolio analysis, and market-cap screening. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/coingecko_client.py
- Change: replaced source README with a Hermes-oriented release README

## last30days

- Category: `communication`
- Path: `hermes-release/communication/last30days`
- Description: Research the last 30 days across Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, and grounded web search. Use when: the user needs recent multi-source research across the last 30 days.
- Change: removed 1 non-runtime generated/test files from the release bundle
- Change: replaced source README with a Hermes-oriented release README

## last30days-zh

- Category: `communication`
- Path: `hermes-release/communication/last30days-zh`
- Description: 聚合最近 30 天的 Reddit、X/Twitter、YouTube、TikTok、Instagram、Hacker News、Polymarket 和 web search 结果. Use when: the user needs recent multi-source research across the last 30 days.
- Change: removed 1 non-runtime generated/test files from the release bundle
- Change: replaced source README with a Hermes-oriented release README

## llm-router

- Category: `ai`
- Path: `hermes-release/ai/llm-router`
- Description: Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key. Use when: the user needs model routing, provider setup, or Chinese LLM access guidance.
- Change: patched Hermes runtime auth and storage defaults in scripts/llm_router_client.py
- Change: replaced source README with a Hermes-oriented release README

## market

- Category: `finance`
- Path: `hermes-release/finance/market`
- Description: Query real-time and historical financial data across equities and crypto—prices, market moves, metrics, and trends for analysis, alerts, and reporting. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/market_client.py
- Change: replaced source README with a Hermes-oriented release README

## marketpulse

- Category: `finance`
- Path: `hermes-release/finance/marketpulse`
- Description: Query real-time and historical financial data for equities—prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/market_client.py
- Change: replaced source README with a Hermes-oriented release README

## media-gen

- Category: `creative`
- Path: `hermes-release/creative/media-gen`
- Description: Generate images and videos with AIsa. Four image models (Google Gemini 3 Pro Image, Alibaba Wan 2.7 image + image-pro, ByteDance Seedream) and four Wan video variants (wan2.6/2.7 × t2v/i2v). One API key; the client routes each model to the correct endpoint automatically. Use when: the user needs AI image or video generation workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/media_gen_client.py
- Change: replaced source README with a Hermes-oriented release README

## multi-search

- Category: `research`
- Path: `hermes-release/research/multi-search`
- Description: Parallel multi-source search combining Web, Scholar, Smart, and Tavily results with confidence scoring and AI synthesis. Best for comprehensive research requiring cross-source validation. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## multi-source-search

- Category: `research`
- Path: `hermes-release/research/multi-source-search`
- Description: Multi-source intelligent search for agents. Retrieval across web, scholar, Tavily, and Perplexity Sonar models. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## openclaw-aisa-youtube-aisa

- Category: `research`
- Path: `hermes-release/research/openclaw-aisa-youtube-aisa`
- Description: Search YouTube videos, channels, and trends through the AISA YouTube SERP client. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: patched Hermes runtime auth and storage defaults in scripts/youtube_client.py
- Change: replaced source README with a Hermes-oriented release README

## openclaw-media-gen

- Category: `creative`
- Path: `hermes-release/creative/openclaw-media-gen`
- Description: Generate images and videos with AIsa. Four image models (Google Gemini 3 Pro Image, Alibaba Wan 2.7 image + image-pro, ByteDance Seedream) and four Wan video variants (wan2.6/2.7 × t2v/i2v). One API key; the client routes each model to the correct endpoint automatically. Use when: the user needs AI image or video generation workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/media_gen_client.py
- Change: replaced source README with a Hermes-oriented release README

## openclaw-search

- Category: `research`
- Path: `hermes-release/research/openclaw-search`
- Description: Intelligent search for agents. Multi-source retrieval with confidence scoring - web, academic, and Tavily in one unified API. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## openclaw-twitter

- Category: `communication`
- Path: `hermes-release/communication/openclaw-twitter`
- Description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AISA relay, then publish approved posts with OAuth. Use when: the user asks for Twitter/X research, monitoring, or posting without sharing passwords. Supports read APIs, authorization links, and media-aware posting.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## openclaw-twitter-post-engage

- Category: `communication`
- Path: `hermes-release/communication/openclaw-twitter-post-engage`
- Description: Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AISA relay. Use when: the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords. Supports read APIs, OAuth-gated posting, and follow or like operations.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_engagement_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## openclaw-youtube

- Category: `research`
- Path: `hermes-release/research/openclaw-youtube`
- Description: YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: patched Hermes runtime auth and storage defaults in scripts/youtube_client.py
- Change: replaced source README with a Hermes-oriented release README

## perplexity-research

- Category: `research`
- Path: `hermes-release/research/perplexity-research`
- Description: Deep research using Perplexity Sonar models via AIsa API. Provides synthesized answers with citations. Supports 4 models from fast to exhaustive deep research. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## perplexity-search

- Category: `research`
- Path: `hermes-release/research/perplexity-search`
- Description: Perplexity Sonar search and answer generation through AIsa. Use when the task is specifically to call Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, or Sonar Deep Research for citation-backed web answers, analytical reasoning, or long-form research reports.
- Change: patched Hermes runtime auth and storage defaults in scripts/perplexity_search_client.py
- Change: replaced source README with a Hermes-oriented release README

## prediction-market

- Category: `finance`
- Path: `hermes-release/finance/prediction-market`
- Description: Prediction markets data - Polymarket, Kalshi markets, prices, positions, and trades. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/prediction_market_client.py
- Change: replaced source README with a Hermes-oriented release README

## prediction-market-arbitrage

- Category: `finance`
- Path: `hermes-release/finance/prediction-market-arbitrage`
- Description: Find and analyze arbitrage opportunities across prediction markets like Polymarket and Kalshi. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/arbitrage_finder.py
- Change: patched Hermes runtime auth and storage defaults in scripts/prediction_market_client.py
- Change: replaced source README with a Hermes-oriented release README

## prediction-market-arbitrage-api

- Category: `finance`
- Path: `hermes-release/finance/prediction-market-arbitrage-api`
- Description: Find arbitrage opportunities across Polymarket and Kalshi prediction markets via AIsa API. Scan sports markets for cross-platform price discrepancies, compare real-time odds, verify orderbook liquidity. Use when user asks about: prediction market arbitrage, cross-platform price differences, sports betting arbitrage, odds comparison, risk-free profit, market inefficiencies.
- Change: patched Hermes runtime auth and storage defaults in scripts/arbitrage_finder.py
- Change: patched Hermes runtime auth and storage defaults in scripts/prediction_market_client.py
- Change: replaced source README with a Hermes-oriented release README

## prediction-market-arbitrage-zh

- Category: `finance`
- Path: `hermes-release/finance/prediction-market-arbitrage-zh`
- Description: 通过 AIsa API 发现 Polymarket 和 Kalshi 预测市场的套利机会。扫描体育市场跨平台价差、比较实时赔率、验证订单簿流动性。适用场景：预测市场套利、跨平台价差、体育博彩套利、赔率对比、无风险利润、市场低效。 Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/arbitrage_finder.py
- Change: patched Hermes runtime auth and storage defaults in scripts/prediction_market_client.py
- Change: replaced source README with a Hermes-oriented release README

## prediction-market-data

- Category: `finance`
- Path: `hermes-release/finance/prediction-market-data`
- Description: Prediction markets data - Polymarket, Kalshi markets, prices, positions, and trades. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/prediction_market_client.py
- Change: replaced source README with a Hermes-oriented release README

## prediction-market-data-zh

- Category: `finance`
- Path: `hermes-release/finance/prediction-market-data-zh`
- Description: 通过 AIsa API 查询跨平台预测市场数据。支持 Polymarket 和 Kalshi 的市场行情、价格、订单簿、K线、持仓和交易记录。适用场景：查询预测市场赔率、选举博彩、事件概率、市场情绪、Polymarket 价格、Kalshi 价格、体育博彩赔率、钱包盈亏、跨平台市场对比。 Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/prediction_market_client.py
- Change: replaced source README with a Hermes-oriented release README

## scholar-search

- Category: `research`
- Path: `hermes-release/research/scholar-search`
- Description: Search academic papers and scholarly articles via AIsa Scholar endpoint. Supports year range filtering for targeted research. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## search

- Category: `research`
- Path: `hermes-release/research/search`
- Description: Intelligent search for agents. Multi-source retrieval across web, scholar, Tavily, and Perplexity Sonar models. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## smart-search

- Category: `research`
- Path: `hermes-release/research/smart-search`
- Description: Intelligent hybrid search combining web and academic sources via AIsa Smart Search endpoint. Best when you need both web and scholarly results. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## stock-analysis

- Category: `finance`
- Path: `hermes-release/finance/stock-analysis`
- Description: Analyze stocks and cryptocurrencies with 8-dimension scoring via AIsa API. Provides BUY/HOLD/SELL signals with confidence levels, entry/target/stop prices, and risk flags. Supports single or multi-ticker analysis with optional fast mode and JSON output. Use when the user asks to analyze a stock, check a ticker, or compare investments.
- Change: patched Hermes runtime auth and storage defaults in scripts/analyze_stock.py
- Change: replaced source README with a Hermes-oriented release README

## stock-dividend

- Category: `finance`
- Path: `hermes-release/finance/stock-dividend`
- Description: Analyze dividend metrics for stocks via AIsa API. Provides yield, payout ratio, growth CAGR, safety score (0-100), income rating, and Dividend Aristocrat/King status. Use when the user asks about dividends, income investing, or dividend safety.
- Change: patched Hermes runtime auth and storage defaults in scripts/dividends.py
- Change: replaced source README with a Hermes-oriented release README

## stock-hot

- Category: `finance`
- Path: `hermes-release/finance/stock-hot`
- Description: Hot Scanner — find the most trending and high-momentum stocks and crypto right now via AIsa API. Top gainers, losers, most active by volume, crypto highlights, news catalysts, and top 5 watchlist picks. Use when the user asks about trending stocks, what's hot, market movers, or momentum plays.
- Change: patched Hermes runtime auth and storage defaults in scripts/hot_scanner.py
- Change: replaced source README with a Hermes-oriented release README

## stock-portfolio

- Category: `finance`
- Path: `hermes-release/finance/stock-portfolio`
- Description: Manage investment portfolios with live P&L tracking via AIsa API. Create, add, update, remove positions, rename, and show portfolio summary with real-time profit/loss. Use when the user wants to track investments, manage a portfolio, check P&L, or add/remove holdings.
- Change: switched default local storage to repo-local path in scripts/portfolio.py
- Change: patched Hermes runtime auth and storage defaults in scripts/portfolio.py
- Change: replaced source README with a Hermes-oriented release README

## stock-rumors

- Category: `finance`
- Path: `hermes-release/finance/stock-rumors`
- Description: Rumor Scanner — find early signals including M&A rumors, insider activity, analyst upgrades/downgrades, social whispers, and SEC/regulatory activity via AIsa API. Ranked by impact score. Use when the user asks about rumors, insider trading, M&A activity, analyst changes, or early market signals.
- Change: patched Hermes runtime auth and storage defaults in scripts/rumor_scanner.py
- Change: replaced source README with a Hermes-oriented release README

## stock-watchlist

- Category: `finance`
- Path: `hermes-release/finance/stock-watchlist`
- Description: Manage a stock/crypto watchlist with price target and stop-loss alerts via AIsa API. Add, remove, list, and check tickers with live price alerts. Use when the user wants to track stocks, set price alerts, manage a watchlist, or check triggered alerts.
- Change: switched default local storage to repo-local path in scripts/watchlist.py
- Change: patched Hermes runtime auth and storage defaults in scripts/watchlist.py
- Change: replaced source README with a Hermes-oriented release README

## tavily-extract

- Category: `research`
- Path: `hermes-release/research/tavily-extract`
- Description: Extract clean, readable content from one or more URLs using Tavily Extract via AIsa API. Useful for reading full articles without visiting the page. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## tavily-search

- Category: `finance`
- Path: `hermes-release/finance/tavily-search`
- Description: Advanced web search via Tavily through AIsa API. Supports search depth, topic filtering (general/news/finance), time ranges, domain inclusion/exclusion, and LLM-generated answers. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## twitter

- Category: `communication`
- Path: `hermes-release/communication/twitter`
- Description: Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_engagement_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## twitter-autopilot

- Category: `communication`
- Path: `hermes-release/communication/twitter-autopilot`
- Description: Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_engagement_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## twitter-command-center-search-post

- Category: `communication`
- Path: `hermes-release/communication/twitter-command-center-search-post`
- Description: Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, or posting without sharing account passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## twitter-command-center-search-post-interact

- Category: `communication`
- Path: `hermes-release/communication/twitter-command-center-search-post-interact`
- Description: Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_engagement_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## us-stock-analyst

- Category: `finance`
- Path: `hermes-release/finance/us-stock-analyst`
- Description: Professional US stock analysis with financial data, news, social sentiment, and multi-model AI. Comprehensive reports at $0.02-0.10 per analysis. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows.
- Change: patched Hermes runtime auth and storage defaults in scripts/stock_analyst.py
- Change: patched Hermes runtime auth and storage defaults in scripts/test_api_data.py
- Change: replaced source README with a Hermes-oriented release README

## web-search

- Category: `research`
- Path: `hermes-release/research/web-search`
- Description: Search the web using AIsa Scholar Web endpoint. Returns structured web results with titles, URLs, and snippets. Use when: the user needs web search, research, source discovery, or content extraction.
- Change: patched Hermes runtime auth and storage defaults in scripts/search_client.py
- Change: replaced source README with a Hermes-oriented release README

## x-intelligence-automation

- Category: `communication`
- Path: `hermes-release/communication/x-intelligence-automation`
- Description: Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords.
- Change: disabled browser auto-open in scripts/twitter_oauth_client.py
- Change: removed non-runtime documentation directories from the Hermes release bundle
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_engagement_client.py
- Change: patched Hermes runtime auth and storage defaults in scripts/twitter_oauth_client.py
- Change: replaced source README with a Hermes-oriented release README

## youtube

- Category: `research`
- Path: `hermes-release/research/youtube`
- Description: YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: patched Hermes runtime auth and storage defaults in scripts/youtube_client.py
- Change: replaced source README with a Hermes-oriented release README

## youtube-search

- Category: `communication`
- Path: `hermes-release/communication/youtube-search`
- Description: YouTube Search API via AIsa unified endpoint. Search YouTube videos, channels, and playlists with a single AIsa API key — no Google API key or OAuth required. Use this skill when users want to search YouTube content. For other AIsa capabilities (LLM, financial data, Twitter, web search), see the aisa-core skill. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: replaced source README with a Hermes-oriented release README

## youtube-serp

- Category: `research`
- Path: `hermes-release/research/youtube-serp`
- Description: YouTube SERP for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.
- Change: patched Hermes runtime auth and storage defaults in scripts/youtube_client.py
- Change: replaced source README with a Hermes-oriented release README
