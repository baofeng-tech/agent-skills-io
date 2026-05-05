---
name: media-gen
description: 'Generate images and videos with AIsa using one API key. Supports Gemini image generation, Wan 2.7 image models, Seedream image generation, and Wan text-to-video / image-to-video variants, while routing each model to the correct AIsa endpoint automatically. Use when: you need a neutral cross-platform skill for creating images or videos from prompts or reference images through AIsa.'
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

Generate images and videos with AIsa using one API key. Supports Gemini image generation, Wan 2.7 image models, Seedream image generation, and Wan text-to-video / image-to-video variants, while routing each model to the correct AIsa endpoint automatically. Use when: you need a neutral cross-platform skill for creating images or videos from prompts or reference images through AIsa.

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
