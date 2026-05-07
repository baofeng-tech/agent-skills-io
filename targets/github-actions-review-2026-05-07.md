# GitHub Actions Review 2026-05-07

## Scope

This review answers the unresolved May 2026 workflow questions and records the fixes made in the same pass:

- run `25299535400` cancelled after hosted build/test success
- run `25289383679` succeeded while self-hosted jobs skipped
- run `25460452313` failed in `self-hosted-preflight`
- `baofeng-tech` owner type and organization-runner fallback behavior
- `SELF_HOSTED_RUNNER_API_TOKEN` and `DOWNSTREAM_REPO_TOKEN` fine-grained PAT requirements
- `skill:openclaw-twitter-post-engage` ClawHub suspicious remediation
- `stock-dividend-slot1` rename/remediation and `last30days-zh-plugin` Review/Suspicious remediation

## Run Answers

| Run | Observed state | Diagnosis | Fix status |
| --- | --- | --- | --- |
| `25299535400` | `sync-build-test` and preflight succeeded; `self-hosted-publish` queued for about 24 hours and the run concluded `cancelled` | This was not a hosted build/test bug. The manual run had `force_self_hosted_queue=true`, so preflight intentionally bypassed runner confirmation and let GitHub queue `runs-on: self-hosted`. No runner picked it up. | Normal result for forced queue with no available runner. Do not use force unless a runner is expected. Current workflow fails fast unless force is explicit. |
| `25289383679` | Scheduled run succeeded; `sync-build-test` succeeded; self-hosted publish, suspicious repair, and breakout jobs were skipped | This was old workflow behavior: scheduled self-hosted lanes were requested, but preflight could not confirm a runner and downstream `if` conditions skipped the lanes while the overall run stayed green. | Bug in the old flow. Current workflow fails fast when any self-hosted lane is requested but no matching runner can be confirmed. |
| `25460452313` | Scheduled run failed in `self-hosted-preflight`; `sync-build-test` succeeded first | This was not a `403`. The repo runner API was readable and current local verification returned `total_count=0`; no online repository self-hosted runner matched `["self-hosted"]`. `SELF_HOSTED_RUNNER_RUNS_ON_JSON` only chooses labels and does not register or start a runner. | Workflow defaults and repo variables were changed so scheduled self-hosted lanes are opt-in until an actual runner is online. |

## Token And Runner Conclusions

- `baofeng-tech` is a GitHub `User`, not an `Organization`.
- Organization runner fallback is therefore not applicable for `baofeng-tech/agent-skills-io`.
- Current workflow resolves the owner through `GET /users/{owner}` and only calls organization runner APIs when the owner type is `Organization`.
- Local `gh` runner inventory check can read `baofeng-tech/agent-skills-io` repository runners and returned `total_count=0`.
- Current state for the reported failure is therefore `200 with zero runners`, not `403`.
- GitHub Actions secrets cannot be introspected from the repo. If CI preflight reports `403`, then `SELF_HOSTED_RUNNER_API_TOKEN` still lacks selected-repo access, repository `Administration: read`, required SSO approval, or an equivalent permission path.
- A fine-grained `SELF_HOSTED_RUNNER_API_TOKEN` for this repo should select `baofeng-tech/agent-skills-io` and grant repository `Administration: read` plus Metadata read.
- `DOWNSTREAM_REPO_TOKEN` may be the same fine-grained PAT only if it also selects every downstream publish repo and grants Contents read/write plus Metadata read. If the same token is used for both roles, it must cover both runner inventory and downstream pushes.

## Current Live State Checked On 2026-05-07

- Repo variables now show `AUTO_FULL_PLATFORM_PUBLISH=false`, `AUTO_RUN_SUSPICIOUS_REPAIR=false`, and `AUTO_RUN_BREAKOUT_ROLLOUT=false`.
- `SELF_HOSTED_RUNNER_RUNS_ON_JSON` is still `["self-hosted"]`; this is only the requested runner label set.
- `gh api repos/baofeng-tech/agent-skills-io/actions/runners` currently returns `200` with `total_count=0`, so the current runner inventory condition is still no registered repository runner, not `403`.
- The latest failed scheduled run in this review window is `25460452313` from 2026-05-06, before those three AUTO vars were flipped to false; its failure was `no online repository self-hosted runner matched labels: ["self-hosted"]`.
- Hosted schedule still runs sync/build/test/diagnosis/AISA regression. The self-hosted lanes are requested only by manual dispatch inputs or by setting the corresponding `AUTO_*` repo variables true after a matching runner is online.

## Test Engineer Findings

### 1. Workflow runner-label contract needed a regression test

Risk: preflight could validate one label source while self-hosted jobs queued against another.

Fix:

- `SELF_HOSTED_RUNNER_RUNS_ON_JSON` is now the single source for preflight and all three self-hosted `runs-on` expressions.
- `scripts/test_github_actions_workflow.py` locks the guard behavior.
- Hosted CI runs this static workflow test before the pipeline body.

### 2. Self-hosted queue behavior needed explicit failure semantics

Risk: no-runner cases could either sit queued for 24 hours when forced or silently skip in the old scheduled flow.

Fix:

- Requested self-hosted lanes fail fast when `can_queue != true`.
- Manual `force_self_hosted_queue` remains supported, but the summary states that force was used.
- Personal-owner repos skip organization-runner fallback.

### 3. ClawHub batch publish had a false-negative exit path

Risk: a spare token `whoami` timeout could return process exit `1` even after the requested artifact was already published by another token.

Fix:

- `scripts/publish_clawhub_batch.py` now treats token login failure as worker unavailability, not an artifact failure.
- The command fails only when artifacts remain pending or an artifact-level publish fails.
- `scripts/test_clawhub_batch_publish_exit.py` covers the false-negative case.

### 4. Twitter public-write safety still had ambiguous post-mode surface

Risk: ClawHub flagged `skill:openclaw-twitter-post-engage` because public posting instructions mixed quote/default behavior and exposed too much credential context in CLI output.

Fix:

- Default post relationship is now reply-thread behavior, not quote.
- `--type quote` requires an explicit `--quote-tweet-url`.
- Long content continues as replies to the prior published tweet.
- CLI outputs report `aisa_api_key_present` instead of echoing the API key.
- Public writes still require `--confirm-public-write`.
- New `scripts/test_twitter_oauth_client_safety.py` locks these boundaries.

### 5. Suspicious remediation needed rescan-first behavior

Risk: ClawHub Review/Suspicious can clear after a platform rescan, so auto-remediation could make unnecessary package edits or republish a package that only needed rescan.

Fix:

- Added `scripts/clawhub_rescan_artifacts.py` for targeted skill/package rescan and post-wait inspect.
- `scripts/clawhub_suspicious_remediation.py` now supports `--rescan-before-repair` and the workflow suspicious lane passes it before editing or publishing.
- After the rescan wait, remediation refreshes live diagnosis and exits without edits if no selected suspicious source skill remains.

### 6. Targeted suspicious repair must not hide slug-owner failures

Risk: If the original owner token is unavailable, fallback publishing can create a clean replacement slug while the originally flagged URL remains suspicious.

Fix:

- Suspicious remediation now passes `--slug-conflict-strategy fail` by default.
- Product-style fallback slugs remain available for general publish/breakout work, but targeted repair of an existing URL should use the original owner token unless the user explicitly accepts a replacement slug.

### 7. ClawHub login timeout errors needed secret-safe wording

Risk: a timed-out CLI login can include the original command in the exception text, which may include a token argument.

Fix:

- `scripts/publish_clawhub_batch.py` and `scripts/clawhub_rescan_artifacts.py` now catch ClawHub login timeouts and report only the token slot.
- This preserves failure diagnostics without echoing credential-bearing command lines.

## ClawHub Result

- Local source and all generated release layers were rebuilt at `openclaw-twitter-post-engage` version `2.0.4`.
- `clawhub inspect openclaw-twitter-post-engage --json` now reports `latest: 2.0.4`.
- Live status after publish and follow-up refresh: `vt=clean`, `clawscan=clean`, `static=clean`, `suspicious=0`.
- The earlier `vt=pending` state cleared on the follow-up live-status refresh and was not the previous ClawScan suspicious reason.

## ClawHub Follow-up Result

- `stock-dividend-slot1` was renamed to `stock-dividend-aisa`; the old slug now resolves to the canonical `stock-dividend-aisa` page.
- `stock-dividend-aisa@1.0.2` is live latest under `baofeng-tech` and reports `vt=clean`, `clawscan=clean`, `static=clean`, `suspicious=0`.
- `last30days-zh-plugin` was republished as `1.0.9` after adding package-level provider/auth/environment metadata that ClawHub actually extracts into capabilities.
- `last30days-zh-plugin@1.0.9` now reports `clawscan=clean`, `openclaw=clean`, `static=clean`, `suspicious=0`; VirusTotal remains asynchronous `pending`, so it is tracked as `pending_scan` warning, not suspicious.

## Bibaofeng Targeted ClawHub Result

- `twitter-post-aisa` was rescanned first, then republished on the original slug as `1.0.3` after VirusTotal stayed suspicious; `clawhub inspect` confirms latest `1.0.3` and `moderation=null`. Live status is now `vt=pending`, `clawscan=clean`, `static=clean`, `suspicious=0`.
- `twitter-aisa` inspect confirms latest `1.0.2` with `moderation=null`.
- `aisa-perplexity-search-sonar-plugin` is live clean: `vt=clean`, `clawscan=clean`, `static=clean`.
- `aisa-tavily-search-plugin` stayed static-suspicious after rescan, so the ClawHub plugin payload now uses explicit `--aisa-api-key` arguments instead of JS `process.env` access; `1.0.3` is live clean.
- `last30days-plugin` was republished as `1.0.4` after the generated manifests began declaring optional `GH_TOKEN` / `GITHUB_TOKEN` and other optional last30days runtime envs; it is live clean.
- `aisa-twitter-research-engage-relay-plugin@1.0.6` is live clean.
- `@clawhub/prediction-market-arbitrage` inspect reports `scanStatus=clean`.
- `@clawhub/aisa-twitter-api` rescan was requested successfully; inspect still reports platform `scanStatus=pending`, not suspicious.

## Validation

- `scripts/test_github_actions_workflow.py`: passed
- `scripts/test_clawhub_batch_publish_exit.py`: passed
- `scripts/test_clawhub_plugin_auth_metadata.py`: passed
- `scripts/test_twitter_oauth_client_safety.py`: passed
- `scripts/test_release_layers.py`: structure errors `0`, smoke hard failures `0`, transient external failures `5` in the latest full run

## Remaining Watch Items

- Keep `scripts/clawhub_live_status.py --targets skill --artifact skill:openclaw-twitter-post-engage --include-status published --skill-owner aisadocs --render-mode always` as the verification command for future drift checks.
- If a real self-hosted runner exists, register it at repository level or align `SELF_HOSTED_RUNNER_RUNS_ON_JSON` with its actual labels.
- Keep `AUTO_FORCE_SELF_HOSTED_QUEUE=false` for scheduled runs unless intentionally waiting for a runner that will come online later.
- Keep `AUTO_FULL_PLATFORM_PUBLISH`, `AUTO_RUN_SUSPICIOUS_REPAIR`, and `AUTO_RUN_BREAKOUT_ROLLOUT` false until the runner inventory API shows an online matching runner.
