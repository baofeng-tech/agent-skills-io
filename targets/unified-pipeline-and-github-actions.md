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

The workflow now has one hosted lane plus three independent self-hosted lanes:

- hosted lane
  - safe default for scheduled or manual sync, rebuild, validation, artifact upload, and committing generated outputs back into this repo
- self-hosted publish lane
  - true publish continuation for downstream GitHub repo publish and optional ClawHub batch publish
  - can now also be auto-enabled from `schedule` through repo variable `AUTO_FULL_PLATFORM_PUBLISH=true`
- self-hosted suspicious-remediation lane
  - separate from the normal publish lane
  - can auto-select self-owned suspicious blockers and republish only that subset
- self-hosted breakout-rollout lane
  - separate from both normal publish and suspicious repair
  - runs the dedicated breakout path from `targets/clawhub-breakout-variants.json`

Current scheduler details:

- hosted lane cron is `21 19 * * *`
- that means the sync/build/test lane now runs once daily at 19:21 UTC
- edit `.github/workflows/unified-skill-pipeline.yml` under `on.schedule[0].cron` if you want to change that cadence later
- workflow-level env now pins `UPSTREAM_BRANCH=main`, so the scheduled sync follows the AIsa upstream `main` branch by default
- hosted auto-commit now uses `persist-credentials: false`, explicit token push, pre-commit `git rebase --autostash`, and push retry rebase; this avoids both the earlier `actions/checkout` post-job `exit code 128` cleanup failure and non-fast-forward races with other action commits
- schedule runs keep a shared concurrency group; manual dispatches use a per-run concurrency group so urgent manual repair does not sit behind the scheduled queue
- workflow-dispatch defaults now keep the publish, suspicious repair, breakout rollout, AISA API regression, and ClawHub CLI install switches open; self-hosted publish is still gated by the hosted preflight before any runner queue is created
- self-hosted publish, suspicious repair, and breakout rollout now pass through a hosted preflight first; if no online self-hosted runner matches `SELF_HOSTED_RUNNER_LABELS` (default `self-hosted`), the lane is skipped with a summary instead of sitting queued for 24 hours
- runner availability checks should use `SELF_HOSTED_RUNNER_API_TOKEN` with repository Administration read permission when the default `GITHUB_TOKEN` cannot call the runners API
- each self-hosted lane also has its own lane-level concurrency group and bounded runtime so manual reruns cannot stack overlapping publish/remediation work on the same branch
- generated root-flat ZIPs are now written with deterministic ordering, timestamps, and Git-index-derived executable bits so repeated release builds do not create binary churn when skill contents are unchanged, including on Windows-mounted worktrees
- workflow-level env also sets `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` to get ahead of the current GitHub-hosted Node 20 deprecation warning
- when no upstream skill changed but publish or downstream sync is explicitly requested, `scripts/unified_skill_pipeline.py` now continues from the current `targetSkills/` state instead of returning before publish

### What the hosted lane does

1. checks out this repo
2. installs Python 3.12 plus `PyYAML`
3. fetches upstream `AIsa-team/agent-skills`
4. runs `scripts/unified_skill_pipeline.py`
5. optionally runs the repo-local skill-refinement helper for changed AISA API skills (`--run-llm-step`)
6. refreshes ClawHub suspicious diagnosis JSON and rules-doc snapshot block
7. optionally runs read-only AISA-backed skill code regression and writes `targets/aisa-api-regression-report-YYYY-MM-DD.json`
8. uploads state and test artifacts
9. auto-commits regenerated outputs back into this repo when files changed

### Explicit LLM refinement step

The pipeline now supports an explicit model-execution stage between sync and build:

- `scripts/sync_codex_repo_skills.py`
  - syncs global `*-all` skills into `.agents/skills`
- `scripts/llm_refine_aisa_skills.py`
  - uses AISA/OpenAI-compatible endpoints to refine changed AISA API `targetSkills/*`
  - now supports profile selection:
    - `--profile source`
      - neutral mother-skill refinement for normal sync/build runs
    - `--profile clawhub_breakout`
      - ClawHub breakout refinement
    - `--profile clawhub_suspicious`
      - diagnosis-driven ClawHub suspicious remediation
  - supports:
    - `https://api.aisa.one/v1/responses`
    - `https://api.aisa.one/v1/chat/completions`
    - `https://api.aisa.one/v1/messages`
    - `https://api.aisa.one/v1/models/{model}:generateContent`
  - keeps the repo-local refinement helper separate from the published AISA API product skills
  - uses the shared AISA credential lane only:
    - `AISA_API_KEY`
    - optional `AISA_LLM_MODEL`
  - defaults to `gpt-5.4` only for this repo-local refinement helper; that model default must not be copied into shipped AISA API skill runtime scripts unless a specific runtime change is intentionally approved

In workflow-dispatch mode, the controls are:

- `run_llm_step`
- `llm_apply`
- `sync_repo_skills`

Current default behavior:

- normal hosted/self-hosted sync runs the helper with `--profile source`
- targeted ClawHub suspicious remediation runs the helper with `--profile clawhub_suspicious`

This split exists specifically to avoid mixing ClawHub breakout copy into the neutral mother-skill layer during routine syncs.

### Suspicious remediation loop

The self-hosted suspicious-remediation lane now supports an optional repair path for live ClawHub blockers:

- `scripts/clawhub_suspicious_remediation.py`
  - reads `targets/clawhub-suspicious-diagnosis.json`
  - selects matching `blocker` artifacts in `suspicious` state
  - maps them back to `targetSkills/*`
  - runs repo-local suspicious-remediation context via `scripts/llm_refine_aisa_skills.py --profile clawhub_suspicious`
  - rebuilds only `targetSkills/`, `clawhub-release/`, and `clawhub-plugin-release/`
  - optionally re-syncs downstream publish repos
  - optionally re-publishes only the selected artifact keys through `scripts/publish_clawhub_batch.py --artifact ... --force`

Current workflow-dispatch controls for this lane:

- `run_suspicious_repair`
- `suspicious_artifacts`
- `suspicious_max_artifacts`
- `adjacent_targets`
- `install_clawhub_cli`

Current scheduled default when no explicit artifact list is supplied:

- select self-owned `blocker` artifacts in `suspicious` state
- owner handles default to `baofeng-tech`, `bibaofeng`, and `aisadocs`
- optionally cap the batch with `AUTO_SUSPICIOUS_MAX_ARTIFACTS`

### Breakout rollout lane

The self-hosted breakout lane now has its own entry script:

- `scripts/clawhub_breakout_rollout.py`
  - reads `targets/clawhub-breakout-variants.json`
  - optionally filters by source skill
  - runs repo-local breakout context via `scripts/llm_refine_aisa_skills.py --profile clawhub_breakout`
  - rebuilds release layers
  - optionally re-syncs downstream publish repos
  - optionally publishes only the selected breakout skill/plugin slugs

Current workflow-dispatch controls for this lane:

- `run_breakout_rollout`
- `breakout_skills`
- `breakout_publish`
- `adjacent_targets`

### Suspicious diagnosis chain

The hosted lane now supports:

1. ClawHub live-status refresh (`scripts/clawhub_live_status.py`)
2. diagnosis JSON generation (`targets/clawhub-suspicious-diagnosis.json`)
3. optional rules-doc snapshot update in `targets/clawhub-suspicious-causes-and-fixes-2026-04-25.md`
4. direct hosted-lane auto-commit of regenerated diagnosis output when files changed

### Upstream-authority rule

For skill sync and future manual edits:

- if a skill already exists in `AIsa-team/agent-skills@main`, that upstream runtime is the first source to diff against
- publish-surface cleanup should preserve runtime completeness unless the task explicitly asks for a behavior change
- conservative narrowing belongs in generated release layers or manual-review exceptions, not as a silent breakage of the mother skill

### What the self-hosted lanes add

When `run_self_hosted_publish=true` on a manual dispatch, the workflow also:

1. prepares downstream public publish repos in a dedicated workspace area
2. reruns the unified pipeline with optional `--sync-adjacent-repos --adjacent-targets ...`
3. optionally continues into `publish_clawhub_batch.py`
4. commits self-hosted repo changes back into this repo when files changed
5. commits and pushes changed downstream GitHub publish repos
6. uploads self-hosted publish-state artifacts

When `run_suspicious_repair=true` on a manual dispatch, the workflow instead uses the dedicated suspicious-remediation lane:

1. fast-forwards to the latest repo state
2. optionally prepares only the selected downstream publish repos
3. auto-selects or explicitly targets suspicious artifacts
4. applies diagnosis-driven repair and force-republishes only that subset
5. commits repo and downstream changes separately

When `run_breakout_rollout=true` on a manual dispatch, the workflow uses the dedicated breakout lane:

1. fast-forwards to the latest repo state
2. reads `targets/clawhub-breakout-variants.json`
3. optionally filters to selected source skills
4. applies breakout-profile refinement, rebuilds, and optionally republishes only those breakout slugs

When repo variable `AUTO_FULL_PLATFORM_PUBLISH=true` is set, the same self-hosted lane can also run from the scheduled trigger without manual dispatch.

Self-hosted lane switches are intentionally "open but gated":

- manual dispatch can request publish, suspicious repair, and breakout rollout independently
- scheduled automation can request the same lanes through repo variables
- `self-hosted-preflight` checks the GitHub runner API before queueing any self-hosted job
- if a runner is intentionally expected to come online later, set manual `force_self_hosted_queue=true` or repo variable `AUTO_FORCE_SELF_HOSTED_QUEUE=true`

Useful repo variables for scheduled self-hosted automation:

- `AUTO_PIPELINE_DRY_RUN`
- `AUTO_PIPELINE_SELECTION`
- `AUTO_DIAGNOSIS_DOC_UPDATE`
- `AUTO_RUN_AISA_API_REGRESSION`
- `AUTO_RUN_LLM_STEP`
- `AUTO_LLM_APPLY`
- `AUTO_SYNC_REPO_SKILLS`
- `AUTO_SYNC_ADJACENT_REPOS`
- `AUTO_ADJACENT_TARGETS`
- `AUTO_PUSH_ADJACENT_REPOS`
- `AUTO_CLAWHUB_PUBLISH`
- `AUTO_CLAWHUB_DRY_RUN`
- `AUTO_RUN_SUSPICIOUS_REPAIR`
- `AUTO_SUSPICIOUS_ARTIFACTS`
- `AUTO_SUSPICIOUS_MAX_ARTIFACTS`
- `AUTO_RUN_BREAKOUT_ROLLOUT`
- `AUTO_BREAKOUT_SKILLS`
- `AUTO_BREAKOUT_PUBLISH`
- `AUTO_INSTALL_CLAWHUB_CLI`
- `AUTO_FORCE_SELF_HOSTED_QUEUE`
- `SELF_HOSTED_RUNNER_LABELS`
- `AUTO_HERMES_PUBLISH_MODE`
- `CLAWHUB_CLI_VERSION`

Before those publish/remediation steps, the self-hosted job now fast-forwards its checkout to the latest `main` using an explicit token URL. Before committing repo changes, each hosted and self-hosted commit step also fetches and rebases with `--autostash`, then retries push after another rebase if the remote advanced.

Why:

- the hosted lane may auto-commit regenerated repo state first
- without a fast-forward, the self-hosted job could later fail its own repo push with a non-fast-forward rejection
- without the pre-commit rebase/retry, independent workflow-generated commits can still race at push time

On this runner, the self-hosted lane now also supports a local credential fallback:

- if `DOWNSTREAM_REPO_TOKEN` or ClawHub tokens are blank in GitHub Actions secrets
- the job will try `/mnt/d/workplace/agent-skills-io/example/accounts`
- downstream repo preparation now prefers public `https://github.com/<repo>.git` clone URLs so repo sync does not stall on SSH timeout before publish starts

If ClawHub publishing is enabled, the self-hosted lane can now also optionally bootstrap the CLI first:

- `install_clawhub_cli=true` in workflow dispatch
- or `AUTO_INSTALL_CLAWHUB_CLI=true` in repo variables for scheduled publish
- current install path is `npm install -g clawhub@<version>`

Hermes publishing in this repo still defaults to syncing `hermes-release/` into its GitHub publish repo, and now also supports an optional `hermes_publish_mode=cli` path when the runner already has the Hermes CLI.

### Downstream repo preparation

The self-hosted lane now supports CI-injected publish destinations through:

- `PUBLISH_AGENTSKILLS_SO_DEST`
- `PUBLISH_AGENTSKILL_SH_DEST`
- `PUBLISH_CLAUDE_DEST`
- `PUBLISH_CLAUDE_MARKETPLACE_DEST`
- `PUBLISH_HERMES_DEST`

That lets the workflow publish into workspace-managed downstream clones instead of assuming a fixed local sibling layout.

Current downstream defaults are:

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
- optional real AISA skill-code regression reports
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
  - needed for optional skill-code regression checks that hit real AIsa-backed runtime clients

### Required only when upstream Git access is not public

- `UPSTREAM_REPO_TOKEN`
  - used to clone `AIsa-team/agent-skills`

As of 2026-04-23, the upstream repo is publicly readable, so this token should be treated as optional fallback rather than a default requirement.

### Optional self-hosted publish secret

- `SELF_HOSTED_RUNNER_API_TOKEN`
  - recommended for the hosted preflight when self-hosted lanes are enabled
  - needs repository Administration read permission to list self-hosted runners
- `DOWNSTREAM_REPO_TOKEN`
  - used when the self-hosted runner cannot clone and push downstream repos through existing SSH auth
  - also used as a fallback token for downstream clone/fetch/push URLs

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
- optional `scripts/test_aisa_api_skills.py` reports when `run_aisa_api_regression=true` or `AUTO_RUN_AISA_API_REGRESSION=true`
- committing generated repo state

### Manual self-hosted publish continuation

Use the self-hosted lane for:

- `publish_clawhub_batch.py`
- downstream GitHub publish to `agent-skills-so`, the public `baofeng-tech/agent-skills` import repo, Claude, Claude marketplace, and Hermes repos
- never for write-back into `AIsa-team/agent-skills`
- any step that needs live marketplace CLI auth or repo auth

Recommended manual-dispatch pattern:

- keep `dry_run=false`
- enable `run_self_hosted_publish=true`
- enable `sync_adjacent_repos=true` when you want downstream GitHub publish
- set `clawhub_publish=skill`, `plugin`, or `both` only when the self-hosted runner is ready for live publish
- keep `clawhub_dry_run=true` for the first publish rehearsal, then flip it to `false` for real continuation
- enable `run_suspicious_repair=true` plus an explicit `suspicious_artifacts=...` value when you want the runner to diagnose, minimally rewrite, and republish a ClawHub-owned live blocker set
