---
name: twitter-intel
description: Real-time X/Twitter data — profiles, followers, tweets, trends, analytics. 15 direct endpoints plus Grok Live Search. No X API keys needed.
---

# Twitter Intel

Get real-time X/Twitter data without API keys. 15 direct endpoints for structured data, plus Grok Live Search for sentiment analysis.

## When to Use This Skill

- Getting a user's profile, followers, or tweets
- Searching X for specific topics or keywords
- Checking what's trending on X
- Analyzing an author's engagement and reach
- Comparing two accounts
- Monitoring brand mentions

## Quick Decision Tree

| User wants... | Use | Cost |
|--------------|-----|------|
| Profile data | `x_user_info()` or `x_user_lookup()` | $0.002/user |
| Follower/following list | `x_followers()` / `x_followings()` | $0.05/page |
| Verified followers | `x_verified_followers()` | $0.048/page |
| User's tweets | `x_user_tweets()` | $0.032/page |
| Mentions of a user | `x_user_mentions()` | $0.032/page |
| Tweet details | `x_tweet_lookup()` | $0.16/batch |
| Replies to a tweet | `x_tweet_replies()` | $0.032/page |
| Full tweet thread | `x_tweet_thread()` | $0.032/page |
| Search X | `x_search()` | $0.032/page |
| Trending topics | `x_trending()` | $0.002 |
| Viral articles | `x_articles_rising()` | $0.05 |
| Author analytics | `x_author_analytics()` | $0.02 |
| Compare two authors | `x_compare_authors()` | $0.05 |
| Sentiment / analysis | Grok + Live Search | ~$0.25 |

## Instructions

### 1. Initialize

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()
```

### 2. Direct API Endpoints (structured data, cheap)

```python
# Profile lookup ($0.002/user)
users = client.x_user_lookup(["blockrunai", "elonmusk"])
for u in users.users:
    print(f"@{u.userName}: {u.followers} followers")

# Followers ($0.05/page, ~200 accounts)
result = client.x_followers("blockrunai")
for f in result.followers:
    print(f"@{f.get('userName', '?')} - {f.get('description', '')}")

# Paginate
while result.has_next_page:
    result = client.x_followers("blockrunai", cursor=result.next_cursor)

# User's tweets ($0.032/page)
tweets = client.x_user_tweets("blockrunai")
for t in tweets.tweets:
    print(f"{t.text[:80]}... | {t.favorite_count} likes")

# Trending ($0.002)
trending = client.x_trending()
for topic in trending.data.get("trends", []):
    print(f"{topic.get('name')} — {topic.get('tweet_count', '?')} tweets")

# Search ($0.032/page)
results = client.x_search("AI agents")
for t in results.tweets:
    author = t.author.get("userName", "?") if t.author else "?"
    print(f"@{author}: {t.text[:80]}...")

# Author analytics ($0.02)
analytics = client.x_author_analytics("blockrunai")
score = analytics.data.get("score", "N/A")
print(f"Author score: {score}")

# Compare authors ($0.05)
comparison = client.x_compare_authors("elonmusk", "sama")

# Single profile ($0.002)
info = client.x_user_info("blockrunai")
print(f"Bio: {info.data.get('description', '')}")

# Verified followers ($0.048/page)
verified = client.x_verified_followers("elonmusk")

# Mentions ($0.032/page)
mentions = client.x_user_mentions("blockrunai")

# Tweet details ($0.16/batch, up to 200 IDs)
tweet = client.x_tweet_lookup(["1234567890"])

# Replies ($0.032/page)
replies = client.x_tweet_replies("1234567890")

# Full thread ($0.032/page)
thread = client.x_tweet_thread("1234567890")

# Viral articles ($0.05)
articles = client.x_articles_rising()
```

### 3. Grok Live Search (sentiment analysis, expensive)

Use when users want analysis, sentiment, or natural-language summaries of X activity:

```python
response = client.chat(
    "xai/grok-3",
    f"Analyze @{username}'s recent X activity. Include: recent posts, engagement patterns, content themes.",
    search_parameters={
        "mode": "on",
        "sources": [{"type": "x", "included_x_handles": [username], "post_favorite_count": 5}],
        "max_search_results": 15,
        "return_citations": True
    }
)
```

Cost: ~$0.025/source, so 10-15 sources = $0.25-0.38.

### 4. When to Use Which

| Need | Use | Why |
|------|-----|-----|
| Structured data (profiles, follower lists, tweets) | Direct endpoints | 10-100x cheaper |
| Sentiment, analysis, summaries | Grok Live Search | AI-generated insights |
| Trending topics | `x_trending()` | $0.002, instant |
| Follower/following audit | `x_followers()` + `x_followings()` | Paginated, complete data |

## Requirements

- BlockRun SDK: `pip install blockrun-llm`
- USDC wallet (auto-created on first use)
- Fund with $1-5 USDC on Base
