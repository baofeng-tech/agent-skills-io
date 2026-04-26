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
python3 scripts/unified_skill_pipeline.py --dry-run
```

### Sync from the default upstream GitHub repo

```bash
python3 scripts/unified_skill_pipeline.py
```

Current default upstream branch:

- `AIsa-team/agent-skills@main`

### Force a full upstream refresh

```bash
python3 scripts/unified_skill_pipeline.py --selection all
```

### Sync only selected skills

```bash
python3 scripts/unified_skill_pipeline.py \
  --skills crypto-market-data,multi-source-search,youtube-serp
```

### Continue into downstream repo sync

```bash
python3 scripts/unified_skill_pipeline.py \
  --sync-adjacent-repos
```

### Important local-repo note

Do not use `/mnt/d/workplace/agent-skills` as this repo's automation input in this environment.

Why:

- that checkout is reserved for manual company-skill authoring and upload work
- automation in this repo should fetch from `AIsa-team/agent-skills` directly so the baseline is stable and repeatable

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
- `last30days`
- `twitter-autopilot`
- `youtube-serp`

As of 2026-04-26, `last30days` no longer stays behind a scheduler-level manual-review hold.

What changed:

- this repo now follows `AIsa-team/agent-skills@main` directly for `last30days` during unified sync
- any conservative narrowing should happen in release-layer packaging, live diagnosis, or targeted suspicious remediation
- the mother skill should preserve upstream runtime completeness instead of silently lagging behind

## GitHub Actions

The repo includes:

- `.github/workflows/unified-skill-pipeline.yml`

The workflow now has two lanes:

- hosted lane
  - safe default for scheduled or manual sync, rebuild, validation, artifact upload, and committing generated outputs back into this repo
- self-hosted lane
  - true publish continuation for downstream GitHub repo publish and optional ClawHub batch publish

Current scheduler details:

- hosted lane cron is `21 */2 * * *`
- that means the sync/build/test lane now runs every 2 hours
- edit `.github/workflows/unified-skill-pipeline.yml` under `on.schedule[0].cron` if you want to change that cadence later
- workflow-level env now pins `UPSTREAM_BRANCH=main`, so the scheduled sync follows the AIsa upstream `main` branch by default
- hosted auto-commit now uses `persist-credentials: false` plus explicit token push, which avoids the earlier `actions/checkout` post-job `exit code 128` cleanup failure
- workflow-level env also sets `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` to get ahead of the current GitHub-hosted Node 20 deprecation warning

### What the hosted lane does

1. checks out this repo
2. installs Python 3.12 plus `PyYAML`
3. fetches upstream `AIsa-team/agent-skills`
4. runs `scripts/unified_skill_pipeline.py`
5. optionally runs explicit LLM refinement for changed AIsa-backed skills (`--run-llm-step`)
6. refreshes ClawHub suspicious diagnosis JSON and rules-doc snapshot block
7. uploads state and test artifacts
8. auto-commits regenerated outputs back into this repo when files changed

### Explicit LLM refinement step

The pipeline now supports an explicit model-execution stage between sync and build:

- `scripts/sync_codex_repo_skills.py`
  - syncs global `*-all` skills into `.agents/skills`
- `scripts/llm_refine_aisa_skills.py`
  - uses AISA/OpenAI-compatible endpoints to refine changed AIsa-backed `targetSkills/*`
  - supports:
    - `https://api.aisa.one/v1/chat/completions`
    - `https://api.aisa.one/v1/messages`
    - `https://api.aisa.one/v1/models/{model}:generateContent`
  - supports fallback env config:
    - `AI_BASE_URL`
    - `AI_API_KEY`
    - `AI_MODEL`

In workflow-dispatch mode, the controls are:

- `run_llm_step`
- `llm_apply`
- `sync_repo_skills`

### Suspicious remediation loop

The self-hosted lane now also supports an optional repair path for live ClawHub blockers:

- `scripts/clawhub_suspicious_remediation.py`
  - reads `targets/clawhub-suspicious-diagnosis.json`
  - selects matching `blocker` artifacts in `suspicious` state
  - maps them back to `targetSkills/*`
  - runs repo-local `.agents/skills` context plus `scripts/llm_refine_aisa_skills.py`
  - rebuilds every release layer
  - optionally re-syncs downstream publish repos
  - optionally re-publishes only the selected artifact keys through `scripts/publish_clawhub_batch.py --artifact ... --force`

Current workflow-dispatch controls for this lane:

- `run_suspicious_repair`
- `suspicious_artifacts`

Current default targeted blocker set:

- `skill:aisa-twitter-api`
- `plugin:aisa-twitter-engagement-suite-plugin`

### Suspicious diagnosis chain

The hosted lane now supports:

1. ClawHub live-status refresh (`scripts/clawhub_live_status.py`)
2. diagnosis JSON generation (`targets/clawhub-suspicious-diagnosis.json`)
3. optional rules-doc snapshot update in `targets/clawhub-suspicious-causes-and-fixes-2026-04-25.md`
4. optional PR creation for diagnosis-only updates (`diagnosis-pr` job)

### Upstream-authority rule

For skill sync and future manual edits:

- if a skill already exists in `AIsa-team/agent-skills@main`, that upstream runtime is the first source to diff against
- publish-surface cleanup should preserve runtime completeness unless the task explicitly asks for a behavior change
- conservative narrowing belongs in generated release layers or manual-review exceptions, not as a silent breakage of the mother skill

### What the self-hosted lane adds

When `run_self_hosted_publish=true` on a manual dispatch, the workflow also:

1. prepares downstream publish repos in a dedicated workspace area
2. reruns the unified pipeline with optional `--sync-adjacent-repos`
3. optionally continues into `publish_clawhub_batch.py`
4. optionally runs the suspicious-remediation loop and force-republishes only the matching artifacts
5. commits self-hosted repo changes back into this repo when files changed
6. commits and pushes changed downstream GitHub publish repos
7. uploads self-hosted publish-state artifacts

Before those publish/remediation steps, the self-hosted job now fast-forwards its checkout to the latest `main` using an explicit token URL.

Why:

- the hosted lane may auto-commit regenerated repo state first
- without a fast-forward, the self-hosted job could later fail its own repo push with a non-fast-forward rejection

On this runner, the self-hosted lane now also supports a local credential fallback:

- if `DOWNSTREAM_REPO_TOKEN`, ClawHub tokens, or `AI_*` config are blank in GitHub Actions secrets
- the job will try `/mnt/d/workplace/agent-skills-io/example/accounts`
- downstream repo preparation now prefers public `https://github.com/<repo>.git` clone URLs so repo sync does not stall on SSH timeout before publish starts

### Downstream repo preparation

The self-hosted lane now supports CI-injected publish destinations through:

- `PUBLISH_AGENT_SKILLS_DEST`
- `PUBLISH_AGENTSKILLS_SO_DEST`
- `PUBLISH_AGENTSKILL_SH_DEST`
- `PUBLISH_CLAUDE_DEST`
- `PUBLISH_CLAUDE_MARKETPLACE_DEST`
- `PUBLISH_HERMES_DEST`

That lets the workflow publish into workspace-managed downstream clones instead of assuming a fixed local sibling layout.

Current downstream defaults are:

- `AIsa-team/agent-skills` on branch `main`
- `baofeng-tech/agent-skills-so` on branch `main`
- `baofeng-tech/agent-skills` on branch `main`
- `baofeng-tech/Aisa-One-Skills-Claude` on branch `main`
- `baofeng-tech/Aisa-One-Plugins-Claude` on branch `main`
- `baofeng-tech/Aisa-One-Skills-Hermes` on branch `main`

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

### Practical fallback for this workspace

In this repo's current environment, WSL/Linux HTTP access to some `clawhub.ai` endpoints can be flaky even when the same machine's Windows side can reach them.

That means a valid self-hosted operating pattern is:

- keep source generation in this repo as usual
- invoke `py -3 scripts/publish_clawhub_batch.py` or `py -3 scripts/clawhub_live_status.py` through `cmd.exe /c` from the Windows side when live ClawHub publish or scan calls need reliable network access

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
- downstream GitHub publish to the official `AIsa-team/agent-skills@agentskills`, `agent-skills-so`, the public `baofeng-tech/agent-skills` import repo, Claude, Claude marketplace, and Hermes repos
- any step that needs live marketplace CLI auth or repo auth

Recommended manual-dispatch pattern:

- keep `dry_run=false`
- enable `run_self_hosted_publish=true`
- enable `sync_adjacent_repos=true` when you want downstream GitHub publish
- set `clawhub_publish=skill`, `plugin`, or `both` only when the self-hosted runner is ready for live publish
- keep `clawhub_dry_run=true` for the first publish rehearsal, then flip it to `false` for real continuation
- enable `run_suspicious_repair=true` plus `suspicious_artifacts=skill:aisa-twitter-api,plugin:aisa-twitter-engagement-suite-plugin` when you want the runner to diagnose, minimally rewrite, and republish that live blocker set
