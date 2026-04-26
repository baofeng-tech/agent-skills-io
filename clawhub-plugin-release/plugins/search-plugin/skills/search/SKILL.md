---
name: search
description: 'Run web, scholar, Tavily, and deep research through one AIsa search command center. Use when: the user needs one flagship skill for live search, source discovery, or citation-ready research. Supports fast lookup, answer generation, and deep research reports.'
author: AIsa
version: 1.0.0
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 🔎
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
    emoji: 🔎
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# AIsa Search Command Center

Run web, scholar, Tavily, and deep research through one AIsa search command center. Use when: the user needs one flagship skill for live search, source discovery, or citation-ready research. Supports fast lookup, answer generation, and deep research reports.

## When to use

- The user needs one flagship search skill for live lookup, source discovery, or citation-ready research.
- The user wants to move between web search, scholar search, Tavily, and deep research without switching packages.
- The user wants a search lane that can expand from fast lookup into broader synthesis.

## High-Intent Workflows

- Search quickly, then expand into cited answers.
- Pull academic or extracted-page evidence when the first pass needs stronger support.
- Turn a short query into a deep research report.

## Quick Reference

- `python3 scripts/search_client.py --help`

## Setup

- `AISA_API_KEY` is required for AIsa-backed API access.
- Use repo-relative `scripts/` paths from the shipped package.
- Prefer explicit CLI auth flags when a script exposes them.

## Example Requests

- Search the latest AI agent launches and show the most relevant sources first
- Find papers and cited analysis on multimodal reasoning from the last 18 months
- Build a deep research report on browser-use agents with sources and tradeoffs

## Guardrails

- Do not present test-only helpers as public features.
- Do not market cross-source consensus scoring as this package's primary lane.
- If some providers time out, report that honestly.
