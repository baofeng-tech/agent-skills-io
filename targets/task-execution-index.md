# Task Execution Index

## What This Repo Is

`agent-skills-io` is an AIsa skill migration, packaging, validation, and publishing workbench.

It turns cross-platform mother skills in `targetSkills/` into generated release layers for:

- ClawHub skill uploads: `clawhub-release/`
- ClawHub native-first plugins: `clawhub-plugin-release/`
- Claude standalone skills: `claude-release/`
- Claude marketplace plugins: `claude-marketplace/`
- Hermes Hub/GitHub distribution: `hermes-release/`
- Agent Skills public catalogs: `agentskills-so-release/`
- agentskill.sh import: `agentskill-sh-release/`

## First Files To Read

For any multi-step task, read in this order:

1. `PROJECT_OVERVIEW.md`
2. `AGENTS.md`
3. `README.md`
4. this file
5. a relevant target doc under `targets/`

`PROJECT_OVERVIEW.md` is the high-level source of truth. This index is the execution shortcut.

## Work Type Routing

Use this routing before editing:

| Work type | Source of truth | Generated output |
| --- | --- | --- |
| mother skill work | `targetSkills/` | all release layers |
| ClawHub suspicious repair | `targetSkills/` plus diagnosis reports | `clawhub-release/`, `clawhub-plugin-release/` |
| ClawHub plugin packaging | `scripts/build_clawhub_plugin_release.py` and `clawhub-release/` | `clawhub-plugin-release/` |
| Claude/Hermes publish output | `targetSkills/` | `claude-release/`, `claude-marketplace/`, `hermes-release/` |
| public catalog output | `targetSkills/` | `agentskills-so-release/`, `agentskill-sh-release/` |
| CI/workflow repair | `.github/workflows/`, `scripts/unified_skill_pipeline.py`, `targets/unified-pipeline-and-github-actions.md` | workflow docs and test reports |
| methodology/docs | `targets/`, `platformDesc/`, repo docs | no release layer unless workflow changes |

Do not hand-edit generated release layers as the primary fix when the source should be `targetSkills/` or a build script.

## Standard Build Order

Use this order after skill or generator changes:

```bash
python3 scripts/normalize_target_skills.py
python3 scripts/build_targetskills_catalog.py
python3 scripts/build_clawhub_release.py
python3 scripts/build_clawhub_plugin_release.py
python3 scripts/build_claude_release.py
python3 scripts/build_claude_marketplace.py
python3 scripts/build_hermes_release.py
python3 scripts/build_agentskills_so_release.py
python3 scripts/build_agentskill_sh_release.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_github_actions_workflow.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_batch_publish_exit.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_live_status_review.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_plugin_auth_metadata.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_twitter_oauth_client_safety.py
python3 scripts/test_release_layers.py
python3 -m compileall -q scripts
```

Do not run `build_claude_marketplace.py` in parallel with `build_claude_release.py`; the marketplace builder reads `claude-release/`.

## CI And Secret Map

Important CI values:

- `SELF_HOSTED_RUNNER_RUNS_ON_JSON`: single source for self-hosted runner labels, for example `["self-hosted","linux","clawhub"]`. This only selects labels; it does not register or start a runner.
- `SELF_HOSTED_RUNNER_API_TOKEN`: PAT used only to confirm runner inventory.
- `DOWNSTREAM_REPO_TOKEN`: PAT used to clone/fetch/push downstream publish repos.
- `AISA_API_KEY`: runtime key for AISA-backed skill tests and refinements.
- `CLAWHUB_TOKEN`, `CLAWHUB_TOKEN_2`, `CLAWHUB_TOKEN_3`: ClawHub publish tokens.
- `CLAWHUB_CLI_VERSION`: optional CI-controlled ClawHub CLI version.

`GITHUB_TOKEN` in Actions is an auto-generated run token; do not treat it as the same secret as `SELF_HOSTED_RUNNER_API_TOKEN`.

For `baofeng-tech/agent-skills-io`, the owner is a GitHub `User`, not an organization. Repository runner discovery is the relevant API path; organization runner fallback is skipped unless `GET /users/{owner}` returns `Organization`.

Scheduled self-hosted publish, suspicious repair, and breakout rollout are opt-in. Keep `AUTO_FULL_PLATFORM_PUBLISH`, `AUTO_RUN_SUSPICIOUS_REPAIR`, and `AUTO_RUN_BREAKOUT_ROLLOUT` false until `GET /repos/baofeng-tech/agent-skills-io/actions/runners` shows an online runner matching `SELF_HOSTED_RUNNER_RUNS_ON_JSON`.

Fine-grained PAT guidance:

- `SELF_HOSTED_RUNNER_API_TOKEN`: select `baofeng-tech/agent-skills-io`, grant repository `Administration: read` plus Metadata read.
- `DOWNSTREAM_REPO_TOKEN`: select each downstream publish repo, grant Contents read/write plus Metadata read.
- Reuse one PAT only when it covers both permission sets and all selected repos.

## ClawHub Repair Loop

Use diagnosis first:

```bash
python3 scripts/clawhub_live_status.py --targets both --include-status published --render-mode auto
python3 scripts/clawhub_suspicious_diagnosis.py --doc-mode update
```

Before editing a suspicious artifact, request a platform rescan when possible:

```bash
CLAWHUB_COMMAND="npx -y clawhub@0.12.3" python3 scripts/clawhub_rescan_artifacts.py \
  --artifact plugin:<name> \
  --inspect-after \
  --wait-seconds 180
python3 scripts/clawhub_live_status.py --targets both --artifact plugin:<name> --include-status published --render-mode auto
python3 scripts/clawhub_suspicious_diagnosis.py --doc-mode update
```

If the rescan clears the artifact, stop. If it stays suspicious or pending, repair from `targetSkills/` or the generator and rebuild the ClawHub layers. For existing suspicious URLs, keep `--slug-conflict-strategy fail` unless the user explicitly accepts a replacement slug; a fallback slug does not repair the flagged URL.

For targeted publish:

```bash
python3 scripts/publish_clawhub_batch.py --targets both --skip-build --force --artifact plugin:<name> --post-publish-scan --scan-render-mode auto
```

When the local `clawhub` CLI is older than the registry behavior, prefer a pinned command:

```bash
CLAWHUB_COMMAND="npx -y clawhub@0.12.3" python3 scripts/publish_clawhub_batch.py ...
```

Owner/slug conflict fallback now prefers product-style suffixes (`-aisa`, `-aisa-api`, `-aisa-one`) instead of new `-slotN` names. Existing `-slotN` live slugs may still exist in state and should be renamed or superseded when the owning token is available.

After a targeted suspicious repair, confirm the public latest version, not only the version you just uploaded:

```bash
npx -y clawhub@0.12.3 inspect <slug> --json
python3 scripts/clawhub_live_status.py --targets skill --artifact skill:<slug> --include-status published --render-mode always
```

## Upstream Rule

When comparing or absorbing upstream runtime behavior, use:

- authoritative upstream: `https://github.com/AIsa-team/agent-skills`
- local cache if present: `.cache/upstream-agent-skills`

Do not use `/mnt/d/workplace/agent-skills` as automation input; that checkout is reserved for manual company-skill authoring and upload work.

## Stash Safety

If the worktree is dirty before a pull, create a named safety stash and record it. Drop only the temporary safety stash you created after the work is reconciled. Do not drop older user stashes.
