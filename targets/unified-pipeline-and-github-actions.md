# Unified Pipeline And GitHub Actions

## What Was Added

This repo now has a unified scheduler:

- `scripts/unified_skill_pipeline.py`

It replaces the old fragmented flow of:

- manually checking upstream changes
- manually copying updated skills
- separately running build scripts
- separately remembering which publish steps are safe to continue

The scheduler handles one repeatable sequence:

1. locate upstream source
2. compare upstream baseline commit vs current commit
3. detect changed or new skills
4. sync safe skills into `targetSkills/`
5. normalize mother-skill frontmatter
6. rebuild the `targetSkills/` catalog
7. regenerate all release layers
8. run `scripts/test_release_layers.py`
9. optionally continue into sibling-repo sync or ClawHub batch publish

## Local Usage

### Preview the next sync

```bash
python3 scripts/unified_skill_pipeline.py \
  --upstream-local-path /mnt/d/workplace/agent-skills \
  --include-working-tree \
  --dry-run
```

### Sync current local upstream edits

```bash
python3 scripts/unified_skill_pipeline.py \
  --upstream-local-path /mnt/d/workplace/agent-skills \
  --include-working-tree
```

### Force a full upstream refresh

```bash
python3 scripts/unified_skill_pipeline.py \
  --upstream-local-path /mnt/d/workplace/agent-skills \
  --selection all
```

### Sync only selected skills

```bash
python3 scripts/unified_skill_pipeline.py \
  --upstream-local-path /mnt/d/workplace/agent-skills \
  --skills crypto-market-data,multi-source-search,youtube-serp
```

### Continue into local sibling-repo sync

```bash
python3 scripts/unified_skill_pipeline.py \
  --upstream-local-path /mnt/d/workplace/agent-skills \
  --include-working-tree \
  --sync-adjacent-repos
```

## Current Sync Decisions

As of 2026-04-23, the scheduler uses these repo-specific decisions:

### Auto-sync directly

- `crypto-market-data`
- `marketpulse`
- `media-gen`
- `multi-source-search`
- `perplexity-search`
- `prediction-market-arbitrage`
- `prediction-market-data`
- `twitter-autopilot`
- `youtube-serp`

### Manual review hold

- `last30days`

Why `last30days` stays on manual review:

- the upstream working tree currently includes extra briefing, watchlist, GitHub setup, and expanded helper surfaces
- this repo intentionally keeps a more conservative public mother-skill variant
- blindly copying the new upstream tree would broaden the shipped runtime and publish surface without a focused review

Current status of that hold:

- on 2026-04-23, this repo manually merged the safe subset of upstream `last30days` changes
- the public mother skill kept its stateless research CLI boundary
- safe parser compatibility updates were merged for date parsing and Polymarket field handling
- automatic upstream sync for `last30days` is still held, so future upstream changes continue to require manual review

## GitHub Actions

The repo includes:

- `.github/workflows/unified-skill-pipeline.yml`

The workflow now has two lanes:

- hosted lane
  - safe default for scheduled or manual sync, rebuild, validation, artifact upload, and committing generated outputs back into this repo
- optional self-hosted lane
  - manual-only continuation for downstream GitHub repo publish and optional ClawHub batch publish

### What the hosted lane does

1. checks out this repo
2. installs Python 3.12 plus `PyYAML`
3. fetches upstream `AIsa-team/agent-skills`
4. runs `scripts/unified_skill_pipeline.py`
5. uploads state and test artifacts
6. auto-commits regenerated outputs back into this repo when files changed

### What the self-hosted lane adds

When `run_self_hosted_publish=true` on a manual dispatch, the workflow also:

1. prepares downstream publish repos in a dedicated workspace area
2. reruns the unified pipeline with optional `--sync-adjacent-repos`
3. optionally continues into `publish_clawhub_batch.py`
4. commits and pushes changed downstream GitHub publish repos
5. uploads self-hosted publish-state artifacts

### Downstream repo preparation

The self-hosted lane now supports CI-injected publish destinations through:

- `PUBLISH_AGENT_SKILLS_DEST`
- `PUBLISH_CLAUDE_DEST`
- `PUBLISH_CLAUDE_MARKETPLACE_DEST`
- `PUBLISH_HERMES_DEST`

That lets the workflow publish into workspace-managed downstream clones instead of assuming a fixed local sibling layout.

## What The Workflow Assumes

### Hosted lane

It does not assume:

- a local sibling repo layout like `../Aisa-One-Skills-Claude`
- ClawHub CLI availability on the runner
- Hermes CLI availability on the runner
- direct publish credentials for every downstream platform

That makes the hosted lane safe for:

- upstream sync
- release regeneration
- regression detection
- committing generated outputs

### Self-hosted lane

The self-hosted lane closes the publish gap when the runner provides either:

- downstream GitHub auth via SSH, such as a configured `github-work` host alias
- or a `DOWNSTREAM_REPO_TOKEN` secret for cross-repo clone and push

If `clawhub_publish` is enabled, the runner also needs the `clawhub` CLI plus the relevant publish tokens.

## Secrets And Permissions

### Strongly recommended

- `AISA_API_KEY`
  - needed for smoke tests that hit real AIsa-backed runtime clients

### Required only when upstream Git access is not public

- `UPSTREAM_REPO_TOKEN`
  - used to clone `AIsa-team/agent-skills`

As of 2026-04-23, the upstream repo is publicly readable, so this token should be treated as optional fallback rather than a default requirement.

### Optional self-hosted publish secret

- `DOWNSTREAM_REPO_TOKEN`
  - used when the self-hosted runner cannot clone and push downstream repos through existing SSH auth

### Optional publish secrets

- `CLAWHUB_TOKEN`
- `CLAWHUB_TOKEN_2`
- `CLAWHUB_TOKEN_3`

## What Still Needs Your Help

These are environment-side tasks rather than repo-code tasks:

1. If `AIsa-team/agent-skills` ever becomes private to the runner, add `UPSTREAM_REPO_TOKEN`.
2. For self-hosted true publish, make sure the runner has either downstream Git SSH auth or `DOWNSTREAM_REPO_TOKEN`.
3. If you want ClawHub publish continuation in self-hosted mode, provide `CLAWHUB_TOKEN*` and the `clawhub` CLI runtime on that runner.
4. If you want GitHub Actions to push into sibling publish repos directly, confirm whether CI should mirror into:
   - `Aisa-One-Skills-Claude`
   - `Aisa-One-Plugins-Claude`
   - `Aisa-One-Skills-Hermes`
   - any public Agent Skills release repos

## Recommended Operating Model

### Scheduled GitHub Action

Use the hosted lane for:

- upstream diff detection
- mother-skill sync
- release rebuild
- smoke-test regression watch
- committing generated repo state

### Manual self-hosted publish continuation

Use the self-hosted lane for:

- `publish_clawhub_batch.py`
- downstream GitHub publish to `agent-skills`, Claude, Claude marketplace, and Hermes repos
- any step that needs live marketplace CLI auth or repo auth

Recommended manual-dispatch pattern:

- keep `dry_run=false`
- enable `run_self_hosted_publish=true`
- enable `sync_adjacent_repos=true` when you want downstream GitHub publish
- set `clawhub_publish=skill`, `plugin`, or `both` only when the self-hosted runner is ready for live publish
- keep `clawhub_dry_run=true` for the first publish rehearsal, then flip it to `false` for real continuation
