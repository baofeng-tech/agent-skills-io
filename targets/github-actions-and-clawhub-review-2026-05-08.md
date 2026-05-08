# GitHub Actions And ClawHub Targeted Review 2026-05-08

## Scope

This pass answers the unresolved workflow and ClawHub questions from the May 2026 follow-up:

- whether the remote GitHub Actions workflow is currently successful
- whether the previous workflow fixes are fully verified
- rescan-first handling for:
  - `https://clawhub.ai/bibaofeng/twitter-aisa`
  - `https://clawhub.ai/plugins/last30days-slot2-plugin`
  - `https://clawhub.ai/plugins/@clawhub/aisa-twitter-api`
- senior test review of the workflow scripts
- AI engineering fixes for issues found during the review

## GitHub Actions Answer

Latest remote run checked before this pass:

- Run: `25460452313`
- Created: `2026-05-06T20:52:07Z`
- Conclusion: `failure`
- Failing job: `self-hosted-preflight`
- Hosted job result: `sync-build-test` succeeded
- Failure reason: schedule had `AUTO_FULL_PLATFORM_PUBLISH=true`, `AUTO_RUN_SUSPICIOUS_REPAIR=true`, and `AUTO_RUN_BREAKOUT_ROLLOUT=true`, but repository runner inventory had `total_count=0`.

Repo state after the previous fix:

- HEAD: `4b0cbe6310fba0ce46ba2b75eca008d3287a85cc15c64df0fe92b`
- Repo variables now show:
  - `AUTO_FULL_PLATFORM_PUBLISH=false`
  - `AUTO_RUN_SUSPICIOUS_REPAIR=false`
  - `AUTO_RUN_BREAKOUT_ROLLOUT=false`
- Runner inventory check: `GET /repos/baofeng-tech/agent-skills-io/actions/runners` returns `total_count=0`.

Initial conclusion before this pass was pushed:

- The latest remote run itself did not succeed.
- The failed run was on an older configuration/state before the current false-by-default self-hosted variables.
- The hosted build/test part is healthy.
- The self-hosted publish lanes are not "fully runnable" until a matching runner is actually registered and online.
- A current-HEAD remote validation run was required before saying the workflow was fully verified remotely.

Post-push validation:

- Run: `25512859636`
- Created: `2026-05-07T17:53:59Z`
- Head SHA: `8bdc42c12d1ce50a5642c28011f0db2b22cd9978`
- Conclusion: `success`
- `sync-build-test`: success
- `self-hosted-preflight`: success
- `self-hosted-publish`, `self-hosted-suspicious-repair`, `self-hosted-breakout-rollout`: skipped as expected because manual inputs requested no self-hosted lanes
- Note: the run's commit step produced follow-up commit `8c74e34581138dc2dbdacc06925934e78b81d681` with refreshed diagnosis outputs.

## Test Engineer Findings

### 1. No successful remote run exists for current HEAD

Severity: warning

The latest remote run initially failed before the repo-variable fix and before the local repair commit. Local workflow guard tests passed, and post-push run `25512859636` succeeded on the repair commit.

Fix:

- Recorded the exact run/head mismatch.
- Triggered a fresh remote validation run after the repair commit was pushed.

### 2. Self-hosted lanes are fixed as opt-in, but runner capacity is still zero

Severity: warning

The workflow behavior is now correct: requested self-hosted lanes fail fast when no runner can be confirmed. The environment is not ready for true self-hosted publishing because runner inventory is still zero.

Fix:

- Keep the three `AUTO_*` self-hosted variables false.
- Register an online repository-level runner before enabling them.

### 3. Scoped plugin URLs were parsed incorrectly in live-status checks

Severity: blocker

`scripts/clawhub_live_status.py` parsed `https://clawhub.ai/plugins/@clawhub/aisa-twitter-api` as plugin slug `@clawhub` instead of `@clawhub/aisa-twitter-api`.

Fix:

- Updated scoped plugin URL extraction.
- Added regression assertions in `scripts/test_clawhub_live_status_review.py`.

### 4. Exact repair of `@clawhub/aisa-twitter-api` is blocked by publisher scope

Severity: blocker

Rescan was requested successfully, but exact republish to `@clawhub/aisa-twitter-api` fails for all configured tokens with `Forbidden for "@clawhub"`.

Fix status:

- No fallback slug was used.
- The original URL remains pending plus ClawScan suspicious in live status.
- This needs the `@clawhub` publisher owner or ClawHub platform intervention.

### 5. Historical slot packages need explicit tracking

Severity: warning

`last30days-slot2-plugin` is not a generated canonical local artifact, but it is a real live URL. It needed exact package republish from the local `last30days-plugin` payload.

Fix:

- Republished exact package name `last30days-slot2-plugin` as `1.0.4`.
- Kept a targeted report instead of pretending this was the canonical `last30days-plugin`.

## ClawHub Target Results

### `skill:twitter-aisa`

- Rescan result: limit reached for current release
- Repair action: exact slug republish from local `clawhub-release/aisa-twitter-api`
- Published version: `1.0.5`
- Inspect: latest `1.0.5`, `moderation=null`
- Live status after publish: `vt=clean`, `clawscan=clean`, `static=clean`, `suspicious=0`

### `plugin:last30days-slot2-plugin`

- Rescan result: already in progress
- Repair action: exact package republish from local `last30days-plugin` payload
- Published version: `1.0.4`
- Inspect: latest `1.0.4`, `scanStatus=pending`
- Live status after publish: `vt=pending`, `clawscan=pending`, `static=clean`, `suspicious=0`

### `plugin:@clawhub/aisa-twitter-api`

- Rescan result: requested successfully
- Inspect after wait: latest `1.0.0`, `scanStatus=pending`
- Exact republish attempts: failed for all configured tokens
- Platform response: `Forbidden for "@clawhub"`
- Live status after rescan: `scanStatus=pending`, `clawscan=suspicious`, `static=clean`, `suspicious=1`
- Current blocker: original scoped package can only be repaired by the `@clawhub` publisher owner or ClawHub platform action.

## Validation

- `python3 scripts/test_github_actions_workflow.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_live_status_review.py`: passed
- `python3 -m py_compile scripts/clawhub_live_status.py scripts/test_clawhub_live_status_review.py`: passed

## Artifacts

- `targets/clawhub-rescan-artifacts.json`
- `targets/clawhub-live-status-targeted-2026-05-08.json`
- `targets/clawhub-targeted-republish-2026-05-08.json`
- `targets/clawhub-targeted-republish-last30days-slot2-2026-05-08.json`

## 2026-05-08 Follow-up: Auto Continuation Repair

### Why the downstream lanes were false

The successful schedule run `25520903382` was on head `747222cb60cc940cd4eed28b2a0f8fe63ff4cf7b`, while the repo had already advanced to `7500f41f211ee4f7f24903a5cfa076911c657825` after the hosted auto-commit. Its preflight reported all three continuation lanes as false because workflow-dispatch defaults and scheduled `AUTO_*` variable fallbacks were hard `false` values. The workflow did not inspect `targets/unified-pipeline-state.json`, diagnosis output, or breakout live status before deciding whether there was work to continue.

Current runner inventory during this follow-up was still `total_count=0`, so `SELF_HOSTED_RUNNER_RUNS_ON_JSON` could not queue a real self-hosted job by itself.

### Test Engineer Findings

1. Blocker: continuation decisions were switch-driven, not evidence-driven. A run with synced skills could still skip publish, suspicious repair, and breakout rollout if the three switches were false.
2. Blocker: manual dispatch could look successful while silently skipping the requested full flow, because the default values were false and the summary did not distinguish explicit skip from no work.
3. Warning: no online self-hosted runner exists, but the repo already has the secrets needed for hosted continuation. The workflow had no hosted fallback path for true continuation lanes.
4. Warning: breakout live drift was not used as a rollout signal; missing/fallback live slugs could stay stale until manually noticed.
5. Warning: prediction-market smoke tests treated a 200 non-JSON upstream response as a traceback hard failure instead of a structured external transient.
6. Blocker found during current-HEAD dispatch: adding a manual hosted-fallback input exceeded GitHub's 25-input limit for `workflow_dispatch`, so the workflow could not be dispatched until that input was removed.

### Engineering Fixes

- Added `scripts/plan_workflow_continuation.py`.
  - `publish=auto` requests continuation when synced/created skills or generated release-layer changes exist.
  - `suspicious=auto` requests remediation only for owned blocker suspicious artifacts.
  - `breakout=auto` requests rollout when a breakout source changed or a declared breakout live artifact is missing, pending, or suspicious.
- Changed manual continuation controls from boolean defaults to `auto` / `true` / `false` choices.
- Changed scheduled `AUTO_FULL_PLATFORM_PUBLISH`, `AUTO_RUN_SUSPICIOUS_REPAIR`, and `AUTO_RUN_BREAKOUT_ROLLOUT` fallbacks from `false` to `auto`.
- Updated the remote repository variables to `AUTO_FULL_PLATFORM_PUBLISH=auto`, `AUTO_RUN_SUSPICIOUS_REPAIR=auto`, `AUTO_RUN_BREAKOUT_ROLLOUT=auto`, and `AUTO_ALLOW_HOSTED_CONTINUATION=true`.
- Added hosted continuation fallback: when no matching self-hosted runner is online and fallback is enabled, continuation lanes run on `ubuntu-latest` instead of being silently skipped.
- Kept `workflow_dispatch` at 25 inputs by controlling hosted fallback only through `AUTO_ALLOW_HOSTED_CONTINUATION`; added a workflow guard for the input-count limit.
- Updated workflow guard tests to execute the planner against positive and no-work fixtures.
- Hardened prediction-market client JSON decoding across the prediction-market family and classified `UPSTREAM_NON_JSON` smoke output as transient.

### ClawHub Follow-up Result

- Owned suspicious repair auto-plan found no owned blocker suspicious artifacts after diagnosis.
- Breakout rollout published or confirmed 8 breakout artifacts.
- Rescan-first cleanup cleared the newly suspicious/pending breakout fallback artifacts:
  - `skill:aisa-twitter-research-engage-relay` now resolves to `https://clawhub.ai/bibaofeng/aisa-twitter-research-engage-relay-aisa-api` and is clean.
  - `plugin:aisa-twitter-research-engage-relay-plugin` now resolves to `https://clawhub.ai/plugins/aisa-twitter-research-engage-relay-aisa-api-plugin` and is clean.
- Current breakout variants in `targets/clawhub-live-status.json` are all clean.

### Validation

- `python3 scripts/test_github_actions_workflow.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_batch_publish_exit.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_live_status_review.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_plugin_auth_metadata.py`: passed.
- Full release rebuild plus `python3 scripts/test_release_layers.py`: passed with `structure_error_count=0`, `smoke_failure_count=0`, `smoke_transient_count=3`.

## 2026-05-08 Follow-up: Runner Clarity And Current Continuation State

### Current Remote State

- `git pull` returned `Already up to date`.
- Latest remote run checked in this pass: `25556988565`.
- Latest run head SHA: `26108947434216d559391f3839dbe01f280b4a36`.
- Current local `HEAD`: `26108947434216d559391f3839dbe01f280b4a36`.
- Latest run conclusion: `success`.
- Repository runner inventory: `total_count=0`.

### Test Engineer Findings

1. Warning: the workflow logic is healthy at current `HEAD`, but the repository still has no registered self-hosted runner. `SELF_HOSTED_RUNNER_RUNS_ON_JSON` only selects labels and does not create, register, or start a runner.
2. Warning: the preflight summary said `Can queue self-hosted jobs` even when hosted fallback made the continuation lanes runnable. That wording could be read as proof that a real self-hosted runner existed.
3. Current ClawHub diagnosis contains no owned suspicious blockers for `baofeng-tech`, `bibaofeng`, or `aisadocs`. The remaining suspicious blockers are external publisher URLs and should not be "fixed" by publishing fallback slugs.
4. Current breakout variants are clean in `targets/clawhub-live-status.json`; no rollout drift was found.

### Engineering Fix

- Updated `.github/workflows/unified-skill-pipeline.yml` preflight summary wording from `Can queue self-hosted jobs` to `Continuation lanes can run`.
- Added an explicit runner decision line for self-hosted match, hosted fallback, no-request, and unavailable states.
- Added a workflow guard assertion so the misleading wording cannot return.
- Documented the concrete conditions that make a self-hosted runner available or unavailable.
- After current-HEAD remote validation spent 23 minutes inside `Run AISA API skill regression`, bounded hosted AISA regression with CI-level timeout/retry/delay vars and added per-command progress logs.
- After run `25561267587` exposed a `subprocess.TimeoutExpired` crash on `prediction-market`, changed the regression harness so command timeouts become transient results and still produce a report.

### Local Checks

- `python3 scripts/plan_workflow_continuation.py --ignore-git-status`: no publish, suspicious repair, or breakout rollout requested.
- `python3 scripts/clawhub_suspicious_remediation.py --plan --owned-only --severity blocker --status suspicious`: selected `0` artifacts.
- `python3 scripts/clawhub_breakout_rollout.py --plan`: selected the 4 declared breakout variants, all already clean in live status.
- Canceled remote run `25559955152` after it revealed the unbounded practical runtime of the default AISA regression step; this was a test finding, not a workflow syntax failure.
