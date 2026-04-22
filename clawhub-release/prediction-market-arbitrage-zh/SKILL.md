---
name: prediction-market-arbitrage-zh
description: 通过 AIsa 查询股票、加密、预测市场与投资分析数据。触发条件：当用户需要市场研究、筛选、价格走势或组合分析时使用。支持研究与分析输出。
author: AIsa
version: 1.0.0
license: MIT
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 📊
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 📊
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# Prediction Market Arbitrage Zh

通过 AIsa 查询股票、加密、预测市场与投资分析数据。触发条件：当用户需要市场研究、筛选、价格走势或组合分析时使用。支持研究与分析输出。

## 适用场景

- 用户需要股票、加密、预测市场或投资研究数据。
- 用户需要价格、筛选、估值、组合或事件分析。
- 用户需要结构化金融输出用于进一步分析。

## 高意图工作流

- 查看价格走势与市场波动。
- 筛选符合条件的股票或币种。
- 研究组合、分红或预测市场机会。

## 快速命令

- `python3 scripts/arbitrage_finder.py --help`
- `python3 scripts/prediction_market_client.py --help`

## 配置

- 需要 `AISA_API_KEY` 才能访问 AIsa API。
- 使用公开包里的相对 `scripts/` 路径。
- 如果脚本提供显式鉴权参数，优先使用该参数。

## 示例请求

- 查询 NVDA 最近价格与分析师预期
- 找出符合某些财务条件的股票
- 查看 BTC 和 ETH 的最新市场数据

## 边界说明

- 不要给出虚构价格或财务数字。
- 不要把示例请求当成投资建议。
- 如果接口受限，要直接说明。
