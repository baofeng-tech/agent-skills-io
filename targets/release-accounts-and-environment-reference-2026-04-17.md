# Release Accounts And Environment Reference

## Purpose

This repo now supports real release packaging and real-data testing for:

- ClawHub-oriented bundles
- Claude skill / plugin marketplace bundles
- Hermes-oriented bundles

When you need credentials, runtime paths, or test environment hints, **start with**:

- [example/accounts](/mnt/d/workplace/agent-skills-io/example/accounts:1)

## Source Of Truth

Do not duplicate live secrets across multiple docs.

For the current working values, open:

- [example/accounts](/mnt/d/workplace/agent-skills-io/example/accounts:1)

That file currently contains the repo's working references for:

- X/Twitter test account
- AISA API key
- Python 3.12 executable path

## How To Use It

### AISA-backed tests

Read `AISA_API_KEY` from [example/accounts](/mnt/d/workplace/agent-skills-io/example/accounts:1), then export it before running real API tests.

### Python 3.12 tests

Use the Python 3.12 path recorded in [example/accounts](/mnt/d/workplace/agent-skills-io/example/accounts:1).

As of this test wave, the repo uses:

- `python3.12 path: /usr/local/python3.12/bin/python3.12`

### X/Twitter write validation

Use the X/Twitter account noted in [example/accounts](/mnt/d/workplace/agent-skills-io/example/accounts:1) only for release validation workflows.

Preferred path:

1. Generate the OAuth authorization URL with the packaged Twitter skill.
2. Complete approval manually in the browser if needed.
3. Run a real write validation command and record the returned tweet id.

## Safety Notes

- Keep `example/accounts` out of publish bundles.
- Do not paste the raw secrets into release READMEs.
- In public-facing docs, reference the file path instead of copying secret values.
- When creating screenshots or reports, redact secrets unless the report is intentionally private.

## Related Docs

- [targets/claude-market-structure-and-upload-plan-2026-04-17.md](/mnt/d/workplace/agent-skills-io/targets/claude-market-structure-and-upload-plan-2026-04-17.md:1)
- [targets/hermes-market-structure-and-upload-plan-2026-04-17.md](/mnt/d/workplace/agent-skills-io/targets/hermes-market-structure-and-upload-plan-2026-04-17.md:1)
