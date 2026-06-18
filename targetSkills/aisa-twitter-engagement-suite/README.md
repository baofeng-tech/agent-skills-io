# AIsa Twitter Engagement Suite

Engagement-focused Twitter/X skill for research, approved posting, and follow-through actions through the AIsa relay.

## What it does

- Search Twitter/X profiles, tweets, and trends
- Publish through OAuth after explicit approval
- Like, unlike, follow, and unfollow through bundled Python clients
- Keep read and write workflows in one package without asking for passwords

## Best fit

- Use this when the user already knows what to engage with and needs action-oriented Twitter/X follow-through.
- Use this when the workflow needs both research and approved engagement in the same package.
- Use this when relay-based reads, remote writes, and relay-based media upload are acceptable.
- Use this when the runtime can provide `AISA_API_KEY`, `python3`, and network access to `api.aisa.one`.
- Use `aisa-twitter-api` for the flagship all-purpose Twitter lane.
- Use `aisa-twitter-command-center` for watchlists, trend scanning, and recurring monitoring.

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

## Security & Trust

- Requires only `AISA_API_KEY` for the shipped runtime.
- All reads, writes, and approved uploads are relayed through `api.aisa.one`.
- Write actions require explicit OAuth approval.
- Media posting uses relay-based upload paths supported by the runtime.
- Reads, writes, and uploads are remote API operations, not local-only actions.
- Do not claim a write action succeeded until the API confirms it.
