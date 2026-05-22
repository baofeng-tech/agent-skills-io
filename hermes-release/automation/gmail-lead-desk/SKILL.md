---
name: gmail-lead-desk
description: 'Gmail Lead Desk — standalone sales/CS Gmail skill via the AISA gateway: OAuth connect, scan unread leads, summarize threads, draft template replies (default draft-only), archive with labels. Keywords: Gmail Lead Desk, Gmail, lead desk, sales, customer support, follow-up, unread, inquiry summary, draft reply, archive, OAuth, AISA, connected account, thread_id. Use when: the user needs this workflow''s domain-specific automation or guidance.'
license: MIT
metadata:
  aisa:
    emoji: 🛠
    requires:
      bins: []
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  hermes:
    tags:
    - automation
    - aisa
required_environment_variables:
- name: AISA_API_KEY
  prompt: AIsa API key
  help: Get your key from https://aisa.one or the AIsa marketplace account panel.
  required_for: AIsa-backed API access
---

# gmail-lead-desk

Gmail Lead Desk — standalone sales/CS Gmail skill via the AISA gateway: OAuth connect, scan unread leads, summarize threads, draft template replies (default draft-only), archive with labels. Keywords: Gmail Lead Desk, Gmail, lead desk, sales, customer support, follow-up, unread, inquiry summary, draft reply, archive, OAuth, AISA, connected account, thread_id. Use when: the user needs this workflow's domain-specific automation or guidance.

## When to Use

- Use this release when the user needs the runtime packaged under `scripts/`.
- Prefer the bundled Python or shell entrypoints instead of copying raw API examples into the chat.
- For Hermes community installs, keep setup explicit and review the command help text before the first run.

## Setup

- Review `README.md` for the release-specific summary and structure.
- Use repo-relative paths under `scripts/`.
- Prefer explicit CLI auth flags such as `--api-key` or `--aisa-api-key` when a script exposes them.

## Verification

- Confirm the command returns structured output or a successful API response.
- If the workflow stores local state, verify it writes under a repo-local data directory rather than a home-directory default.
