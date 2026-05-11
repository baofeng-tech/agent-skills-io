---
name: media-gen
description: 'Generate images and videos with AIsa. Supports Gemini, Wan, and Seedream image generation plus Wan text-to-video and image-to-video models. One API key; the bundled client routes each model to the correct endpoint automatically. Use when: you need a neutral AIsa media-generation skill that spans multiple model families without changing credentials or request flow.'
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
    - creative
    - x
    - image
    - video
    - aisa
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# media-gen

Generate images and videos with AIsa. Supports Gemini, Wan, and Seedream image generation plus Wan text-to-video and image-to-video models. One API key; the bundled client routes each model to the correct endpoint automatically. Use when: you need a neutral AIsa media-generation skill that spans multiple model families without changing credentials or request flow.

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Quick Reference

- `python3 scripts/media_gen_client.py --help`

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
