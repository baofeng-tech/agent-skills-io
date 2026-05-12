# GitHub Actions And AISA Usage Review 2026-05-12

## Scope

This pass reviewed:

- GitHub Actions run `25696814846`
- repository Actions variables that control scheduled automation
- likely AISA API usage created by the repo automation

## Failed Run

Run `25696814846` was a scheduled run created at `2026-05-11T20:55:46Z`.

- Run head: `876ef4d66977b496398c131e653555a0ad003483`
- Current remote HEAD during review: `b87450a7bb782f04a6328aff943867cf5f63e385`
- `sync-build-test`: success
- `self-hosted-preflight`: success
- `self-hosted-publish`: failed

The failing command was:

```bash
python3 scripts/publish_clawhub_batch.py --targets both --skip-build --post-publish-scan
```

The batch publish summary was:

- `published=0`
- `skipped=9`
- `failed=12`

Representative failures were ClawHub slug or version ownership conflicts:

- `skill:aisa-twitter-api@1.0.5`: fallback `aisa-twitter-api-aisa` returned `Version already exists`
- `skill:search@1.0.1`: `search` is a reserved slug
- `skill:perplexity-search@1.0.0`: slug locked to a deleted or banned account
- `skill:last30days@1.0.4`: fallback `last30days-aisa` already taken
- `skill:twitter@1.0.0`: fallback `twitter-aisa` already taken

Conclusion: the hosted build/test portion was healthy. The failure came from scheduled continuation trying to run a full ClawHub publish against slugs that are not all currently publishable by the configured tokens.

## AISA Usage Findings

The same run used `AISA_API_KEY` in two paid paths:

- repo-local LLM refinement via `scripts/llm_refine_aisa_skills.py`
  - log line: `Refinement helper config: source=AISA_API_KEY, mode=chat-completions, model=gpt-5.4, base_url=https://api.aisa.one/v1/chat/completions`
  - this appeared in both the hosted sync lane and the publish continuation lane
- read-only AISA API regression via `scripts/test_aisa_api_skills.py`
  - latest scheduled run checked `54` skills with `72` commands

Recent workflow volume from `2026-04-28` through `2026-05-12`:

- total runs: `43`
- scheduled runs: `26`
- manual dispatch runs: `16`
- push runs: `1`

This is enough automation volume to plausibly explain a large part of the recent AISA API spend, especially because the scheduled config had:

- `AUTO_PIPELINE_SELECTION=all`
- `AUTO_RUN_LLM_STEP=true`
- `AUTO_LLM_APPLY=true`
- AISA regression defaulting on when no variable overrode it
- `AUTO_CLAWHUB_PUBLISH=both`

## Immediate Safety Changes

Repository variables were changed to reduce scheduled spend and stop the failing publish lane:

- `AUTO_PIPELINE_SELECTION=changed`
- `AUTO_RUN_LLM_STEP=false`
- `AUTO_LLM_APPLY=false`
- `AUTO_RUN_AISA_API_REGRESSION=false`
- `AUTO_FULL_PLATFORM_PUBLISH=false`
- `AUTO_CLAWHUB_PUBLISH=none`

Workflow defaults were also updated so `run_aisa_api_regression` is opt-in by default for manual and scheduled runs. The workflow now documents that AISA regression uses paid AISA API traffic.

## Remaining Notes

The AISA console usage log still needs account-side confirmation to attribute every request. Local GitHub Actions logs prove the repo automation used the configured `AISA_API_KEY`, but the console is the source of truth for exact dollar attribution by request, model, and key.
