# Hermes Skill Structure And Upload Plan

## 1. Official Hermes Skill Rules

Based on the official Hermes docs as of **2026-04-17**:

- Hermes uses `SKILL.md` as the required entry file.
- Bundled skills live under category directories such as `skills/research/<skill>/`.
- Official optional skills use the same structure under `optional-skills/`.
- Hermes officially documents frontmatter support for:
  - `name`
  - `description`
  - `version`
  - `author`
  - `license`
  - `platforms`
  - `metadata.hermes.tags`
  - `metadata.hermes.related_skills`
  - `required_environment_variables`

Key docs:

- Creating Skills: <https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills/>
- Skills System: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/>
- Working with Skills: <https://hermes-agent.nousresearch.com/docs/guides/work-with-skills/>
- Configuration / skill settings: <https://hermes-agent.nousresearch.com/docs/user-guide/configuration/>

## 2. Discovery And Search Optimization

Hermes discovery has several layers:

- local installed skills in `~/.hermes/skills/`
- official optional skills via `hermes skills browse`
- Hub search via `hermes skills search`
- integrated external sources such as GitHub, `skills.sh`, well-known indexes, ClawHub, and Claude marketplace sources

For Hermes search and selection, the most important fields are:

- category path
- skill `name`
- skill `description`
- `metadata.hermes.tags`
- `metadata.hermes.related_skills`

Optimization rules that follow directly from the docs and observed CLI behavior:

- keep `name` stable and kebab-case
- place skills under an intuitive category
- include concrete task keywords in `description`
- use a strong `When to Use` section near the top
- add `metadata.hermes.tags` for query terms and domain labels
- add `related_skills` where families of similar skills exist

## 3. Suspicious / Scanner Risk In Hermes

Hermes docs say hub-installed skills are security-scanned for:

- data exfiltration
- prompt injection
- destructive commands
- shell injection
- supply-chain signals

Practical packaging implications for this repo:

- remove test and sync helpers from published bundles
- avoid browser auto-open by default
- avoid home-directory persistence defaults where a repo-local path is acceptable
- avoid references to local credential scraping or cookie extraction
- keep command examples relative to the shipped skill directory

## 4. Output Strategy Used Here

To avoid mutating `targetSkills/`, Hermes packaging should be generated into a separate layer:

- `hermes-release/`

Recommended layout:

```text
hermes-release/
├── research/
│   └── search/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
├── communication/
│   └── aisa-twitter-command-center/
└── finance/
    └── prediction-market/
```

This structure matches Hermes category expectations while keeping each skill portable.

## 5. Publish Paths

For Hermes there are three practical publish routes:

1. Public GitHub repo + direct install:
   - `hermes skills install github:owner/repo/category/skill-name`
2. Custom tap:
   - `hermes skills tap add owner/repo`
3. Official / optional contribution path:
   - prepare a PR-shaped `optional-skills/<category>/<skill>` candidate

## 6. Testing Guidance

Recommended validation order:

1. parse every generated `SKILL.md`
2. verify category path + required Hermes metadata
3. scan for banned packaging noise
4. run representative smoke tests for each unique implementation group
5. if Hermes CLI is available, install one or more generated skills in a clean local path and confirm slash-command visibility
