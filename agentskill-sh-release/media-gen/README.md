# Media Gen

GitHub-ready release package prepared specifically for agentskill.sh import and refresh.

## Notes

- Generate images and videos with AIsa. Supports four image models (Google Gemini 3 Pro Image, Alibaba Wan 2.7 image and image-pro, ByteDance Seedream) and four Wan video variants (wan2.6/2.7 × t2v/i2v). One API key; the client routes each model to the correct endpoint automatically. Use when: you want a neutral cross-platform skill for AIsa image or video generation from prompts or reference images.
- This directory keeps one root-level skill per folder so agentskill.sh can scan the repository cleanly.
- The same skill can also be submitted by direct `SKILL.md` URL when needed.
