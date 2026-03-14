# SocialClaw

<div align="center">

<img src="assets/banner.png" alt="SocialClaw" width="600" />

<h3>Grow your X/Twitter presence with AI-powered intelligence</h3>

<p>Competitor research, audience insights, trend discovery, and engagement strategy — all from your AI coding agent. No API keys needed.</p>

<br />

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-Compatible-412991.svg)](https://openai.com/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-Compatible-4285F4.svg)](https://github.com/google-gemini/gemini-cli)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-000000.svg)](https://cursor.com)

[Tutorials](#tutorials) · [Get Started](#get-started) · [Docs](docs/) · [Pricing](docs/pricing.md)

</div>

---

## Tutorials

### How to spy on your competitors

Find out what your competitor is doing on X — their posting strategy, who talks about them, and their most influential followers.

```
"Run a SocialClaw insight on @competitor"
```

Your AI agent will:
1. Pull their full profile — followers, following, tweet count, verification
2. Find their 20 most recent mentions — who's talking about them and with how much engagement
3. Rank their followers by influence — find the big accounts following them

**What you'll learn:**
- How engaged their audience really is (not just follower count)
- Which influencers are in their orbit
- Their follower/following ratio (a key credibility signal)

---

### How to find what to post about

Stop guessing. See what's actually trending and what content is getting engagement right now.

```
"Run a SocialClaw radar on AI agents"
```

Your AI agent will:
1. Show you today's trending topics with view counts (Anthropic: 115M views, OpenAI: 51M views...)
2. Pull the latest 20 tweets about your topic — see what people are saying
3. Surface viral articles that are rising right now

**What you'll learn:**
- Which topics have momentum today
- What content format is getting engagement
- Angle ideas for your next post

---

### How to find influencers in your niche

Discover the key voices in any topic — ranked by influence, ready for outreach or collaboration.

```
"Run a SocialClaw scout on base blockchain"
```

Your AI agent will:
1. Search X for your topic
2. Extract every unique author from the results
3. Batch-lookup their profiles and rank by follower count

**What you'll learn:**
- Top 20 voices in your space with follower counts and bios
- Who to follow, engage with, or pitch for collaboration
- The accounts that are actually driving conversation (not just big, but active)

---

### How to find high-value conversations to join

Engagement is the fastest growth lever on X. SocialClaw finds the conversations worth your time.

```
"Run a SocialClaw hitlist on AI agents crypto"
```

Your AI agent will:
1. Search for recent tweets on your topic
2. Rank them by engagement (likes + retweets) × author influence
3. Suggest reply angles for each conversation

**What you'll learn:**
- Which conversations are getting traction right now
- Who's posting them (and how many followers they have)
- How to craft a reply that gets noticed

---

### How to understand your audience

Who actually follows your competitors? Are they crypto people? Developers? VCs? Segment by influence tier and find patterns.

```
"Run a SocialClaw audience analysis on @competitor"
```

Your AI agent will:
1. Pull 200 followers
2. Batch-lookup the top 50 by follower count for detailed profiles
3. Segment into tiers: Mega (100K+), Macro (10K-100K), Micro (1K-10K)
4. Analyze bios for common themes

**What you'll learn:**
- Audience composition by influence tier
- Common interests (from bio keywords)
- Potential partners or leads from the Mega/Macro tier

---

### How to do a daily growth check-in

Run this every morning. 2 minutes, 3 actions for the day.

```
"Run a SocialClaw brief on @myaccount"
```

Your AI agent will:
1. Check who mentioned you overnight
2. Show what's trending in your space
3. Surface any rising viral content
4. Give you 3 concrete actions for today

**Example output:**
```
SUGGESTED ACTIONS
  1. Reply to @Rich_lifee_ — they're talking about you to 5K followers
  2. Create content around "Anthropic" trend (115M views today)
  3. Share perspective on rising "AI agents" article
```

---

### How to benchmark against a competitor

Side-by-side comparison — see where you're winning and where to improve.

```
"Run a SocialClaw compare on @me vs @competitor"
```

Your AI agent will:
1. Pull both profiles side-by-side
2. Compare mention engagement (who gets more buzz?)
3. Compare follower quality (who has bigger accounts following them?)

**What you'll learn:**
- Raw numbers: followers, tweets, verification
- Engagement quality: who actually gets talked about more
- Audience quality: whose followers have more influence

---

## Get Started

**Claude Code:**
```
try https://github.com/BlockRunAI/socialclaw
```

**Codex / Cursor / any agent:**
```bash
pip install blockrun-llm[solana]
```

**CLI:**
```bash
git clone https://github.com/BlockRunAI/socialclaw && cd socialclaw
pip install blockrun-llm[solana]
python scripts/socialclaw.py insight @anyuser
```

**Wallet auto-detected.** SocialClaw scans your `~/` directory for any USDC wallet (Base or Solana). No config needed.

---

## Works With Every AI Agent

SocialClaw is a Python SDK. It works anywhere Python runs.

| Platform | How it works |
|----------|-------------|
| **Claude Code** | Loads as a skill. Agent reads SKILL.md, calls SDK automatically. |
| **OpenAI Codex** | Executes Python in sandbox. Import SDK, run workflows. |
| **Gemini CLI** | Loads as Antigravity skill. Same SDK, same workflows. |
| **Cursor / Windsurf** | Agent reads CLAUDE.md for context, calls SDK via terminal. |
| **Any terminal** | `python scripts/socialclaw.py insight @user` |
| **Your own agent** | `from blockrun_llm import SolanaLLMClient` |

---

## How It Works

```
   You: "spy on @competitor"
    ↓
   SocialClaw finds your USDC wallet (auto-scan ~/.<any>/)
    ↓
   Calls BlockRun API → pays per request via x402
    ↓
   Data saved locally (~/.blockrun/data/)
    ↓
   AI agent synthesizes into actionable growth insights
```

- **No API keys.** Your wallet IS your authentication.
- **No subscriptions.** Pay only for what you use.
- **Private key stays local.** Only cryptographic signatures are sent — like signing a MetaMask tx.
- **Data is yours.** Every response saved as JSON in `~/.blockrun/data/`.

---

## Docs

| | |
|--|--|
| [Pricing](docs/pricing.md) | Workflow costs, API endpoint costs, vs. alternatives |
| [API Reference](docs/api-reference.md) | All 16 X/Twitter endpoints + AI models |

---

<div align="center">

**[blockrun.ai](https://blockrun.ai)** · **[AttentionVC](https://attentionvc.com)** · **[x402 Protocol](https://x402.org)** · **[hello@blockrun.ai](mailto:hello@blockrun.ai)**

Powered by [BlockRun](https://blockrun.ai) × [AttentionVC](https://attentionvc.com) · MIT

</div>
