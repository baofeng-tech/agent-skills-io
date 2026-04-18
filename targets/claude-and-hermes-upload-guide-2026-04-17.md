# Claude And Hermes Upload Guide

## 1. Uploading Skills To Claude

### A. Standalone Claude skills via GitHub

Best source layer in this repo:

- [claude-release](</mnt/d/workplace/agent-skills-io/claude-release>)

Build it from source with:

```bash
python3 scripts/build_claude_release.py
```

Recommended steps:

1. Create a new public GitHub repository for the Claude skill catalog.
2. Copy the contents of `claude-release/` to the repository root.
3. Commit and push the repo.
4. Seed installs through GitHub sharing or `skills.sh`.

Why this works:

- Claude-compatible standalone skills are discovered from root-level skill directories with `SKILL.md`.
- `claudemarketplaces.com` currently behaves like an index layered on top of broader ecosystem sources instead of a classic manual upload console.

Relevant official docs:

- Claude skills: <https://code.claude.com/docs/en/skills>
- Claude plugin marketplaces: <https://code.claude.com/docs/en/plugin-marketplaces>

### B. Claude plugin marketplace

Best source layer in this repo:

- [claude-marketplace](</mnt/d/workplace/agent-skills-io/claude-marketplace>)

Current external publish repo in this workspace:

- `D:\workplace\Aisa-One-Plugins-Claude`

Build it from source with:

```bash
python3 scripts/build_claude_marketplace.py
```

Recommended steps:

1. Create a dedicated GitHub repository for the marketplace.
2. Copy the contents of `claude-marketplace/` to the repository root.
3. Commit and push.
4. In Claude Code, add the marketplace:

```text
/plugin marketplace add owner/repo
```

5. Install a packaged plugin:

```text
/plugin install aisa-twitter-command-center@aisa-claude-marketplace
```

### C. Local validation before publish

From the marketplace repo root:

```bash
claude plugin validate .
```

Or inside Claude Code:

```text
/plugin validate .
```

Then test locally:

```text
/plugin marketplace add ./path/to/marketplace
/plugin install aisa-twitter-command-center@aisa-claude-marketplace
```

### D. Optional official marketplace submission

Claude Code docs say official plugin submissions use Anthropic's submission flow in-app:

- Claude.ai settings plugin submission form

That is separate from self-hosted GitHub marketplaces.

## 2. Uploading Skills To Hermes

Best source layer in this repo:

- [hermes-release](</mnt/d/workplace/agent-skills-io/hermes-release>)

Build it from source with:

```bash
python3 scripts/build_hermes_release.py
```

### A. GitHub repository install path

1. Create a public GitHub repository for the Hermes catalog.
2. Copy `hermes-release/` contents to the repo root.
3. Commit and push.
4. Install directly from Hermes:

```bash
hermes skills install github:owner/repo/category/skill-name
```

Example shape:

```bash
hermes skills install github:your-org/aisa-hermes-skills/communication/aisa-twitter-command-center
```

### B. Publish to the Skills Hub

Hermes official docs show:

```bash
hermes skills publish skills/my-skill --to github --repo owner/repo
```

For this repo's generated layout, the practical approach is:

1. choose a specific skill directory under `hermes-release/<category>/<skill>`
2. place it into the expected publish source location
3. run `hermes skills publish ...`

### C. Custom tap repository

Hermes docs also support custom taps:

```bash
hermes skills tap add owner/repo
```

Users can then browse/install from that repo as a source.

### D. Local validation / runtime test

Hermes docs recommend validating by actually invoking the skill:

```bash
hermes chat --toolsets skills -q "Use the X skill to do Y"
```

And for discovery:

```bash
hermes skills browse
hermes skills search twitter
hermes skills inspect owner/repo/path
```

## 3. Repo-Specific Notes

- Use [targets/release-accounts-and-environment-reference-2026-04-17.md](/mnt/d/workplace/agent-skills-io/targets/release-accounts-and-environment-reference-2026-04-17.md:1) for where to look up credentials and runtime paths.
- Run real smoke tests before publishing.
- Publish the generated release layers, not `targetSkills/` directly.
- Before publishing, regenerate the target layer from `targetSkills/` instead of editing release copies by hand.
- Use [scripts/test_release_layers.py](/mnt/d/workplace/agent-skills-io/scripts/test_release_layers.py:1) for structure/smoke validation.

## 4. Official Sources

- Claude plugin marketplaces: <https://code.claude.com/docs/en/plugin-marketplaces>
- Claude plugins: <https://code.claude.com/docs/en/plugins>
- Claude skills: <https://code.claude.com/docs/en/skills>
- Hermes creating skills: <https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills/>
- Hermes skills system: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/>
