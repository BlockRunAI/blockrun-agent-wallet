# API Reference

All data through [BlockRun](https://blockrun.ai)'s unified gateway, powered by [AttentionVC](https://attentionvc.com).

## Setup

```python
from pathlib import Path

chain_file = Path.home() / ".blockrun" / ".chain"
chain = chain_file.read_text().strip() if chain_file.exists() else "base"

if chain == "solana":
    from blockrun_llm import setup_agent_solana_wallet
    client = setup_agent_solana_wallet(silent=True)
else:
    from blockrun_llm import setup_agent_wallet
    client = setup_agent_wallet(silent=True)
```

## X/Twitter Data (16 endpoints)

| Method | What | Cost |
|--------|------|------|
| `x_user_info(username)` | Profile, bio, stats, verification | $0.002 |
| `x_user_lookup([users])` | Batch profiles, up to 100 | $0.002/user |
| `x_followers(username)` | Follower list ~200/page | $0.05/page |
| `x_followings(username)` | Following list ~200/page | $0.05/page |
| `x_verified_followers(user_id)` | Blue-check followers only | $0.048/page |
| `x_user_tweets(username)` | User's tweets + engagement | $0.032/page |
| `x_user_mentions(username)` | Tweets mentioning user | $0.032/page |
| `x_search(query)` | Search tweets, Latest or Top | $0.032/page |
| `x_trending()` | Trending topics + view counts | $0.002 |
| `x_articles_rising()` | Viral content detection | $0.05 |
| `x_tweet_lookup([ids])` | Batch tweet data, up to 200 | $0.16/batch |
| `x_tweet_replies(tweet_id)` | Replies to a tweet | $0.032/page |
| `x_tweet_thread(tweet_id)` | Full conversation thread | $0.032/page |
| `x_author_analytics(handle)` | Author intelligence score | $0.02 |
| `x_compare_authors(h1, h2)` | Compare two accounts | $0.05 |

## AI Models

| Method | What | Cost |
|--------|------|------|
| `chat(model, prompt)` | GPT-5.2, Grok, DeepSeek, Claude, Gemini | varies |
| `chat(model, prompt, search=True)` | Grok with live X/Twitter search | ~$0.25 |
| `search(query)` | Web + X + news search | ~$0.25 |
| `generate(prompt)` | Image generation (DALL-E, Nano Banana) | $0.01-0.04 |
| `image_edit(prompt, image)` | Image editing | $0.02-0.04 |

## Wallet

SocialClaw auto-scans `~/.<any-folder>/wallet.json` and `solana-wallet.json`.

```python
balance = client.get_balance()
address = client.get_wallet_address()
```

## Data Auto-Save

All responses saved to `~/.blockrun/data/` as timestamped JSON.
