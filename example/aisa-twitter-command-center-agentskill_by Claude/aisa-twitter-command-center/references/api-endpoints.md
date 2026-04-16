# Twitter API Endpoints Reference (via AIsa)

Base URL: `https://api.aisa.one/apis/v1`

Auth: `Authorization: Bearer $AISA_API_KEY` (read endpoints) or `aisa_api_key` in JSON body (post endpoints).

## Read Endpoints (GET)

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `/twitter/user/info` | User profile | `userName` |
| `/twitter/user_about` | User about (country, verification, username history) | `userName` |
| `/twitter/user/batch_info_by_ids` | Batch users by IDs | `userIds` (comma-separated) |
| `/twitter/user/last_tweets` | Recent tweets | `userName`, `cursor` |
| `/twitter/user/mentions` | Mentions | `userName`, `cursor` |
| `/twitter/user/followers` | Followers | `userName`, `cursor` |
| `/twitter/user/followings` | Followings | `userName`, `cursor` |
| `/twitter/user/verifiedFollowers` | Verified followers | `user_id` (numeric!), `cursor` |
| `/twitter/user/check_follow_relationship` | Check follow | `source_user_name`, `target_user_name` |
| `/twitter/user/search` | Search users | `query`, `cursor` |
| `/twitter/tweet/advanced_search` | Tweet search | `query`, `queryType` (**Required**: `Latest` or `Top`), `cursor` |
| `/twitter/tweets` | Tweets by IDs | `tweet_ids` (comma-separated) |
| `/twitter/tweet/replies` | Replies | `tweetId`, `cursor` |
| `/twitter/tweet/quotes` | Quotes | `tweetId`, `cursor` |
| `/twitter/tweet/retweeters` | Retweeters | `tweetId`, `cursor` |
| `/twitter/tweet/thread_context` | Full thread | `tweetId`, `cursor` |
| `/twitter/article` | Article by tweet | `tweet_id` |
| `/twitter/trends` | Trending topics | `woeid` (1=worldwide) |
| `/twitter/list/members` | List members | `list_id`, `cursor` |
| `/twitter/list/followers` | List followers | `list_id`, `cursor` |
| `/twitter/community/info` | Community info | `community_id` |
| `/twitter/community/members` | Community members | `community_id`, `cursor` |
| `/twitter/community/moderators` | Community moderators | `community_id`, `cursor` |
| `/twitter/community/tweets` | Community tweets | `community_id`, `cursor` |
| `/twitter/community/get_tweets_from_all_community` | Search all communities | `query`, `cursor` |
| `/twitter/spaces/detail` | Space detail | `space_id` |

## Post Endpoints (POST, body auth)

| Endpoint | Description | Body Params |
|----------|-------------|-------------|
| `/twitter/auth_twitter` | Get OAuth authorization URL | `aisa_api_key` |
| `/twitter/post_twitter` | Publish a tweet | `aisa_api_key`, `content`, `media_ids` (optional array) |

## Pagination

Most list endpoints support `cursor` for pagination. The response includes a `cursor` field — pass it as the `cursor` param in the next request to fetch more results.

## Pricing

| Operation | Cost |
|-----------|------|
| Read query | ~$0.0004 |
| OAuth post | See [aisa.one](https://aisa.one) pricing |

Every response includes `usage.cost` and `usage.credits_remaining`.
