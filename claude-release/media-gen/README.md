# Media Gen

Release-ready Claude Code skill package generated from `targetSkills/media-gen`.

- Skill name: `media-gen`
- Entry point: `SKILL.md`
- Runtime assets: `scripts/`, `references/`, `assets/` when present

## Notes

- Generate images and videos with AIsa using one API key. Supports Gemini image generation, Wan 2.7 image models, Seedream image generation, and Wan text-to-video / image-to-video variants, while routing each model to the correct AIsa endpoint automatically. Use when: you need a neutral cross-platform skill for creating images or videos from prompts or reference images through AIsa.
- This README is release-specific and replaces source READMEs that were written for other runtimes.
- If the underlying instructions mention OpenClaw, treat that as source-context or compatibility guidance unless the skill is specifically about OpenClaw setup.

## Quick Start

1. Open `SKILL.md` to review invocation guidance and runtime requirements.
2. Set any required environment variables before running bundled scripts.
3. Use repo-relative paths like `python3 scripts/...` when following command examples.
