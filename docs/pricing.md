# Pricing

## Workflow Costs

| Workflow | API Calls | Cost |
|----------|-----------|------|
| Insight | 3 calls | ~$0.08 |
| Radar | 4 calls | ~$0.07 |
| Compare | 6 calls | ~$0.15 |
| Audience | 3 calls | ~$0.15 |
| Scout | 2 calls | ~$0.07 |
| Hitlist | 1 call | ~$0.03 |
| Brief | 3 calls | ~$0.08 |

**$1 USDC = ~12 full marketing reports.**

## API Endpoint Costs

| Endpoint | What you get | Cost |
|----------|-------------|------|
| `users/info` | Profile, bio, stats, verification | $0.002 |
| `users/lookup` | Batch profiles (up to 100) | $0.002/user |
| `users/followers` | Follower list with stats (~200/page) | $0.05/page |
| `users/followings` | Following list (~200/page) | $0.05/page |
| `users/tweets` | User's tweets with engagement | $0.032/page |
| `users/mentions` | Who's talking about them | $0.032/page |
| `search` | Search tweets (Latest/Top) | $0.032/page |
| `trending` | Trending topics + view counts | $0.002 |
| `articles/rising` | Viral content detection | $0.05 |
| `tweets/lookup` | Batch tweet data (up to 200) | $0.16/batch |
| `tweets/replies` | Replies to a tweet | $0.032/page |
| `tweets/thread` | Full thread context | $0.032/page |
| `x_author_analytics` | Author intelligence score | $0.02 |
| `x_compare_authors` | Compare two accounts | $0.05 |

## AI Models

| Model | Best for | Input | Output |
|-------|----------|-------|--------|
| `openai/gpt-5.2` | General, code review | $1.75/M | $14.00/M |
| `openai/gpt-5-mini` | Fast + cheap | $0.30/M | $1.20/M |
| `xai/grok-3` | Real-time X data | $3.00/M | $15.00/M |
| `deepseek/deepseek-chat` | Bulk processing | $0.28/M | $0.42/M |
| `anthropic/claude-sonnet-4` | Coding | $3.00/M | $15.00/M |
| `google/gemini-2.5-flash` | Long documents | $0.15/M | $0.60/M |

## vs. Alternatives

| What you need | X API Official | SocialClaw |
|--------------|---------------|------------|
| 1 profile lookup | $100/month subscription | $0.002 |
| 1,000 follower profiles | $100/month subscription | $0.25 |
| Trending topics | $100/month subscription | $0.002 |
| Full competitor report | $100/month + build it yourself | $0.15 |

## Payment

- **Protocol:** [x402](https://x402.org) — HTTP 402 micropayments
- **Currency:** USDC on [Base](https://base.org) or [Solana](https://solana.com)
- **No subscriptions.** Pay only for what you use.
