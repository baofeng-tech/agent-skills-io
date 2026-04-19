---
name: last30days-zh
description: 聚合最近 30 天的 Reddit、X/Twitter、YouTube、TikTok、Instagram、Hacker News、Polymarket 和 web search 结果。触发条件：当用户需要 recent social research、人物近况、公司动态、竞品对比、发布反应、趋势扫描时使用。支持 AISA 规划、聚类、重排和 JSON 输出。
license: MIT
metadata:
  aisa:
    emoji: 🛠
    requires:
      bins:
      - python3
      - bash
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  hermes:
    tags:
    - communication
    - twitter
    - x
    - youtube
    - search
    - research
    - market
    - aisa
    related_skills:
    - search
    - aisa-multi-search-engine
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# last30days-zh

聚合最近 30 天的 Reddit、X/Twitter、YouTube、TikTok、Instagram、Hacker News、Polymarket 和 web search 结果。触发条件：当用户需要 recent social research、人物近况、公司动态、竞品对比、发布反应、趋势扫描时使用。支持 AISA 规划、聚类、重排和 JSON 输出。

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Quick Reference

- `bash scripts/run-last30days.sh --help`
- `python3 scripts/last30days.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
