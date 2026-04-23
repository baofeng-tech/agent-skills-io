# last30days

`last30days` is the cross-platform mother skill for recent multi-source research.
It pulls evidence from Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News,
Polymarket, and grounded web search, then turns that into one ranked brief.

This repo keeps a conservative public variant on purpose:

- the shipped runtime is the stateless research CLI
- `AISA_API_KEY` is the only hosted credential
- repo-local config lives at `./.last30days-data/config.env`
- the broader upstream watchlist, briefing, GitHub-token, local store, and setup-wizard
  surfaces are not part of this public mother skill

## Quick Start

```bash
export AISA_API_KEY=sk-...
bash scripts/run-last30days.sh "OpenAI Agents SDK"
python3 scripts/last30days.py "Claude Code vs Codex" --emit=json
```

If you prefer a repo-local config file:

```bash
mkdir -p .last30days-data
printf 'AISA_API_KEY=sk-...\n' > .last30days-data/config.env
bash scripts/run-last30days.sh "Peter Steinberger"
```

## Common Commands

```bash
bash scripts/run-last30days.sh "$ARGUMENTS" --quick
bash scripts/run-last30days.sh "$ARGUMENTS" --deep
python3 scripts/last30days.py "$ARGUMENTS" --search=reddit,x,grounding
python3 scripts/last30days.py "$ARGUMENTS" --lookback-days=14
python3 scripts/last30days.py --diagnose
```

## What It Returns

- compact markdown by default
- JSON with `query_plan`, `ranked_candidates`, `clusters`, and `items_by_source`
- fail-soft output when one source times out but others still succeed

## Requirements

- Python 3.12+
- `bash`
- `AISA_API_KEY`

Reddit and Hacker News use public routes. Hosted planning, reranking, grounded web,
X/Twitter, YouTube, and Polymarket use AISA-backed endpoints.

## Conservative Public Boundary

This mother skill intentionally does not ship:

- the older watchlist workflow
- the briefing workflow
- GitHub-token-based retrieval as a required surface
- the local SQLite store workflow
- the interactive setup wizard and other dev-only helpers

That keeps the public runtime smaller, easier to audit, and more predictable across
ClawHub, Claude, Hermes, AgentSkill, AgentSkills.so, and GitHub-backed installs.
