# AGENTS.md

## Repo Working Rule

Any AI working in this repository should treat `PROJECT_OVERVIEW.md` as the high-level source of truth.

## AI Execution Addendum

Before starting a new substantial task:

1. Review the previous task outcome first
2. Check whether the last change was actually completed well
3. Check whether there is any obvious optimization, correction, or follow-up worth doing before starting new edits

Execution style for this repo:

- Assume the highest working permission has already been granted unless the user explicitly says otherwise
- Do not stop to ask for permission on normal repo analysis, editing, validation, workflow updates, or publishing-flow work
- Make the best plan you can as the acting engineer
- Then execute against that plan end-to-end, only pausing when a branch choice has real hidden consequences
- When upstream changes are large or structural, treat `AIsa-team/agent-skills` as the authoritative source first, then adapt that upstream state into mother skills and platform release layers here
- Do not use `/mnt/d/workplace/agent-skills` as this repo's automation input source; that local checkout is reserved for manual company-skill authoring and upload work

### Before doing substantial work

1. Read `PROJECT_OVERVIEW.md`
2. Use it to understand:
   - project purpose
   - directory roles
   - current outputs
   - publishing flow
   - current project status

### After completing work

Update `PROJECT_OVERVIEW.md` if any of the following changed:

- project purpose or positioning
- directory structure or directory meaning
- key outputs or generated artifacts
- publishing workflow
- recommended working flow
- project stage / current status

### Update rule

- Keep `PROJECT_OVERVIEW.md` concise and easy for both humans and AI to scan
- Prefer updating existing sections over adding noisy new sections
- Do not rewrite the document for tiny code-only changes unless they affect project understanding

## Standard Execution Flow

Use this default flow unless the task is truly trivial.

### Step 1: Ground yourself

Read these files first:

1. `PROJECT_OVERVIEW.md`
2. `README.md`
3. one or more of the following if relevant:
   - `targetSkills/PUBLISHING.md`
   - `clawhub-release/README.md`
   - files under `targets/`
   - files under `platformDesc/`

### Step 2: Identify the work type

Classify the task before editing:

- `source analysis`
  - working from `sources/` zip bundles
- `mother skill work`
  - working in `targetSkills/`
- `clawhub publish work`
  - working in `clawhub-release/`
- `claude / hermes publish work`
  - working in `claude-release/`, `claude-marketplace/`, or `hermes-release/`
- `methodology / docs work`
  - working in `targets/`, `platformDesc/`, or repo-level docs
- `ai helper skill work`
  - working in `.agents/skills/`

### Step 3: Use the right target directory

- If the goal is cross-platform skill output, prefer `targetSkills/`
- If the goal is ClawHub upload hardening, prefer `clawhub-release/`
- If the goal is Claude standalone publish output, prefer `claude-release/`
- If the goal is Claude plugin marketplace output, prefer `claude-marketplace/`
- If the goal is Hermes publish output, prefer `hermes-release/`
- If the goal is research, templates, or explanation, prefer `targets/`
- Do not confuse `targetSkills/` with the final ClawHub upload layer
- Do not hand-edit generated release layers when the real source of truth should be `targetSkills/`

### Step 3.5: Use the generation scripts

When the task is about Claude / Hermes release output, prefer these entry points:

- `python3 scripts/build_claude_release.py`
- `python3 scripts/build_claude_marketplace.py`
- `python3 scripts/build_hermes_release.py`
- `python3 scripts/test_release_layers.py`

These scripts are the default way to regenerate publish layers and validate them.
Run them in order. Do not run `build_claude_marketplace.py` in parallel with `build_claude_release.py`, because the marketplace builder reads `claude-release/` as its source tree.

### Step 4: Preserve project intent

When changing skills:

- keep runtime functionality intact unless the task explicitly asks for behavior changes
- prefer minimal safe changes over broad rewrites
- preserve relative paths in cross-platform mother skills
- keep ClawHub variants conservative and low-noise

### Step 5: Validate before finishing

When applicable, verify:

- directory structure is still coherent
- referenced files actually exist
- Python scripts still compile
- no accidental `__pycache__`, temp files, or other publish noise remains
- `targetSkills/` and `clawhub-release/` are not being mixed up

### Step 6: Update project memory

Before finishing, check whether `PROJECT_OVERVIEW.md` should be updated.

Update it when:

- a new major directory appears
- a new skill family is added
- the publishing workflow changes
- the repo's role changes
- the project stage meaningfully advances

Do not update it for tiny wording fixes or isolated code changes that do not affect repo understanding.

### Priority

When `README.md`, ad hoc notes, and scattered docs differ, prefer:

1. `AGENTS.md`
2. `PROJECT_OVERVIEW.md`
3. other project documents
