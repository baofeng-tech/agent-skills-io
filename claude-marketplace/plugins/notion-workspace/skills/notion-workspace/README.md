# Notion Workspace

Release-ready Claude Code skill package generated from `targetSkills/notion-workspace`.

- Skill name: `notion-workspace`
- Entry point: `SKILL.md`
- Runtime assets: `scripts/`, `references/`, `assets/` when present

## Notes

- Manage Notion workspace: search pages and databases, read markdown, create pages, insert rows, triggers, MCP. Powered by AISA gateway (Notion toolkit). Requires AISA_API_KEY and curl. Keywords: notion, workspace, page, database, block, markdown, wiki, task board, insert row, OAuth. Use when: the user needs web search, research, source discovery, or content extraction.
- This README is release-specific and replaces source READMEs that were written for other runtimes.
- If the underlying instructions mention OpenClaw, treat that as source-context or compatibility guidance unless the skill is specifically about OpenClaw setup.

## Quick Start

1. Open `SKILL.md` to review invocation guidance and runtime requirements.
2. Set any required environment variables before running bundled scripts.
3. Use repo-relative paths like `python3 scripts/...` when following command examples.
