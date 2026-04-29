# Repo Runbook And Script Reference

## Purpose

This document is the practical operator guide for this repository.

Use it when you need to:

- understand which directory is the source of truth
- know which script to run for import, build, test, or publish
- know which parameters matter
- avoid mixing mother skills with generated release layers

## Canonical Working Flow

1. Read `PROJECT_OVERVIEW.md`.
2. Update or import mother skills in `targetSkills/`.
3. Normalize frontmatter and rebuild the target catalog.
4. Generate platform release layers from `targetSkills/`.
5. Run `scripts/test_release_layers.py`.
6. Sync generated layers to external repos or publish to marketplaces only after the generated outputs pass validation.

## Credentials And Environment

### Local machine

- Local reference credentials live in `example/accounts`.
- Treat that file as local-only operational state.
- Do not echo its contents into generated docs, logs, or commits.

### CI / GitHub Actions

- Prefer GitHub Actions secrets instead of reading `example/accounts`.
- Typical secrets:
  - `AISA_API_KEY`
  - `UPSTREAM_REPO_TOKEN` only if `AIsa-team/agent-skills` stops being publicly readable
  - `DOWNSTREAM_REPO_TOKEN` for self-hosted downstream GitHub publish when SSH auth is unavailable
  - `CLAWHUB_TOKEN`, `CLAWHUB_TOKEN_2`, `CLAWHUB_TOKEN_3` for optional ClawHub publish
- Self-hosted runners can also publish downstream repos through existing SSH auth such as a local `github-work` host alias.

## Primary Scripts

### Orchestration

| Script | Use for | Key options |
| --- | --- | --- |
| `scripts/unified_skill_pipeline.py` | One entry point for upstream diff detection, mother-skill sync, build, test, and optional publish chaining | `--upstream-local-path`, `--selection`, `--skills`, `--include-working-tree`, `--sync-adjacent-repos`, `--clawhub-publish`, `--dry-run` |
| `scripts/one_click_distribute_all.sh` | Legacy local rebuild helper for full release regeneration | no args |

### Mother-Skill Catalog

| Script | Use for | Key options |
| --- | --- | --- |
| `scripts/normalize_target_skills.py` | Normalize `targetSkills/*/SKILL.md` frontmatter to the repo mother-skill standard | none |
| `scripts/build_targetskills_catalog.py` | Rebuild `targetSkills/index.json`, `index.md`, and `well-known-skills-index.json` | none |

### Import

| Script | Use for | Key options |
| --- | --- | --- |
| `scripts/import-agent-skills-own-to-targetSkills.sh` | Import sibling repo mother skills into `targetSkills/` | positional `source` and `dest`, `OVERWRITE_EXISTING=1` |
| `scripts/import-clawhub-downloads-to-targetSkills.py` | Import downloaded ClawHub zip bundles into `targetSkills/` | `--source`, `--dest`, `--overwrite-existing` |
| `scripts/import-github-downloads-to-targetSkills.py` | Import downloaded GitHub archives into `targetSkills/` | `--source`, `--dest`, `--overwrite-existing` |

### Build

| Script | Output | Notes |
| --- | --- | --- |
| `scripts/build_clawhub_release.py` | `clawhub-release/` | ClawHub-oriented skill layer |
| `scripts/build_clawhub_plugin_release.py` | `clawhub-plugin-release/` | Native-first / bundle-compatible plugin layer |
| `scripts/build_claude_release.py` | `claude-release/` | Claude / GitHub / skills.sh layer |
| `scripts/build_claude_marketplace.py` | `claude-marketplace/` | Claude plugin marketplace wrapper; depends on `claude-release/` |
| `scripts/build_hermes_release.py` | `hermes-release/` | Hermes category-organized runtime layer |
| `scripts/build_agentskills_so_release.py` | `agentskills-so-release/` | Agent Skills standards-first public layer |
| `scripts/build_agentskill_sh_release.py` | `agentskill-sh-release/` | agentskill.sh GitHub-import layer |

### Validation

| Script | Use for | Key options |
| --- | --- | --- |
| `scripts/test_release_layers.py` | Structure validation plus representative smoke tests across generated layers | none |
| `scripts/clawhub_live_status.py` | Resolve live ClawHub detail pages and record `VirusTotal` / `ClawScan` / `Static analysis` / `Suspicious` scan output into state | `--targets`, `--artifact`, `--include-status`, `--render-mode` |
| `scripts/clawhub_suspicious_remediation.py` | Select suspicious blocker artifacts, map them back to mother skills, optionally run the repo-local suspicious-remediation helper with diagnosis context, rebuild, sync, and force-republish only the targeted artifacts | `--artifacts`, `--contains`, `--apply`, `--llm-profile`, `--sync-repo-skills`, `--clawhub-publish`, `--post-publish-scan` |
| `scripts/clawhub_breakout_rollout.py` | Run the dedicated breakout lane from `targets/clawhub-breakout-variants.json`, then optionally rebuild, sync, and publish only those breakout variants | `--skills`, `--apply`, `--sync-repo-skills`, `--sync-adjacent-repos`, `--clawhub-publish` |

### Publish / Sync

| Script | Use for | Key options |
| --- | --- | --- |
| `scripts/publish-targetSkills-to-agent-skills.sh` | Compatibility alias for the agentskill.sh publish lane; rebuilds/syncs `agentskill-sh-release/` into `baofeng-tech/agent-skills` | same options as `publish-agentskill-sh-release.sh`, env `PUBLISH_AGENTSKILL_SH_DEST` |
| `scripts/publish-claude-release.sh` | Sync `claude-release/`, optionally `claude-marketplace/`, into sibling repos or CI-injected destinations | `--dest`, `--with-marketplace`, `--marketplace-only`, `--market-dest`, `--skip-build`, env `PUBLISH_CLAUDE_DEST`, `PUBLISH_CLAUDE_MARKETPLACE_DEST` |
| `scripts/publish-hermes-release.sh` | Sync `hermes-release/` into sibling repo, or optionally publish each generated skill via Hermes CLI | `--dest`, `--mode`, `--repo`, `--skip-build`, env `PUBLISH_HERMES_DEST`, `PUBLISH_HERMES_MODE`, `HERMES_PUBLISH_REPO` |
| `scripts/publish-clawhub-release.sh` | Prepare `clawhub-release/` for manual `clawhub skill publish` | `--skip-build` |
| `scripts/publish-clawhub-plugin-release.sh` | Prepare `clawhub-plugin-release/` for manual `clawhub package publish` | `--skip-build` |
| `scripts/publish-agentskills-so-release.sh` | Rebuild `agentskills-so-release/` and print the next public GitHub steps | `--skip-build` |
| `scripts/publish-agentskill-sh-release.sh` | Rebuild `agentskill-sh-release/` and print the next import/webhook steps | `--skip-build` |
| `scripts/publish_clawhub_batch.py` | Multi-token ClawHub batch publishing with stateful continuation | see detailed args below |
| `scripts/batch_publish_hermes_prs.py` | Batch-push Hermes `add-skill-*` branches and create publish PRs where possible | `skills...`, `--report` |

## Detailed CLI Parameters

### `scripts/unified_skill_pipeline.py`

| Option | Meaning |
| --- | --- |
| `--upstream-local-path <path>` | Use a local upstream checkout instead of cloning; avoid `/mnt/d/workplace/agent-skills` in this workspace because that repo is reserved for manual company upload work |
| `--upstream-repo-url <url>` | Git URL used when the scheduler clones or fetches upstream |
| `--upstream-branch <name>` | Upstream branch to diff against, default `main` |
| `--upstream-cache-dir <path>` | Clone/fetch cache dir used when no local path is provided |
| `--state-file <path>` | JSON file that stores the last synced commit and the last run summary |
| `--selection changed` | Sync only skills changed since the saved baseline commit |
| `--selection all` | Force a full upstream sync |
| `--skills a,b,c` | Sync only selected skills and ignore automatic diff selection |
| `--include-working-tree` | Include uncommitted upstream changes in the diff set |
| `--skip-build` | Skip all release-layer build steps after sync |
| `--skip-test` | Skip `scripts/test_release_layers.py` |
| `--sync-adjacent-repos` | Chain into downstream public repo sync scripts after build/test succeeds |
| `--adjacent-targets <csv>` | Limit downstream sync to `all`, `agentskills-so`, `agentskill-sh`, `claude`, `claude-marketplace`, and/or `hermes` |
| `--clawhub-publish skill|plugin|both` | Chain into `publish_clawhub_batch.py` |
| `--clawhub-dry-run` | Pass `--dry-run` when chaining into ClawHub batch publish |
| `--dry-run` | Show the sync plan without copying files or updating state |

### `scripts/publish_clawhub_batch.py`

| Option | Meaning |
| --- | --- |
| `--targets skill|plugin|both` | Which artifacts to publish |
| `--accounts-file <path>` | Optional local credentials file containing `clawhub_ApI_token*` entries |
| `--token <token>` | Repeatable token input for extra workers |
| `--state-file <path>` | Local publish state JSON |
| `--artifact <key>` | Only publish the specified artifact key such as `skill:search` or `plugin:twitter-plugin`; repeat to target more than one |
| `--config-root <path>` | Per-token ClawHub CLI config directory |
| `--skill-root <path>` | Skill publish source directory |
| `--plugin-root <path>` | Plugin publish source directory |
| `--source-repo-root <path>` | Git repo used for plugin source attribution |
| `--per-token-per-hour <int>` | Conservative hourly publish cap per token |
| `--worker-start-stagger-seconds <float>` | Delay between worker start times |
| `--tags <csv>` | Tags passed to publish commands |
| `--publish-timeout <seconds>` | Timeout for each publish command |
| `--probe-retries <int>` | Retry count for transient remote probe failures |
| `--probe-retry-delay <seconds>` | Delay between remote probe retries |
| `--post-publish-scan` | After publish or remote-existing skip, probe the live ClawHub page for scan status |
| `--slug-conflict-strategy fail\|suffix-by-slot` | How to handle ClawHub ownership or slug conflicts; default retries with a slot-specific fallback slug such as `-slot1`, `-slot2`, or `-slot3` |
| `--scan-retries <int>` | Retry count for post-publish live scan checks when scan output is still pending |
| `--scan-retry-delay <seconds>` | Delay between post-publish live scan retries |
| `--scan-render-mode off|auto|always` | Whether post-publish scan should use Playwright rendering for dynamic pages |
| `--scan-request-timeout <seconds>` | HTTP timeout for post-publish live scans |
| `--scan-render-timeout-ms <ms>` | Navigation timeout for Playwright-based live scans |
| `--scan-render-wait-ms <ms>` | Extra dynamic-page stabilization wait for Playwright-based live scans |
| `--scan-inspect-timeout <seconds>` | Timeout for `clawhub inspect` during post-publish skill URL resolution |
| `--scan-skill-owner <handle>` | Optional fallback owner hint for skill-page URL resolution during post-publish scans; repeat to add more candidates |
| `--skip-build` | Skip normalize/build before publish |
| `--force` | Ignore saved state and republish/reprobe everything |
| `--dry-run` | Probe and plan only, do not publish |

### `scripts/clawhub_live_status.py`

| Option | Meaning |
| --- | --- |
| `--state-file <path>` | Publish state JSON to read artifacts from and write back live scan results into |
| `--output-file <path>` | Standalone live-status JSON report |
| `--targets skill|plugin|both` | Which artifact kinds to scan |
| `--artifact <key>` | Optional artifact key such as `skill:search` or `plugin:twitter-plugin`; repeat as needed |
| `--include-status <status>` | Which publish-state statuses to include; repeat to include more than one |
| `--accounts-file <path>` | Optional local credentials file for skill URL resolution through `clawhub inspect` |
| `--token <token>` | Optional explicit ClawHub token for skill URL resolution |
| `--config-root <path>` | Temporary ClawHub CLI config directory for the scanner |
| `--render-mode off|auto|always` | Whether to use Playwright rendering when the detail page is dynamic |
| `--request-timeout <seconds>` | HTTP fetch timeout |
| `--render-timeout-ms <ms>` | Navigation timeout for Playwright rendering |
| `--render-wait-ms <ms>` | Extra wait window for dynamic HTML stabilization |
| `--inspect-timeout <seconds>` | Timeout for `clawhub inspect` during skill URL resolution |
| `--skill-owner <handle>` | Optional fallback owner hint for skill detail URLs when `clawhub inspect` does not resolve a page; repeat to add more candidates |

### `scripts/clawhub_suspicious_remediation.py`

| Option | Meaning |
| --- | --- |
| `--diagnosis-file <path>` | Input diagnosis JSON, usually `targets/clawhub-suspicious-diagnosis.json` |
| `--report-file <path>` | Output remediation-plan JSON |
| `--artifacts <csv>` | Exact suspicious artifact keys to target |
| `--contains <csv>` | Substring filter matched against key/name/reason/local path |
| `--owned-only` | Restrict automatic selection to self-owned artifacts |
| `--owner-handle <handle>` | Allowed publisher handles when `--owned-only` is enabled; defaults to `baofeng-tech`, `bibaofeng`, `aisadocs` |
| `--max-artifacts <int>` | Optional cap on the number of auto-selected artifacts |
| `--severity blocker|warning|all` | Which diagnosis severity to target |
| `--status suspicious|pending|any` | Which live scan state to target |
| `--apply` | Actually run LLM refinement and downstream rebuild/publish steps |
| `--llm-profile clawhub_suspicious\|clawhub_breakout` | Pick the suspicious-remediation or breakout profile; default is diagnosis-driven suspicious remediation |
| `--sync-repo-skills` | Refresh repo-local `.agents/skills` before refinement |
| `--llm-if-available` | Skip cleanly when LLM credentials are unavailable |
| `--sync-adjacent-repos` | Re-sync downstream publish repos after rebuilding |
| `--adjacent-targets <csv>` | Limit downstream sync to selected downstream targets |
| `--clawhub-publish skill|plugin|both|none` | Force-republish only the selected artifact keys |
| `--clawhub-dry-run` | Rehearse the targeted republish without uploading |
| `--post-publish-scan` | Probe live ClawHub scan output immediately after targeted republish |

### `scripts/clawhub_breakout_rollout.py`

| Option | Meaning |
| --- | --- |
| `--variants-file <path>` | Breakout declaration JSON, usually `targets/clawhub-breakout-variants.json` |
| `--report-file <path>` | Output breakout-rollout plan JSON |
| `--skills <csv>` | Optional source skill filter |
| `--apply` | Actually run breakout-profile refinement and rebuild/publish steps |
| `--sync-repo-skills` | Refresh repo-local `.agents/skills` before breakout refinement |
| `--llm-if-available` | Skip cleanly when LLM credentials are unavailable |
| `--sync-adjacent-repos` | Re-sync downstream publish repos after rebuilding |
| `--adjacent-targets <csv>` | Limit downstream sync to selected downstream targets |
| `--clawhub-publish skill|plugin|both|none` | Publish only the selected breakout skill/plugin slugs |
| `--clawhub-dry-run` | Rehearse the targeted breakout publish without uploading |
| `--post-publish-scan` | Probe live ClawHub scan output immediately after targeted breakout publish |

### `scripts/import-github-downloads-to-targetSkills.py`

| Option | Meaning |
| --- | --- |
| `--source <path>` | Source downloads directory |
| `--dest <path>` | Destination `targetSkills/` directory |
| `--overwrite-existing` | Replace existing target skill directories |

### `scripts/import-clawhub-downloads-to-targetSkills.py`

| Option | Meaning |
| --- | --- |
| `--source <path>` | Source ClawHub download directory |
| `--dest <path>` | Destination `targetSkills/` directory |
| `--overwrite-existing` | Replace existing target skill directories |

### `scripts/batch_publish_hermes_prs.py`

| Option | Meaning |
| --- | --- |
| `skills...` | Optional explicit skill list; default is all release skills without an open PR |
| `--report <path>` | JSON report output path |

## Common Commands

### Default upstream sync from GitHub

```bash
python3 scripts/unified_skill_pipeline.py
```

### Preview the next sync without touching files

```bash
python3 scripts/unified_skill_pipeline.py --dry-run
```

### Change the hosted GitHub Actions schedule

- File: `.github/workflows/unified-skill-pipeline.yml`
- Field: `on.schedule[0].cron`
- Current value: `21 */4 * * *`
- Meaning: hosted auto sync/build/test runs every 4 hours

### Rebuild all release layers from current `targetSkills/`

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
python3 scripts/test_release_layers.py
```

### Continue ClawHub publish safely

```bash
python3 scripts/publish_clawhub_batch.py --targets both --dry-run
python3 scripts/publish_clawhub_batch.py --targets skill --per-token-per-hour 4
python3 scripts/publish_clawhub_batch.py --targets plugin --per-token-per-hour 4
```

### Check live ClawHub scan status from saved publish state

```bash
python3 scripts/clawhub_live_status.py --targets both
python3 scripts/clawhub_live_status.py --targets skill --artifact skill:search
```

### Continue ClawHub publish and probe `VirusTotal` / `ClawScan` / `Static analysis` immediately after upload

```bash
python3 scripts/publish_clawhub_batch.py \
  --targets skill \
  --skip-build \
  --per-token-per-hour 4 \
  --post-publish-scan
```

### Windows-side fallback when WSL cannot reach ClawHub reliably

```bash
cmd.exe /c "cd /d D:\workplace\agent-skills-io && py -3 scripts\publish_clawhub_batch.py --targets both --skip-build --post-publish-scan"
cmd.exe /c "cd /d D:\workplace\agent-skills-io && py -3 scripts\clawhub_live_status.py --targets both --render-mode off"
```

## Operational Notes

- `targetSkills/` is the mother-skill source of truth.
- Do not hand-edit generated release layers when the real change belongs in `targetSkills/`.
- `scripts/build_claude_marketplace.py` must run after `scripts/build_claude_release.py`.
- `scripts/clawhub_live_status.py` now writes explicit `scan_status` values such as `pending` and `unresolved` instead of leaving those states implicit.
- If a ClawHub skill or plugin slug belongs to another publisher, prefer a ClawHub-only `clawhub-slug` alias in the mother skill rather than forcing a same-slug version bump.
- The unified pipeline intentionally separates:
  - upstream sync
  - mother-skill normalization
  - release generation
  - validation
  - optional publish chaining
