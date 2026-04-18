---
name: aisa-youtube-search
description: Search YouTube videos, channels, and playlists through the AIsa YouTube relay with one API key. Use when the user asks for YouTube discovery, query expansion, or pagination without managing Google credentials.
license: MIT-0
metadata:
  hermes:
    tags:
    - research
    - x
    - youtube
    - search
    - video
    - aisa
    related_skills:
    - aisa-youtube-serp-scout
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# AIsa YouTube Search

Search YouTube videos, channels, and playlists through the AIsa YouTube relay with one API key.

## When to Use

- The user wants to search YouTube videos, channels, or playlists.
- The task needs region or language filters without direct Google API setup.
- The workflow can call the AIsa YouTube search endpoint with `AISA_API_KEY`.

## Pitfalls

- The user needs browser automation, local scraping, or direct YouTube account actions.
- The workflow must avoid sending search requests to `api.aisa.one`.
- The request depends on a local helper script that is not part of this package.

## Quick Reference

- Required environment variable: `AISA_API_KEY`
- Endpoint: `https://api.aisa.one/apis/v1/youtube/search`
- This package is curl-first and does not ship a local Python client.

## Setup

```bash
export AISA_API_KEY="your-key"
```

## Common Commands

```bash
curl -s "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=machine+learning+tutorial" \
  -H "Authorization: Bearer $AISA_API_KEY"

curl -s "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+news&gl=us&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"

curl -s "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=python+tutorial&sp=EgIQAQ%3D%3D" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## Capabilities

- Search YouTube SERP results with `q`
- Filter by locale with `gl` and `hl`
- Apply pagination or narrowing via `sp`
- Return structured results that may include `videos` or grouped `sections`

## Guardrails

- Do not ask for Google credentials or browser cookies.
- Do not claim a result is local-only when it depends on relay requests.
- Do not fabricate missing filters or parameters.

## Security Notes

- All search requests go to `api.aisa.one`.
- Required secret: `AISA_API_KEY`.
- This workflow does not require passwords, browser automation, or local scraping.

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow is stateful, re-run a read/list/status command to verify the new state.
