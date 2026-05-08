---
name: last30days
description: Research the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search. Returns a ranked, clustered brief with citations. Use when you need recent social evidence, competitor comparisons, launch reactions, trend scans, or person/company profiles.
license: MIT
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, bash, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.0
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills
  tags: x,youtube,search,research,market
  platforms: agentskills.io,agentskill.sh,github
  primary_env: AISA_API_KEY
allowed-tools: Read Bash Grep
---

# last30days 📰

**30-day multi-source research brief for autonomous agents. Powered by AIsa.**

Use this skill when you need a recent, cross-source view of a topic instead of a single search result or timeless reference. It pulls evidence from Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search, then merges the results into a ranked brief with citations.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- and other harnesses that implement the [Agent Skills specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY` (available at [aisa.one](https://aisa.one)).

## Example requests

### Trend scan
```text
"last30days OpenAI Agents SDK"
```

### Competitor comparison
```text
"last30days Claude Code vs Codex"
```

### Person or company profile
```text
"last30days Peter Steinberger"
```

### Launch reaction
```text
"last30days GPT-5 launch --deep"
```

### Prediction-market angle
```text
"last30days bitcoin price"
```

## Quick start

```bash
# 1. Export your AIsa key
export AISA_API_KEY=sk-...

# 2. First-run setup (interactive — picks planner / rerank / fun-scorer models)
bash scripts/run-last30days.sh setup

# 3. Research a topic
bash scripts/run-last30days.sh "OpenAI Agents SDK"
```

## Common flags

```bash
# Low-latency profile (fewer candidates per source)
bash scripts/run-last30days.sh "$ARGUMENTS" --quick

# Higher-recall profile
bash scripts/run-last30days.sh "$ARGUMENTS" --deep

# Machine-readable output (full plan + candidates + clusters)
bash scripts/run-last30days.sh "$ARGUMENTS" --emit=json

# Restrict to specific sources
bash scripts/run-last30days.sh "$ARGUMENTS" --search=reddit,x,grounding

# Check provider / source availability
bash scripts/run-last30days.sh --diagnose
```

## Inputs and outputs

**Input.** A topic, person, company, product, market, or comparison, for example `OpenAI Agents SDK`, `Claude Code vs Codex`, or `Peter Steinberger`.

**Output.** A markdown brief by default, or JSON with:

- `query_plan` — planner-generated subqueries and source weights
- `ranked_candidates` — reranked candidate pool with scores
- `clusters` — semantically grouped findings
- `items_by_source` — per-source item lists with dates, engagement, and URLs
- `provider_runtime` — which models and retrieval backends ran
- `errors_by_source` — source-level failures, if any

## Use when

- You need last-30-days evidence on a person, company, product, market, tool, or trend.
- You want a ranked competitor comparison, launch-reaction summary, creator/community sentiment scan, or shipping update.
- You want a structured JSON brief that another agent can consume.

## Not ideal when

- The question is timeless and does not depend on recent evidence.
- You only want one official source and do not want social or community signals.

## Capabilities

- **AISA-powered**: planner, reranker, fun-scorer, and hosted retrieval for X, YouTube, TikTok, Instagram, Polymarket, and grounded Tavily web search.
- **Public-source coverage**: Reddit and Hacker News work without extra credentials.
- **Optional GitHub coverage**: GitHub is enabled when `GH_TOKEN` or `GITHUB_TOKEN` is set.
- **Fail-soft behavior**: if one source errors or times out, the brief still renders from the remaining sources and notes the gap.

## Model configuration

The skill makes three LLM calls per run. Each role can be pinned independently via `~/.config/last30days/.env`:

```bash
LAST30DAYS_PLANNER_MODEL=qwen-flash           # fast + reliable JSON
LAST30DAYS_RERANK_MODEL=qwen-plus-2025-12-01  # quality ranking
LAST30DAYS_FUN_MODEL=qwen-flash               # cheap vibes
```

Or set `AISA_MODEL=...` to use one model across all three roles. Run `last30days setup` to choose interactively; the picker fetches the live catalog from [aisa.one/docs/guides/models](https://aisa.one/docs/guides/models).

## API reference

last30days calls the following AIsa endpoints directly. See the [full API reference](https://aisa.one/docs/api-reference) for the complete catalog.

- [OpenAI Chat / `createChatCompletion`](https://aisa.one/docs/api-reference/chat/createchatcompletion) — planner, reranker, fun-scorer
- [Twitter Advanced Search](https://aisa.one/docs/api-reference/twitter/get_twitter-tweet-advanced-search) — X retrieval
- [YouTube Search](https://aisa.one/docs/api-reference/search/get_youtube-search) — YouTube retrieval
- [Tavily Search](https://aisa.one/docs/api-reference/search/post_tavily-search) — grounded web
- [Polymarket Markets](https://aisa.one/docs/api-reference/prediction-market/get_polymarket-markets) — prediction-market retrieval

Reddit and Hacker News use their public APIs directly rather than an AISA proxy.

## Requirements

- **Python 3.12+**
- **`AISA_API_KEY`** — required. Get one at [aisa.one](https://aisa.one).
- **`GH_TOKEN` / `GITHUB_TOKEN`** — optional; enables the GitHub source.

```bash
# Pin an interpreter ≥ 3.12
for py in /usr/local/python3.12/bin/python3.12 python3.14 python3.13 python3.12 python3; do
  command -v "$py" >/dev/null 2>&1 || continue
  "$py" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' || continue
  LAST30DAYS_PYTHON="$py"
  break
done
```
