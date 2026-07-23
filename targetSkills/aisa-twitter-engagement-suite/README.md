# AIsa Twitter Engagement Suite

Research Twitter/X profiles, tweets, and trends, then take approved engagement and posting follow-through actions through the AIsa relay.

## What it does

- Search Twitter/X profiles, tweets, and trends
- Publish through OAuth after explicit approval
- Like, unlike, follow, and unfollow through bundled Python clients
- Keep research and engagement follow-through in one package without asking for passwords

## Best fit

- Use this when the user already knows what to engage with and needs action-oriented Twitter/X follow-through.
- Use this when the workflow needs both research and approved engagement in the same package.
- Use this when relay-based reads, remote writes, and relay-based media upload are acceptable.
- Use this when the runtime can provide `AISA_API_KEY`, `python3`, and network access to `api.aisa.one`.
- Use `aisa-twitter-api` for the broader flagship Twitter lane.
- Use `aisa-twitter-command-center` for watchlists, trend scanning, and recurring monitoring.

## When not to use

- Do not use this for password login, cookie extraction, or browser-derived Twitter auth.
- Do not use this when the workflow must avoid relay-based network calls, remote writes, or relay-based uploads.
- Do not use this as a fully local Twitter/X client.

## Setup

```bash
export AISA_API_KEY="your-key"
```

Requires:

- `python3`
- `AISA_API_KEY`
- network access to `https://api.aisa.one/`
- explicit OAuth approval before posting or engagement writes
- relay-based upload support for approved media posting flows

## Runtime entry points

- Read client: `scripts/twitter_client.py`
- Post client: `scripts/twitter_oauth_client.py`
- Engage client: `scripts/twitter_engagement_client.py`

## Example commands

```bash
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_engagement_client.py like-latest --user "@elonmusk"
```

## Workflow focus

- Research first, then take an approved engagement action from the same package.
- Use this for posting and post-research engagement follow-through, not as the broad flagship Twitter surface.
- Keep relay target, OAuth approval, upload behavior, environment requirements, and remote side effects explicit in user-facing usage.

## Example requests

- "Research this Twitter/X account, then like the latest post if it matches our topic."
- "Search Twitter/X for AI agents, review the results, then prepare an approved engagement action."
- "Authorize posting, then publish a Twitter/X update with media through the relay flow."
- "Check recent activity from this account and decide whether to follow or unfollow."

## Security & Trust

- Requires only `AISA_API_KEY` for the shipped runtime.
- All reads, writes, and approved uploads are relayed through `api.aisa.one`.
- Write actions require explicit OAuth approval.
- Media posting uses relay-based upload paths supported by the runtime.
- Reads, writes, and uploads are remote API operations, not local-only actions.
- Do not claim a write action succeeded until the API confirms it.
