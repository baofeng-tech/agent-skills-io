# Hermes Release

Hermes-oriented packaged copy of all `targetSkills/` mother skills.

## Structure

- Skills are organized by Hermes-style categories such as `research/`, `communication/`, and `finance/`.
- Each skill keeps a runtime-focused `SKILL.md + scripts/` layout, with non-runtime reference docs stripped from this release layer.
- Frontmatter is normalized for `metadata.aisa`, `metadata.hermes.tags`, and `required_environment_variables`.

## Category Counts

- `ai`: 3
- `communication`: 13
- `creative`: 2
- `finance`: 17
- `research`: 19

## Publish Paths

- GitHub repo + `hermes skills install github:owner/repo/path`
- Skills Hub / custom tap packaging
- Well-known index distribution if you later expose the repo via a website
