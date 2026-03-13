# Twitter Intel

Real-time X/Twitter data for Claude Code. Get followers, tweets, trends, analytics — no X API keys needed.

## What You Can Do

```
"get followers of @blockrunai"           → follower list with bios
"what's @elonmusk been tweeting?"        → recent tweets with engagement
"what's trending on X?"                  → trending topics
"search X for AI agent discussions"      → matching tweets and authors
"compare @elonmusk vs @sama"             → side-by-side analytics
"analyze @blockrunai's X presence"       → engagement score and metrics
```

## 15 Endpoints

| Endpoint | Cost |
|----------|------|
| `x_user_info()` — single profile | $0.002 |
| `x_user_lookup()` — batch profiles | $0.002/user |
| `x_followers()` — follower list | $0.05/page |
| `x_followings()` — following list | $0.05/page |
| `x_verified_followers()` — verified only | $0.048/page |
| `x_user_tweets()` — user's tweets | $0.032/page |
| `x_user_mentions()` — mentions of user | $0.032/page |
| `x_tweet_lookup()` — tweet details | $0.16/batch |
| `x_tweet_replies()` — reply thread | $0.032/page |
| `x_tweet_thread()` — full thread | $0.032/page |
| `x_search()` — advanced search | $0.032/page |
| `x_trending()` — trending topics | $0.002 |
| `x_articles_rising()` — viral articles | $0.05 |
| `x_author_analytics()` — author metrics | $0.02 |
| `x_compare_authors()` — compare two users | $0.05 |

Plus **Grok Live Search** for sentiment analysis (~$0.25/query).

## Install

This is part of BlockRun. In Claude Code:

```
try https://github.com/BlockRunAI/blockrun-agent-wallet
```

Or: `pip install blockrun-llm`

## Pricing

$1 gets you ~500 profile lookups, ~20 pages of followers (~4,000 accounts), or ~31 pages of tweets/search results.

---

**Powered by [BlockRun](https://blockrun.ai)** — pay-per-request, no X API keys or subscriptions
