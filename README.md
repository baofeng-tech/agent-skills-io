# agent-skills-io

Start here: [PROJECT_OVERVIEW.md](/mnt/d/workplace/agent-skills-io/PROJECT_OVERVIEW.md:1)

This repository is a temporary AIsa skills migration and packaging workbench.
It is used to:

- analyze legacy OpenClaw / ClawPub skill bundles
- convert them into cross-platform AgentSkills-style mother skills
- prepare conservative ClawHub upload variants
- document the migration, packaging, and publishing workflow

## AI Working Rule

Any AI or collaborator working in this repo should:

1. Read `PROJECT_OVERVIEW.md` before doing substantial work
2. Use it as the map of the project
3. Update it after structural, workflow, or output changes

More detailed repo rules live in [AGENTS.md](/mnt/d/workplace/agent-skills-io/AGENTS.md:1).

## Key Docs

- [Repo Runbook And Script Reference](/mnt/d/workplace/agent-skills-io/targets/repo-runbook-and-script-reference.md:1)
- [Platform Skill And Plugin Methodology](/mnt/d/workplace/agent-skills-io/targets/platform-skill-plugin-methodology.md:1)
- [Unified Pipeline And GitHub Actions](/mnt/d/workplace/agent-skills-io/targets/unified-pipeline-and-github-actions.md:1)

## Recommended Commands

Preview the next upstream sync:

```bash
python3 scripts/unified_skill_pipeline.py --dry-run
```

Sync upstream updates into `targetSkills/`, rebuild every release layer, and run validation:

```bash
python3 scripts/unified_skill_pipeline.py
```

Run a release-only rebuild from the current mother skills:

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

Check live ClawHub VirusTotal / OpenClaw verdicts from the saved publish state:

```bash
python3 scripts/clawhub_live_status.py --targets both
```

## Operational Notes

- `targetSkills/` is the mother-skill source of truth.
- For larger upstream deltas, `AIsa-team/agent-skills@main` is the authority to follow before reshaping into mother skills and downstream releases here.
- Generated release layers should be rebuilt from `targetSkills/`, not hand-edited as primary sources.
- Local credentials can be looked up from `example/accounts`, but CI should use secrets instead.
- `AIsa-team/agent-skills` is currently public, so `UPSTREAM_REPO_TOKEN` is optional fallback rather than a default requirement.
- Do not use `/mnt/d/workplace/agent-skills` as this repo's automation source; that local checkout is reserved for manual company-skill authoring/upload work.
- `.github/workflows/unified-skill-pipeline.yml` now supports:
  - hosted sync/build/test on schedule or manual dispatch
  - hosted suspicious diagnosis update (`targets/clawhub-suspicious-diagnosis.json`) plus optional diagnosis PR
  - self-hosted true publish for `AIsa-team/agent-skills` (`main` branch), `baofeng-tech/agent-skills-so`, `baofeng-tech/agent-skills`, Claude, Claude marketplace, Hermes, and optional ClawHub batch publish
  - optional self-hosted suspicious-remediation loop for targeted ClawHub artifacts such as `skill:aisa-twitter-api-command-center` and `plugin:aisa-twitter-engagement-suite-plugin`
- hosted upstream sync now targets `AIsa-team/agent-skills@main` by default
- workflow dispatch now supports explicit LLM refinement (`run_llm_step`, `llm_apply`, `sync_repo_skills`) before release rebuild/publish
- workflow dispatch now also supports targeted suspicious remediation (`run_suspicious_repair`, `suspicious_artifacts`) that can apply the repo-local skill-refinement helper and force a republish of matching artifacts
- `AISA_API_KEY` remains the shared runtime credential for published AISA API skills; the repo-local skill-refinement helper may borrow it by default, but it is documented and configured as a separate internal helper lane
- the repo-local skill-refinement helper defaults to shared `AISA_API_KEY` / `AISA_*`, supports explicit internal override via `SKILL_REFINER_API_KEY`, `SKILL_REFINER_BASE_URL`, and `SKILL_REFINER_MODEL`, and keeps legacy `AI_*` only as a last-resort compatibility fallback
- on this self-hosted runner, the workflow now falls back to `/mnt/d/workplace/agent-skills-io/example/accounts` for downstream GitHub PAT, ClawHub tokens, and skill-refiner config when those CI secrets are blank
- self-hosted downstream checkout now prefers public `https://github.com/<repo>.git` clone URLs, so repo preparation no longer blocks on `git@github-work` SSH timeouts before publish work even starts
- the hosted schedule currently runs every 4 hours via cron `21 */4 * * *`
- edit `.github/workflows/unified-skill-pipeline.yml` under `on.schedule[0].cron` if you want to change that hosted cadence later
- the hosted auto-commit path now avoids the earlier checkout post-job `exit code 128` by disabling persisted checkout credentials and pushing with an explicit token URL
- the self-hosted lane now fast-forwards its checkout to the latest `main` before downstream publish/remediation work so hosted auto-commits do not cause a later non-fast-forward push failure
- the workflow now also opts into Node 24 for JavaScript-based GitHub Actions to avoid the current hosted-run deprecation warning
- `scripts/publish_clawhub_batch.py` now supports optional `--post-publish-scan` checks so each publish can immediately probe the live ClawHub page for `VirusTotal`, `OpenClaw`, and `Suspicious` signals.
- `scripts/publish_clawhub_batch.py` now also supports repeated `--artifact` filters so workflow-driven remediation can republish only the affected ClawHub skill/plugin keys.
- if WSL-side ClawHub network access is flaky, this workspace can publish or scan through `cmd.exe /c ... py -3 scripts\\publish_clawhub_batch.py` and `scripts\\clawhub_live_status.py` on the Windows side without changing repo structure.
