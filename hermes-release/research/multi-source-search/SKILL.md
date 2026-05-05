---
name: multi-source-search
description: Multi-source search and answer generation for agents across web, scholar, Tavily, and Perplexity Sonar endpoints. Use when you need fast retrieval, citation-rich answers, or deeper research from one AIsa-backed skill.
license: MIT
metadata:
  aisa:
    emoji: 🛠
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
  hermes:
    tags:
    - research
    - x
    - search
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

# multi-source-search

Multi-source search and answer generation for agents across web, scholar, Tavily, and Perplexity Sonar endpoints. Use when you need fast retrieval, citation-rich answers, or deeper research from one AIsa-backed skill.

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Quick Reference

- `python3 scripts/search_client.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
