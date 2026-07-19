# AIsa Twitter API

Flagship Twitter/X skill for research, monitoring, watchlists, and OAuth-approved posting through the AIsa relay.

## What it does

- Search Twitter/X profiles, tweets, trends, lists, communities, and Spaces
- Inspect timelines, mentions, replies, quotes, and thread context
- Run watchlist-style monitoring and approved posting workflows through OAuth
- Send relay API requests, OAuth approval, and approved media uploads through `https://api.aisa.one`

## When to use

- Use this as the primary Twitter/X skill when the user wants one general-purpose surface for research, monitoring, watchlists, and approved posting.
- Use `aisa-twitter-engagement-suite` when the task is mainly likes, follows, replies, or other engagement actions.
- Use `aisa-twitter-command-center` when the task is mainly watchlists, trend scanning, and monitoring.

## Runtime requirements

```bash
export AISA_API_KEY="your-key"
```

Requires:

- `python3`
- `AISA_API_KEY`
- Network access to `https://api.aisa.one`
- Explicit OAuth approval before posting
- User-provided media files for image or video uploads

## Relay, OAuth, upload, and write behavior

- Read operations are sent through the relay target `https://api.aisa.one`.
- OAuth authorization is required before posting can occur.
- Posting is an external write and requires explicit OAuth approval before it can occur.
- Image and video posting sends user-selected media through the relay for upload.
- This skill does not require Twitter/X passwords or browser cookies.

## Common Commands

```bash
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa"
```

## Included runtime files

- Read client: `scripts/twitter_client.py`
- OAuth and posting client: `scripts/twitter_oauth_client.py`
- Posting guide: `references/post_twitter.md`

## Security & Trust

- Requires only `AISA_API_KEY` as the declared environment secret.
- Uses a relay-based flow to `https://api.aisa.one` for reads, OAuth handling, and approved uploads.
- External writes happen only after explicit OAuth approval.
- Image and video posting sends user-selected media through the relay for upload.
- Does not require passwords or browser cookies.
- Do not claim posting succeeded until the relay returns success.
