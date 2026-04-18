---
name: tavily-search
description: 'Advanced web search via Tavily through AIsa API. Supports search depth, topic filtering (general/news/finance), time ranges, domain inclusion/exclusion, and LLM-generated answers. Use when: the user needs web search, research, source discovery, or content extraction.'
metadata:
  hermes:
    tags:
    - finance
    - x
    - search
    - research
    - llm
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

# AIsa Tavily Search

Advanced web search powered by Tavily through the AIsa API. Offers fine-grained control over search depth, topic categories, time ranges, domain filtering, and optional LLM-generated answer summaries.

## Setup

This skill requires the `AISA_API_KEY` environment variable. When installed as a Claude plugin, the key is configured via the environment variables.

## Usage

Run the search client with the `tavily` subcommand:

```bash
python3 scripts/search_client.py tavily --query "<search query>" [options]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--query` / `-q` | Yes | — | Search query |
| `--count` / `-c` | No | 5 | Maximum results (1–20) |
| `--depth` | No | basic | Search depth: `basic`, `advanced`, `fast`, `ultra-fast` |
| `--topic` | No | — | Topic filter: `general`, `news`, `finance` |
| `--time-range` | No | — | Time range filter |
| `--include-answer` | No | false | Include an LLM-generated answer summary |

### Examples

```bash
# Basic search
python3 scripts/search_client.py tavily --query "OpenAI latest announcements" --count 10

# Advanced news search with answer
python3 scripts/search_client.py tavily --query "AI regulation 2026" --depth advanced --topic news --include-answer

# Finance-focused search
python3 scripts/search_client.py tavily --query "NVIDIA earnings Q1 2026" --topic finance --include-answer
```

## Output

The script prints structured results including:
- **Title** — Page title
- **URL** — Direct link
- **Date** — Publication date (when available)
- **Content** — Relevant excerpt
- **Answer** — LLM-generated summary (when `--include-answer` is used)

## When to Use

Use this skill when the user needs advanced search with specific filtering requirements: news-only results, finance-focused results, time-bounded searches, or when they want an AI-generated answer alongside raw results. This is the most feature-rich search tool in the plugin.

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow is stateful, re-run a read/list/status command to verify the new state.
