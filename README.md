# BlockRun: Real-Time X/Twitter Data & Image Gen for Your AI Agent

<div align="center">

![BlockRun](assets/blockrun-agent-skill.png)

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![Antigravity](https://img.shields.io/badge/Antigravity-Compatible-4285F4.svg)](https://antigravity.google)
[![No API Keys](https://img.shields.io/badge/API_Keys-None_Required-brightgreen.svg)](https://blockrun.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

**Give your AI agent access to X/Twitter data, image generation, and 30+ LLMs — no API keys, just a USDC micropayment wallet.**

---

## What Can You Do Right Now?

### X/Twitter data (Claude and Gemini can't do this)

```
"get followers of @blockrunai"           → follower list with bios, stats
"what's @elonmusk been tweeting?"        → recent tweets with engagement
"what's trending on X?"                  → trending topics with volumes
"search X for AI agent discussions"      → matching tweets and authors
"compare @elonmusk vs @sama"             → side-by-side analytics
"analyze @blockrunai's X presence"       → engagement metrics and score
```

### Image generation & editing (Claude can't do this)

```
"generate a logo for my startup Nexus"   → DALL-E image, $0.04
"edit this image to remove the bg"       → AI image editing, $0.03
```

### Second opinions from other models

```
"GPT review this code for security"      → GPT-5 analysis, $0.02
"deepseek summarize each file in /docs"  → bulk at $0.0001/call
```

**Just ask naturally. No prefix needed.**

---

## Install

In Claude Code, just say:

```
try https://github.com/BlockRunAI/blockrun-agent-wallet
```

Claude will install it, create a USDC wallet, and show a QR code to fund. Done.

<details>
<summary>Other install methods</summary>

- **Shell:** `curl -fsSL https://raw.githubusercontent.com/BlockRunAI/blockrun-agent-wallet/main/install.sh | bash`
- **Solana:** `CHAIN=solana bash install.sh`
- **MCP Server:** `claude mcp add blockrun -- npx @blockrun/mcp`
- **Antigravity:** `git clone https://github.com/BlockRunAI/blockrun-agent-wallet ~/.gemini/antigravity/skills/blockrun`

</details>

---

## X/Twitter Endpoints

15 endpoints your agent can't get natively:

| What you say | Endpoint | Cost |
|-------------|----------|------|
| "get @user's profile" | `x_user_info()` | $0.002 |
| "lookup @user1 @user2" | `x_user_lookup()` | $0.002/user |
| "get followers of @user" | `x_followers()` | $0.05/page |
| "who does @user follow?" | `x_followings()` | $0.05/page |
| "verified followers of @user" | `x_verified_followers()` | $0.048/page |
| "get @user's tweets" | `x_user_tweets()` | $0.032/page |
| "who's mentioning @user?" | `x_user_mentions()` | $0.032/page |
| "get data on this tweet" | `x_tweet_lookup()` | $0.16/batch |
| "show replies to this tweet" | `x_tweet_replies()` | $0.032/page |
| "show the full thread" | `x_tweet_thread()` | $0.032/page |
| "search X for..." | `x_search()` | $0.032/page |
| "what's trending?" | `x_trending()` | $0.002 |
| "what articles are going viral?" | `x_articles_rising()` | $0.05 |
| "analyze @user's presence" | `x_author_analytics()` | $0.02 |
| "compare @user1 vs @user2" | `x_compare_authors()` | $0.05 |

---

## Pricing

| Capability | $1 gets you |
|------------|-------------|
| X trending / profiles | ~500 calls |
| X followers / followings | ~20 pages (~4,000 accounts) |
| X tweets / search | ~31 pages |
| DALL-E images | ~25 images |
| GPT second opinions | ~50 calls |
| DeepSeek bulk processing | ~10,000 calls |

**$1-5 lasts weeks.** Wallet balance = spending cap.

---

## How It Works

Your agent has a USDC wallet. When it needs a capability, it pays per request:

- No API keys to manage
- No monthly subscriptions ($0.002 vs $100/month X API)
- Wallet balance is your spending cap
- Private key stays local (`~/.blockrun/`), never sent to any server

**New to USDC?** [5-minute guide](USDC_ON_BASE.md)

---

## Links

[blockrun.ai](https://blockrun.ai) · [USDC Guide](USDC_ON_BASE.md) · [x402 Protocol](https://x402.org) · [care@blockrun.ai](mailto:care@blockrun.ai)

---

MIT · Built by [@bc1beat](https://x.com/bc1beat)
