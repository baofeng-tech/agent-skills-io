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
- `targets/clawhub-suspicious-causes-and-fixes-2026-04-25.md`

What these sources establish:

- `targetSkills/` is the source of truth
- if a skill already exists in `AIsa-team/agent-skills@agentskills`, treat that upstream runtime as the first baseline before local copy optimization
- canonical source frontmatter should center on `metadata.aisa`
- mother skills should prefer relative paths and cross-platform wording
- platform-private metadata should not dominate the mother skill
- copy optimization must not silently remove upstream runtime capability

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
- `targets/clawhub-suspicious-causes-and-fixes-2026-04-25.md`
- `scripts/build_clawhub_plugin_release.py`

What these sources establish:

- package skill-first assets as native-first plugins without rewriting the core workflow
- keep plugin manifests, README, and embedded `skills/` aligned
- prefer trust, coherence, and scanner-friendly packaging over noisy feature expansion
- relay targets, media uploads, OAuth steps, env vars, and registry metadata must all describe the same real side effects
- pending scan output, clean scan output, and `Suspicious` output are different states and should be documented distinctly

### Agent Skills public-layer rules

Primary sources:

- `targets/agentskills-so-structure-and-upload-plan-2026-04-20.md`
- `scripts/build_agentskills_so_release.py`
- `scripts/build_agentskill_sh_release.py`

What these sources establish:

- public GitHub trust matters as much as parser correctness
- root-level skill directories and flat public metadata improve crawler compatibility
- publish layers should look like clean public catalogs, not workspace snapshots

## External Market Evidence From `../skillGet`

This repo also treats the adjacent `../skillGet` workspace as an evidence layer for breakout positioning, not just as an import source.

Primary sources:

- `../skillGet/dist/reports/AISA_All_Skills_Breakout_Plan_ZH.md`
- `../skillGet/dist/reports/ClawHub_Viral_Boss_Report_ZH.md`
- `../skillGet/dist/reports/ClawHub_Plugin_Viral_Report_ZH.md`
- `../skillGet/dist/data/clawhub-top200-aisa-conversion-plan.json`
- `../skillGet/dist/data/aisa-api-analysis.json`

What these sources establish:

- which AIsa-native lanes deserve `flagship`, `growth-variant`, or `supporting-variant` treatment
- which titles, JTBD frames, and sibling ladders match current ClawHub demand
- which online skills are worth converting into new AIsa API packages
- which plugin lanes should stay bundle-first versus graduating into native code plugins later

Use this evidence in addition to repo-local rules:

- use `AISA_All_Skills_Breakout_Plan_ZH.md` when deciding which existing AIsa skill to upgrade first
- use `ClawHub_Viral_Boss_Report_ZH.md` when sharpening task-first naming and example requests
- use `ClawHub_Plugin_Viral_Report_ZH.md` when deciding whether the package needs stronger trust, source-linked proof, or a narrower plugin JTBD
- use `clawhub-top200-aisa-conversion-plan.json` when selecting one online non-AIsa skill to adapt into a new AIsa API experiment
- use `aisa-api-analysis.json` to confirm the target lane maps onto real AIsa endpoint coverage before promising it in copy

## Practical Rule Matrix

| Concern | Rule | Why |
| --- | --- | --- |
| Mother frontmatter | Keep canonical `metadata.aisa` in `targetSkills/` | Cross-platform portability and one source of truth |
| Description style | Include a plain-language task outcome plus `Use when:` or `触发条件：` | Better discovery and better invocation fit |
| Path style | Use relative `scripts/...` paths in mother skills | Avoid runtime-specific placeholders |
| Runtime surface | Exclude compare/test/sync/dev helpers from publish bundles | Reduce upload risk and reviewer distrust |
| State writes | Prefer repo-local persistence in publish layers | Lower security flags and keep side effects visible |
| OAuth / actions | Make approval and side effects explicit | Avoid unsafe automation defaults |
| Upstream baseline | Diff against `AIsa-team/agent-skills@agentskills` before editing an existing skill | Preserve runtime completeness and avoid local drift |
| EN / ZH parity | Keep runtime scope aligned across language variants | Prevent drift and marketplace trust mismatch |
| Plugin packaging | One sharp JTBD per artifact | Better install clarity and portfolio positioning |

## How To Use These Rules When Editing

### When you change a mother skill

Apply optimizer logic first:

- check `name`
- check `description`
- check `metadata.aisa`
- check whether the body still matches the real runtime
- check whether `../skillGet` suggests this skill should act as a flagship, sibling, or supporting variant instead of competing with a nearby AIsa package

### When you create or regenerate a release layer

Apply packager logic second:

- trim to runtime-only files
- emit the correct wrapper structure for the target platform
- keep plugin manifests and embedded skill contents semantically aligned
- make sure the release artifact still supports the same breakout claim that the title, description, and README now make

### When you prepare for a real upload

Apply auditor logic last:

- look for suspicious helpers
- look for docs/runtime drift
- look for unsafe default state paths
- look for auth stories that are broader than the shipped runtime needs
- look back at `../skillGet` demand evidence so you do not ship two sibling skills that are chasing the same exact ClawHub search surface

## Repo-Specific Interpretation

In this project, the three global skills are effectively translated into code and docs:

- optimizer -> mother-skill normalization plus publish-copy wording decisions
- packager -> release build scripts and wrapper generators
- auditor -> smoke tests, guardrail docs, follow-up reports, and publish review checklists

## Repo-Local Profile Split

As of 2026-04-28, this repo no longer treats the global `*-all` publish skills as the default mother-skill editor context.

Why:

- the global skills intentionally mix:
  - cross-platform publish rules
  - ClawHub suspicious-remediation rules
  - breakout positioning rules
- that is useful for ClawHub remediation, but too mixed for default `targetSkills/` refinement

Current repo-local split:

- `.agents/skills/aisa-source-skill-editor/SKILL.md`
  - default neutral profile for `targetSkills/`
- `.agents/skills/aisa-clawhub-breakout-editor/SKILL.md`
  - ClawHub breakout / suspicious-repair profile

Current script wiring:

- `scripts/unified_skill_pipeline.py`
  - normal LLM refinement now calls `scripts/llm_refine_aisa_skills.py --profile source`
- `scripts/clawhub_suspicious_remediation.py`
  - targeted ClawHub repair now calls `scripts/llm_refine_aisa_skills.py --profile clawhub_breakout`

This keeps the mother-skill default path more neutral while still letting ClawHub-only repair work use the stronger breakout/auditor context.

## 2026-04-25 Internalized Suspicious Lessons

The current repo now treats these as reusable method, not one-off incident notes:

- relay-based skills must say exactly where keys, OAuth callbacks, and media uploads go
- public copy must not look like prompt injection or hidden autonomous instructions
- env-var requirements must match across `SKILL.md`, README, manifests, and registry-facing metadata
- if a scan is still pending, do not describe it as clean or suspicious yet
- when a skill already exists upstream, start from that runtime and preserve feature completeness before applying publish-surface edits

That is why the repo should keep these three skill lenses explicit in docs for future humans and future AI agents.
