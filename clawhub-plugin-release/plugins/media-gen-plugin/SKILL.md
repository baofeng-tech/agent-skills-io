---
name: media-gen-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `media-gen`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Generate images and videos with AIsa using one API key. Supports Gemini image generation, Wan 2.7 image models, Seedream image generation, and Wan text-to-video / image-to-video variants, while routing each model to the correct AIsa endpoint automatically. Use when: you need a neutral cross-platform skill for creating images or videos from prompts or reference images through AIsa.'
version: 1.0.0
license: MIT
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one
---

# Media Gen Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/media-gen/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
