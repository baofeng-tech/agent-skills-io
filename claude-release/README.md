# Claude Release

This directory is a GitHub-ready Claude / skills.sh release layer generated from `targetSkills/`.

## Purpose

- Keep `targetSkills/` as the cross-platform mother-skill layer.
- Publish a cleaner Claude-oriented layer without OpenClaw-heavy frontmatter noise.
- Reduce obvious upload and trust-review risks by removing non-runtime files and home-directory defaults where practical.

## What Was Changed

- `SKILL.md` frontmatter was normalized to Claude-friendly fields such as `name`, `description`, `allowed-tools`, and optional `when_to_use`.
- Descriptions were normalized to include explicit trigger phrasing (`Use when:` / `触发条件：`) for better discoverability.
- Non-runtime files such as `__pycache__`, `*.pyc`, compare scripts, sync scripts, and test helpers were removed from release bundles.
- High-risk defaults were reduced for OAuth auto-open and home-directory persistence.

## Publishing To ClaudeMarketplaces

`claudemarketplaces.com` currently behaves like an index, not a manual upload console:

1. Publish this directory as a public GitHub repository.
2. Keep the skill directories at the repo root so each skill has `<skill>/SKILL.md`.
3. Seed installs through `skills.sh` or direct GitHub sharing so the repo becomes discoverable in the wider skills ecosystem.
4. Optionally create a separate Claude plugin marketplace repo later if you want `/plugin marketplace add owner/repo` distribution.

## Skill Count

- Generated skills: 51

## Validation

- Review `AUDIT.md` before publishing.
- Spot-check the highest-risk bundles first: Twitter, `last30days`, `stock-portfolio`, and `stock-watchlist`.
