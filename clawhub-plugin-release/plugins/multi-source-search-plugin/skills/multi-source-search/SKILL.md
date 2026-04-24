---
name: multi-source-search
description: 'Run confidence-scored multi-source retrieval through AIsa. Use when: the user needs cross-source verification, consensus checks, or one report that compares multiple search surfaces. Supports parallel retrieval, confidence scoring, and synthesis-ready outputs.'
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

# Multi-Source Search Verification Engine

Run confidence-scored multi-source retrieval through AIsa. Use when: the user needs cross-source verification, consensus checks, or one report that compares multiple search surfaces. Supports parallel retrieval, confidence scoring, and synthesis-ready outputs.

## When to use

- The user wants the same topic checked across multiple search surfaces instead of trusting one provider.
- The user needs confidence scoring, consensus checks, or a comparison across multiple search lanes.
- The user wants synthesis-ready validation before making a recommendation.

## High-Intent Workflows

- Run parallel retrieval and compare the returned signals.
- Check whether a claim appears across multiple search surfaces.
- Turn multi-source retrieval into a confidence-scored research brief.

## Quick Reference

- `python3 scripts/search_client.py --help`

## Setup

- `AISA_API_KEY` is required for AIsa-backed API access.
- Use repo-relative `scripts/` paths from the shipped package.
- Prefer explicit CLI auth flags when a script exposes them.

## Example Requests

- Compare how three search surfaces describe the latest browser-use agent products
- Verify whether a market claim appears in web, scholar, and cited answer results
- Run a confidence-scored research pass on multi-agent IDEs before writing a recommendation

## Guardrails

- Do not market this package as the generic one-search entry point.
- Do not claim consensus that the returned results do not support.
- If some providers time out, explain how that affects the score.
