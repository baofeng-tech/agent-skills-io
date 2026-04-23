# Platform Skill And Plugin Methodology

## Why This Repo Uses Three Global Publish Skills

This repository treats the three global skills below as an internal operating model, not just as reusable prompts:

- `clawhub-skill-optimizer-all`
- `clawhub-plugin-packager-all`
- `clawhub-security-auditor-all`

They are used together because this repo has three different responsibilities:

1. keep `targetSkills/` as the cross-platform mother-skill source of truth
2. generate conservative platform-specific skill and plugin layers
3. reduce publish risk before any real marketplace upload

One skill alone cannot cover all three jobs cleanly.

## Role Split

| Global skill | Repo responsibility | In this repo it governs |
| --- | --- | --- |
| `clawhub-skill-optimizer-all` | copy and surface design | naming, description, frontmatter, bilingual wording, source mode vs publish mode |
| `clawhub-plugin-packager-all` | artifact construction | runtime-only file set, manifests, plugin wrappers, zip shape, trust-oriented package layout |
| `clawhub-security-auditor-all` | publish gatekeeping | suspicious-pattern review, side-effect review, auth surface review, docs/runtime drift review |

## Why They Are Applied In This Order

### 1. Optimize before packaging

The optimizer skill is applied first because the repo needs a clean source story before it can emit platform variants.

That matches the repo structure:

- `targetSkills/` is the canonical mother layer
- `clawhub-release/`, `claude-release/`, `hermes-release/`, `agentskills-so-release/`, and `agentskill-sh-release/` are generated publish layers

If naming, `description`, `Use when:` wording, or `metadata.aisa` are still unstable at the mother-skill level, packaging the result only amplifies the inconsistency.

### 2. Package after the source story is stable

The packager skill is applied second because platform success here depends on artifact shape:

- ClawHub skill bundles must stay conservative
- ClawHub plugins need `openclaw.plugin.json`, `package.json`, and embedded `skills/`
- Claude marketplace plugins need `.claude-plugin/plugin.json`
- Agent Skills public layers need root-level skill directories and crawler-friendly indexes

This repo implements that via build scripts instead of hand edits:

- `scripts/build_clawhub_release.py`
- `scripts/build_clawhub_plugin_release.py`
- `scripts/build_claude_release.py`
- `scripts/build_claude_marketplace.py`
- `scripts/build_hermes_release.py`
- `scripts/build_agentskills_so_release.py`
- `scripts/build_agentskill_sh_release.py`

### 3. Audit immediately before publish

The security auditor skill is applied last because many publish risks are introduced by the final shipped artifact, not by the mother skill alone.

Examples in this repo:

- dev/test helpers accidentally left in the bundle
- home-directory state defaults that should become repo-local
- browser auto-open behavior that should become explicit/manual
- release README claims that drift away from shipped runtime contents

That is why this repo keeps `scripts/test_release_layers.py` and multiple market-structure docs alongside the build scripts.

## Rule Sources Inside This Repo

The rules in the three global skills are not arbitrary. They are grounded in repo-local documents and live publish experience.

### Mother-skill rules

Primary sources:

- `AGENTS.md`
- `PROJECT_OVERVIEW.md`
- `targets/skill-modification-rules-2026-04-19.md`
- `targets/targetskills-agentskills-compliance-audit-2026-04-20.md`

What these sources establish:

- `targetSkills/` is the source of truth
- canonical source frontmatter should center on `metadata.aisa`
- mother skills should prefer relative paths and cross-platform wording
- platform-private metadata should not dominate the mother skill

### Claude / Hermes publish rules

Primary sources:

- `targets/release-generation-rules-and-runbook-2026-04-17.md`
- `targets/claude-market-structure-and-upload-plan-2026-04-17.md`
- `targets/hermes-market-structure-and-upload-plan-2026-04-17.md`

What these sources establish:

- build release layers from `targetSkills/` instead of hand-editing publish copies
- strip non-runtime helpers from publish layers
- keep README and `SKILL.md` aligned to shipped runtime
- adapt wording and structure to the actual discovery model of each platform

### ClawHub plugin rules

Primary sources:

- `targets/clawhub-plugin-structure-and-upload-plan-2026-04-20.md`
- `targets/claude-clawhub-publish-followup-2026-04-21.md`
- `scripts/build_clawhub_plugin_release.py`

What these sources establish:

- package skill-first assets as native-first plugins without rewriting the core workflow
- keep plugin manifests, README, and embedded `skills/` aligned
- prefer trust, coherence, and scanner-friendly packaging over noisy feature expansion

### Agent Skills public-layer rules

Primary sources:

- `targets/agentskills-so-structure-and-upload-plan-2026-04-20.md`
- `scripts/build_agentskills_so_release.py`
- `scripts/build_agentskill_sh_release.py`

What these sources establish:

- public GitHub trust matters as much as parser correctness
- root-level skill directories and flat public metadata improve crawler compatibility
- publish layers should look like clean public catalogs, not workspace snapshots

## Practical Rule Matrix

| Concern | Rule | Why |
| --- | --- | --- |
| Mother frontmatter | Keep canonical `metadata.aisa` in `targetSkills/` | Cross-platform portability and one source of truth |
| Description style | Include a plain-language task outcome plus `Use when:` or `触发条件：` | Better discovery and better invocation fit |
| Path style | Use relative `scripts/...` paths in mother skills | Avoid runtime-specific placeholders |
| Runtime surface | Exclude compare/test/sync/dev helpers from publish bundles | Reduce upload risk and reviewer distrust |
| State writes | Prefer repo-local persistence in publish layers | Lower security flags and keep side effects visible |
| OAuth / actions | Make approval and side effects explicit | Avoid unsafe automation defaults |
| EN / ZH parity | Keep runtime scope aligned across language variants | Prevent drift and marketplace trust mismatch |
| Plugin packaging | One sharp JTBD per artifact | Better install clarity and portfolio positioning |

## How To Use These Rules When Editing

### When you change a mother skill

Apply optimizer logic first:

- check `name`
- check `description`
- check `metadata.aisa`
- check whether the body still matches the real runtime

### When you create or regenerate a release layer

Apply packager logic second:

- trim to runtime-only files
- emit the correct wrapper structure for the target platform
- keep plugin manifests and embedded skill contents semantically aligned

### When you prepare for a real upload

Apply auditor logic last:

- look for suspicious helpers
- look for docs/runtime drift
- look for unsafe default state paths
- look for auth stories that are broader than the shipped runtime needs

## Repo-Specific Interpretation

In this project, the three global skills are effectively translated into code and docs:

- optimizer -> mother-skill normalization plus publish-copy wording decisions
- packager -> release build scripts and wrapper generators
- auditor -> smoke tests, guardrail docs, follow-up reports, and publish review checklists

That is why the repo should keep these three skill lenses explicit in docs for future humans and future AI agents.
