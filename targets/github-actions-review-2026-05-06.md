# GitHub Actions Review 2026-05-06

## Scope

Review target:

- `.github/workflows/unified-skill-pipeline.yml`
- `scripts/unified_skill_pipeline.py`
- self-hosted runner preflight and downstream publish token flow
- ClawHub publish lane behavior observed during the May 2026 repair run

## Run Status Checked

The previously reported `sync-build-test` failures are resolved in the current GitHub run records:

| Run | Current conclusion | `sync-build-test` | Notes |
| --- | --- | --- | --- |
| `25342426910` | success | success | self-hosted preflight succeeded; self-hosted publish lanes skipped |
| `25400865688` | success | success | self-hosted preflight succeeded; self-hosted publish lanes skipped |
| `25299535400` | cancelled | success | cancellation was in queued self-hosted work, not hosted build/test |
| `25289383679` | success | success | AISA regression skipped; three self-hosted jobs skipped |

## Findings

### 1. Runner label source was ambiguous

Severity: medium

The workflow previously allowed both `SELF_HOSTED_RUNNER_LABELS` and `SELF_HOSTED_RUNNER_RUNS_ON_JSON`. That made it possible for preflight to confirm one label set while `runs-on` queued against another.

Fix applied:

- `SELF_HOSTED_RUNNER_RUNS_ON_JSON` is now the single source.
- Preflight defaults to `["self-hosted"]`, matching the actual `runs-on` fallback.
- README and pipeline docs now describe only the JSON label source.

### 2. Preflight may fail when the token cannot see runner inventory

Severity: medium

The repository owner `baofeng-tech` is a GitHub user account, not an organization. In the checked environment:

- repo runner API returned zero visible runners
- org runner API is not applicable for this owner type

Why this can fail:

- no repo-level self-hosted runner is registered
- the runner is offline or removed
- labels in `SELF_HOSTED_RUNNER_RUNS_ON_JSON` do not all exist on an online runner
- `SELF_HOSTED_RUNNER_API_TOKEN` cannot read repo runner inventory
- the token is scoped to the wrong account/repo

Expected token permission:

- fine-grained PAT selected for `baofeng-tech/agent-skills-io`
- repository `Administration: read`
- metadata read

The workflow intentionally fails fast when self-hosted work is requested but runner confirmation fails. Use `AUTO_FORCE_SELF_HOSTED_QUEUE=true` only when you want to bypass confirmation and let GitHub queue the job anyway.

### 3. `GITHUB_TOKEN` and `SELF_HOSTED_RUNNER_API_TOKEN` are different things

Severity: medium

`github.token` / `GITHUB_TOKEN` inside Actions is generated per workflow run. It is not the same as a user-created PAT stored in `SELF_HOSTED_RUNNER_API_TOKEN`.

Use:

- `SELF_HOSTED_RUNNER_API_TOKEN`: read runner inventory for preflight.
- `DOWNSTREAM_REPO_TOKEN`: clone/fetch/push downstream publish repos.
- workflow `GITHUB_TOKEN`: normal current-repo checkout/status operations where GitHub grants enough scope.

### 4. Downstream push token needs explicit downstream repo access

Severity: medium

`DOWNSTREAM_REPO_TOKEN` should be a PAT that can read/write the downstream publish repositories used by sync jobs:

- `baofeng-tech/agent-skills-so`
- `baofeng-tech/agent-skills`
- `Aisa-One-Skills-Claude`
- `Aisa-One-Plugins-Claude`
- `Aisa-One-Skills-Hermes`

Recommended fine-grained PAT permissions:

- selected downstream repos
- Contents: read/write
- Metadata: read

It can be generated from GitHub personal access token settings. Do not assume it is identical to `SELF_HOSTED_RUNNER_API_TOKEN`; reuse only if its selected repos and permissions cover both jobs.

### 5. Python dependency list is for AISA-compatible runtimes, not OpenAI-only usage

Severity: low

The hosted/self-hosted bootstrap installs `PyYAML`, `openai`, `httpx`, and `requests`.

Meaning:

- `PyYAML`: parses workflow YAML/frontmatter.
- `requests`: used by multiple skill runtime clients and provider modules.
- `httpx`: used by some market/stock runtime checks.
- `openai`: used by OpenAI-compatible clients pointed at AISA/OpenAI-compatible endpoints such as `api.aisa.one`.

This does not require an OpenAI API key. AISA runtime lanes should continue to use `AISA_API_KEY`.

### 6. ClawHub package publish should not rely on old CLI behavior

Severity: medium

Local `clawhub` was `0.9.0`; current npm latest checked on 2026-05-06 is `0.12.3`. The older package publish command uploads files but does not use the newer ClawPack path and can leave registry metadata understated for complex plugin packages.

Fix applied:

- `scripts/publish_clawhub_batch.py` now supports `CLAWHUB_COMMAND`, for example:

```bash
CLAWHUB_COMMAND="npx -y clawhub@0.12.3" python3 scripts/publish_clawhub_batch.py ...
```

This lets CI or a one-off repair run use a pinned latest CLI without changing the global runner install.

## Follow-Up Risk

Self-hosted lanes are expected to fail fast when the runner cannot be confirmed. That is intentional. If a real runner exists, align `SELF_HOSTED_RUNNER_RUNS_ON_JSON` with the runner's actual labels and ensure `SELF_HOSTED_RUNNER_API_TOKEN` can read repository runners.
