# Media Gen

Release-ready Claude Code skill package generated from `targetSkills/media-gen`.

- Skill name: `media-gen`
- Entry point: `SKILL.md`
- Runtime assets: `scripts/`, `references/`, `assets/` when present

## Notes

- Generate images and videos with AIsa. Supports Gemini, Wan, and Seedream image generation plus Wan text-to-video and image-to-video models. One API key; the bundled client routes each model to the correct endpoint automatically. Use when: you need a neutral AIsa media-generation skill that spans multiple model families without changing credentials or request flow.
- This README is release-specific and replaces source READMEs that were written for other runtimes.
- If the underlying instructions mention OpenClaw, treat that as source-context or compatibility guidance unless the skill is specifically about OpenClaw setup.

## Quick Start

1. Open `SKILL.md` to review invocation guidance and runtime requirements.
2. Set any required environment variables before running bundled scripts.
3. Use repo-relative paths like `python3 scripts/...` when following command examples.
