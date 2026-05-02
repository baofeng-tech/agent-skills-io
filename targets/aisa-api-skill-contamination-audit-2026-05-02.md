# AISA API Skill Contamination Audit - 2026-05-02

## Trigger

The local branch had diverged from `origin/main` and carried one unpushed commit plus working-tree edits. The visible symptom was a large set of modified skill files, especially under `targetSkills/`, generated release layers, and ZIP artifacts.

## Finding

- The unpushed local commit `36b4cc0` modified AISA-backed mother skills and generated platform layers.
- Affected mother-layer paths included `targetSkills/aisa-provider`, `targetSkills/aisa-tavily`, `targetSkills/llm-router`, `targetSkills/openclaw-aisa-youtube-aisa`, `targetSkills/stock-dividend`, and `targetSkills/stock-rumors`.
- The follow-up working tree also modified `llm-router` runtime files across every generated platform layer.
- These changes were not pushed to `baofeng-tech/agent-skills-io` and were not pushed to `AIsa-team/agent-skills`.

## Restore Action

- Backed up the contaminated local state as branch `backup/pre-aisa-restore-20260502-234456`.
- Stashed the contaminated working tree before cleanup.
- Reset local `main` to `origin/main@c596e96`.
- Restored the rule that AISA API skill scripts and runtime behavior are not edited as part of model-selection or publish-flow cleanup.
- Verified the final working tree has no `targetSkills/` diffs and no runtime script diffs under `targetSkills/` or generated release layers.

## Upstream Comparison

- Fetched `AIsa-team/agent-skills` as read-only `aisa/main`; nothing was pushed to that upstream repository.
- The upstream repository currently exposes 10 root skill families, while this repo carries a broader `targetSkills/` mother layer plus platform-specific release layers.
- Matching upstream skill families have pre-existing script differences in this repo because the mother layer is adapted for this project and its release targets.
- No upstream-script restore was applied in this cleanup because the final diff does not modify any skill runtime scripts; blindly replacing adapted mother scripts with upstream root files would be a separate upstream-sync task with release-layer consequences.

## AISA API Regression

- Ran `python3 scripts/test_aisa_api_skills.py --timeout 180 --retries 3 --delay 1`.
- Checked 54 AISA-backed skills with 72 read-only command checks.
- Result: 55 passed, 17 failed, 4 docs-only skills.
- Remaining failures were dominated by AISA/API network `UNEXPECTED_EOF_WHILE_READING` or Node TLS disconnects; two stock checks reached AISA but returned model output without the expected JSON block.
- Report: `targets/aisa-api-regression-report-2026-05-02.json`.

## Root Cause

- The `gpt-5.4` model change was applied too broadly: it belongs to the repo-local skill refinement helper, not to shipped AISA API skill runtimes such as `llm-router`.
- ZIP artifacts were being generated with current filesystem metadata, so repeated builds could produce binary diffs even when runtime files did not materially change.
- The workflow ran on a four-hour schedule while long hosted/self-hosted lanes could still be running, causing queued runs to be canceled or left waiting by GitHub concurrency.
- Commit steps pushed generated changes without first rebasing onto the latest remote state, which made action-generated commits race with local or other workflow commits.

## Fix Policy

- Keep `gpt-5.4` only in repo-local LLM refinement defaults unless a specific skill runtime intentionally supports that model.
- Do not hand-edit AISA API skill scripts for publish cleanup. Preserve upstream or current mother-layer runtime behavior.
- Generate release ZIPs deterministically so routine rebuilds stop creating binary churn.
- Rebase workflow checkouts before committing generated outputs and retry push after remote updates.
