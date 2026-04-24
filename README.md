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
- For larger upstream deltas, `AIsa-team/agent-skills` is the authority to follow before reshaping into mother skills and downstream releases here.
- Generated release layers should be rebuilt from `targetSkills/`, not hand-edited as primary sources.
- Local credentials can be looked up from `example/accounts`, but CI should use secrets instead.
- `AIsa-team/agent-skills` is currently public, so `UPSTREAM_REPO_TOKEN` is optional fallback rather than a default requirement.
- Do not use `/mnt/d/workplace/agent-skills` as this repo's automation source; that local checkout is reserved for manual company-skill authoring/upload work.
- `.github/workflows/unified-skill-pipeline.yml` now supports:
  - hosted sync/build/test on schedule or manual dispatch
  - self-hosted true publish for `AIsa-team/agent-skills` (`agentskills` branch), `baofeng-tech/agent-skills-so`, `baofeng-tech/agent-skills`, Claude, Claude marketplace, Hermes, and optional ClawHub batch publish
- `scripts/publish_clawhub_batch.py` now supports optional `--post-publish-scan` checks so each publish can immediately probe the live ClawHub page for `VirusTotal`, `OpenClaw`, and `Suspicious` signals.
