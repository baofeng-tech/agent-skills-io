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

Current repo state after the previous fix:

- HEAD: `4b0cbe6310fba0ce46ba2b75eca008d3287a85cc15c64df0fe92b`
- Repo variables now show:
  - `AUTO_FULL_PLATFORM_PUBLISH=false`
  - `AUTO_RUN_SUSPICIOUS_REPAIR=false`
  - `AUTO_RUN_BREAKOUT_ROLLOUT=false`
- Runner inventory check: `GET /repos/baofeng-tech/agent-skills-io/actions/runners` returns `total_count=0`.

Conclusion:

- The latest remote run itself did not succeed.
- The failed run was on an older configuration/state before the current false-by-default self-hosted variables.
- The hosted build/test part is healthy.
- The self-hosted publish lanes are not "fully runnable" until a matching runner is actually registered and online.
- A current-HEAD remote validation run is still required before saying the workflow is fully verified remotely.

## Test Engineer Findings

### 1. No successful remote run exists for current HEAD

Severity: warning

The latest remote run failed before the current repo-variable fix and before the current local HEAD. Local workflow guard tests pass, but the remote workflow has not yet succeeded on `4b0cbe6`.

Fix:

- Record the exact run/head mismatch.
- Trigger a fresh remote validation run after this pass is committed and pushed.

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
