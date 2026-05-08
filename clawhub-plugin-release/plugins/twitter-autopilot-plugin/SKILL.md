---
name: twitter-autopilot-plugin
description: Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one/apis/v1/twitter. Native-first ClawHub plugin for `twitter-autopilot`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Reads and searches X (Twitter) data including profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Also supports posting, liking/unliking tweets, and following/unfollowing users after the user completes OAuth authorization. Use when the user needs Twitter/X research, social listening, publishing, or account interactions without sharing account passwords.
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
    optionalEnv:
    - TWITTER_RELAY_BASE_URL
    - TWITTER_RELAY_TIMEOUT
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one/apis/v1/twitter
primaryEnv: AISA_API_KEY
optionalEnv:
- TWITTER_RELAY_BASE_URL
- TWITTER_RELAY_TIMEOUT
networkTargets:
- https://api.aisa.one/apis/v1/twitter
---

# Twitter Autopilot Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/twitter-autopilot/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
