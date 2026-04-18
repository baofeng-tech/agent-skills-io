# Publishing Claude Release

This directory is intended to be pushed as the root of a public GitHub repository for Claude Code / skills.sh distribution.

## Recommended Flow

1. Create a new public GitHub repository.
2. Copy the contents of this directory to the repository root.
3. Commit all files except local test artifacts.
4. Push to GitHub and seed at least one install path through `skills.sh` or direct GitHub sharing.
5. Optionally build a plugin marketplace wrapper from this directory for `/plugin marketplace add` users.

## Recommended Repo Contents

- One skill directory per root folder
- `README.md`
- `AUDIT.md`
- `index.json`
- `.gitignore`

## Generated Skill Count

- 51
