# Claude Market Structure And Upload Plan

## 1. What Claude Market Actually Indexes

As of **2026-04-17**, `https://claudemarketplaces.com` behaves like an indexed directory rather than a classic manual upload portal.

Observed current behavior from the site and official docs:

- `claudemarketplaces.com/skills` lists public Claude skills and shows install counts, GitHub repos, and descriptions.
- The site's public About page says skills are crawled from **skills.sh** and that plugin marketplaces are discovered from GitHub repos containing a valid `.claude-plugin/marketplace.json`.
- Claude Code official docs say standalone skills live as `<skill>/SKILL.md` and shared distribution is typically done through plugins and plugin marketplaces.

Implication:

- If the goal is **Claude skill discovery**, the practical path is a **public GitHub repo with root-level skill directories** and clean `SKILL.md` files.
- If the goal is **Claude plugin marketplace distribution**, a second repo or layer with `.claude-plugin/marketplace.json` is helpful, but it is not required just to host standalone skills.

## 2. Claude Skill Structure That Matters

The lowest-friction Claude-compatible standalone structure is:

```text
repo-root/
├── skill-a/
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── skill-b/
│   └── SKILL.md
└── README.md
```

Practical field priorities for `SKILL.md`:

- `name`
- `description`
- `allowed-tools`
- optional Claude-friendly keys such as `when_to_use`, `argument-hint`, `user-invocable`

For search and invocation, the strongest fields are still:

- skill directory name / slug
- frontmatter `name`
- frontmatter `description`

## 3. Search Optimization Rules Worth Following

Based on current marketplace behavior and the repo's ClawHub packaging lessons:

- Keep skill names in stable `kebab-case`.
- Put the main query keywords directly in `name` and `description`.
- Use explicit trigger language such as `Use when:` or `触发条件：`.
- Lead descriptions with the actual task outcome, not platform internals.
- Avoid vague brand-only naming without capability terms such as `twitter`, `youtube`, `search`, `market`, `stock`, `prediction`, or `llm`.
- Keep Chinese skills bilingual enough that core English ecosystem keywords still appear in the description when discoverability matters.

## 4. Suspicious / Trust-Review Risk Patterns

The biggest patterns likely to hurt publishability or trust review in this repo were:

- `webbrowser.open(...)` in multiple Twitter OAuth helpers
- home-directory defaults such as `~/.clawdbot`
- non-runtime shell helpers like `compare.sh`, `sync.sh`, `test-v1-vs-v2.sh`
- generated artifacts such as `__pycache__/` and `*.pyc`
- global config references like `~/.config/last30days/.env`

Risk reduction strategy used for the Claude release layer:

- remove obvious non-runtime files from release bundles
- strip OpenClaw-heavy frontmatter fields from published `SKILL.md`
- disable browser auto-open in OAuth release copies
- move local persistence defaults from home directories to repo-local paths where practical
- keep mother skills unchanged so the release layer stays reversible

## 5. Output Created In This Repo

This turn adds a dedicated Claude-oriented release layer:

- `claude-release/`

This directory is generated from `targetSkills/` and is intended to be the publishable GitHub-facing layer for Claude skill sharing.

## 6. Recommended Next Step To Get Listed

1. Publish `claude-release/` as a public GitHub repository root.
2. Keep each skill at the repo root with `<skill>/SKILL.md`.
3. Share installs through GitHub and `skills.sh`.
4. After the repo is live, watch whether `claudemarketplaces.com` discovers the skills automatically.
5. Only add a plugin marketplace wrapper if you also want `/plugin marketplace add owner/repo` distribution.
