# Publishing AgentSkills.so Release

1. Run `python3.12 scripts/build_agentskills_so_release.py`.
2. Copy the directory contents to the public GitHub repository root at `https://github.com/baofeng-tech/agent-skills-so`.
3. Keep the generated catalog files at repo root: `index.json`, `index.md`, and `well-known-skills-index.json`.
4. Submit or surface that GitHub repository to `agentskills.so` or other Agent Skills directories.
5. Keep future updates on the same repository so marketplace crawlers can refresh from GitHub.

## Notes

- This release layer is standards-first, not Claude-specific.
- It removes plugin-wrapper files such as `package.json` and `index.ts` when they are not part of the shipped standard skill surface.
- It is tuned for `agentskills.so` indexing rather than generic multi-runtime wording.
