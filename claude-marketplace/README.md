# AIsa Claude Marketplace

Local Git-based Claude Code marketplace wrapper for the generated AIsa skills.

## Test Locally

```bash
claude /plugin marketplace add ./claude-marketplace
claude /plugin install aisa-twitter-command-center@aisa-claude-marketplace
```

## Notes

- Plugin entries use relative `./plugins/<name>` sources, which matches Claude Code's Git-based marketplace guidance.
- Each plugin embeds its own `skills/<skill>/` directory so cache installs do not break file resolution.
