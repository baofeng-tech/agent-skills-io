---
name: aisa-tavily
description: 'AI-optimized web search via AIsa''s Tavily API proxy. Returns concise, relevant results for AI agents through AIsa''s unified API gateway. Use when: the user needs web search, research, source discovery, or content extraction.'
homepage: https://aisa.one
metadata:
  hermes:
    tags:
    - research
    - x
    - search
    - aisa
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# AIsa Tavily Search

AI-optimized web search using Tavily API through AIsa's unified gateway. Designed for AI agents - returns clean, relevant content.

## Search

```bash
node scripts/search.mjs "query"
node scripts/search.mjs "query" -n 10
node scripts/search.mjs "query" --deep
node scripts/search.mjs "query" --topic news
```

## Options

- `-n <count>`: Number of results (default: 5, max: 20)
- `--deep`: Use advanced search for deeper research (slower, more comprehensive)
- `--topic <topic>`: Search topic - `general` (default) or `news`
- `--days <n>`: For news topic, limit to last n days

## Extract content from URL

```bash
node scripts/extract.mjs "https://example.com/article"
```

Notes:
- Needs `AISA_API_KEY` from https://marketplace.aisa.one
- Powered by AIsa's unified API gateway (https://aisa.one)
- Use `--deep` for complex research questions
- Use `--topic news` for current events

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow is stateful, re-run a read/list/status command to verify the new state.
