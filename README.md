# BlockRun: Give Claude Code a Wallet to Pay for GPT, Grok, DALL-E

<div align="center">

![BlockRun](assets/blockrun-agent-skill.png)

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![Antigravity](https://img.shields.io/badge/Antigravity-Compatible-4285F4.svg)](https://antigravity.google)
[![Models](https://img.shields.io/badge/Models-30+-green.svg)](https://blockrun.ai/models)
[![Providers](https://img.shields.io/badge/Providers-5-blue.svg)](https://blockrun.ai)
[![Payment](https://img.shields.io/badge/Payment-USDC_on_Base-purple.svg)](USDC_ON_BASE.md)
[![No API Keys](https://img.shields.io/badge/API_Keys-None_Required-brightgreen.svg)](https://blockrun.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

**Claude can't generate images. Claude has no real-time X data. Claude stops when rate limited.**

BlockRun fixes this with a wallet.

---

## The Problem

Claude Code is powerful, but it has hard limits:

```
Without BlockRun:              With BlockRun:
────────────────               ─────────────
❌ No image generation         ✅ DALL-E, Nano Banana
❌ No real-time X/Twitter      ✅ Grok has live X access
❌ Rate limits = work stops    ✅ Overflow to DeepSeek
❌ Single perspective          ✅ GPT second opinions
❌ 5 API keys to manage        ✅ One wallet, all models
```

**BlockRun extends Claude with capabilities it doesn't have.**

---

## Philosophy

> **Give your AI agent a wallet. Let it pay for its own superpowers.**

Claude is brilliant — but armless. BlockRun gives it hands.

With BlockRun, your AI agent has its own wallet. When it needs a capability it doesn't have, it pays for it — autonomously.

| Need | Solution | Agent Pays |
|------|----------|------------|
| Generate an image | Calls DALL-E | $0.05 |
| Real-time X data | Calls Grok | $0.002 |
| Second opinion | Calls GPT-5.2 | $0.001 |
| Cheaper processing | Calls DeepSeek | $0.0001 |

No API keys. No human in the loop. Just an agent with a budget, acquiring capabilities on demand.

We don't replace Claude. We give Claude a wallet and let it buy what it needs.

**Today:** Images, real-time data, LLM routing.
**Tomorrow:** Video generation, music creation, and every capability Claude can't do.

---

## Who Is This For?

**This is for people who believe AI agents should have their own wallets.**

You fund the agent with $1-5 USDC. The agent pays for GPT, Grok, DALL-E autonomously. No API keys. No human approval needed for each call.

| You Are... | You Want... | Start Here |
|------------|-------------|------------|
| **Developer** | Call GPT/Grok from Claude Code | [Quickstart](BULLETPROOF_QUICKSTART.md) |
| **AI Power User** | Real-time X data, images | [Quickstart](BULLETPROOF_QUICKSTART.md) |
| **Cost-Conscious** | 90% cheaper AI calls | [Cost Guide](#the-numbers) |
| **MCP Enthusiast** | Prefer MCP over Skills | [MCP Server](#alternative-mcp-server) |

**New to crypto?** [USDC Guide](USDC_ON_BASE.md) explains how to get USDC on Base (5 min setup).

---

## Install

**Step 1: Install the Python SDK**
```bash
pip install blockrun-llm
```

**Step 2: Install the skill for your platform**

### Claude Code

**Option A: Plugin system (recommended)**
```
/plugin marketplace add BlockRunAI/blockrun-claude-code-wallet
/plugin install blockrun
```

**Option B: Git clone**
```bash
git clone https://github.com/BlockRunAI/blockrun-claude-code-wallet ~/.claude/skills/blockrun
```

### Google Antigravity

**Workspace (project-specific):**
```bash
git clone https://github.com/BlockRunAI/blockrun-claude-code-wallet .agent/skills/blockrun
```

**Global (all projects):**
```bash
git clone https://github.com/BlockRunAI/blockrun-claude-code-wallet ~/.gemini/antigravity/skills/blockrun
```

A wallet is auto-created at `~/.blockrun/` on first use.

**Verify it works:**
```bash
python -c "from blockrun_llm import LLMClient; c = LLMClient(); print('Wallet:', c.get_wallet_address())"
```

If you see a wallet address (0x...), you're ready. The SDK will automatically create a new wallet if one doesn't exist.

**Check your balance:**
```bash
python -c "from blockrun_llm import LLMClient; c = LLMClient(); print(f'Balance: \${c.get_balance():.2f} USDC')"
```

**Get funding QR code:**
```bash
# Opens QR code in browser
python -c "from blockrun_llm import open_wallet_qr, get_wallet_address; open_wallet_qr(get_wallet_address())"

# Or show ASCII QR in terminal
python -c "from blockrun_llm import generate_wallet_qr_ascii, get_wallet_address; print(generate_wallet_qr_ascii(get_wallet_address()))"
```

**Update to latest version:**
```bash
# Claude Code
cd ~/.claude/skills/blockrun && git pull

# Antigravity (global)
cd ~/.gemini/antigravity/skills/blockrun && git pull

# SDK
pip install --upgrade blockrun-llm
```

---

## Usage

Just tell Claude:

```
"blockrun generate an image of a sunset"        → DALL-E creates it
"blockrun grok what's trending on X"            → Grok answers (Claude can't)
"blockrun GPT review this code"                 → AI reviewing AI
"blockrun deepseek summarize this file"         → DeepSeek saves 90%
```

Or ask for something Claude can't do — it will suggest BlockRun:

```
User: "generate a logo for my startup"
Claude: "I can't generate images. Want me to route to DALL-E via BlockRun?"
User: "yes"
→ Done
```

---

## What You Get

| Capability | Count | Examples |
|------------|-------|----------|
| **AI Models** | 30+ | GPT-5, Grok, DeepSeek, Gemini, o3 |
| **Providers** | 5 | OpenAI, xAI, Google, DeepSeek, Anthropic |
| **Image Models** | 3 | DALL-E 3, Nano Banana, Flux |
| **Use Cases** | 5 | Images, Real-time, Second Opinion, Cost, Overflow |

---

## The Numbers

| What | Value |
|------|-------|
| Setup time | **60 seconds** (vs 30+ min with API keys) |
| API keys needed | **0** (vs 5 with traditional setup) |
| Cost per GPT-4 call | **$0.001** |
| Calls per $1 | **1,000** (GPT-5) / **10,000** (DeepSeek) |

---

## How It Works

```
1. pip install blockrun-llm
2. First use → Wallet auto-created at ~/.blockrun/
3. Get QR code for easy funding:
   python -c "from blockrun_llm import open_wallet_qr, get_wallet_address; open_wallet_qr(get_wallet_address())"
4. Scan QR with MetaMask, send $1-5 USDC on Base
5. Claude calls any model, pays per request
6. Your private key never leaves your machine
```

### What $1 USDC Gets You

| Model | Calls per $1 |
|-------|--------------|
| GPT-5 | ~1,000 |
| DeepSeek | ~10,000 |
| Grok | ~500 |
| DALL-E images | ~20 |

**$1 is enough for weeks of normal use.**

**New to crypto?** Read our [USDC beginner's guide](USDC_ON_BASE.md).

---

## Use Cases

### Image Generation
Claude can't generate images. BlockRun routes to DALL-E.
```
"blockrun generate a logo for my startup"
```

### Real-Time X/Twitter Data
Claude's knowledge has a cutoff. Grok has live X access.
```
"blockrun what's trending on X about AI agents?"
```

### AI Reviewing AI
Different models catch different bugs.
```
"blockrun GPT review this code for bugs"
```

### Cost Optimization
DeepSeek is 10-50x cheaper for simple tasks.
```
"blockrun deepseek summarize these 500 files"
```

---

## Available Models

BlockRun provides access to the latest models from OpenAI, Anthropic, Google, xAI, and DeepSeek via x402 micropayments.

| Model | Best For | Pricing |
|-------|----------|---------|
| `openai/gpt-5.2` | Second opinions, code review, general | $1.75/M in, $14/M out |
| `openai/gpt-5-mini` | Cost-optimized tasks | $0.30/M in, $1.20/M out |
| `openai/o4-mini` | Efficient reasoning, math | $$ |
| `openai/o3` | Complex reasoning | $$$ |
| `xai/grok-3` | Real-time X/Twitter data | $3/M + $0.025/source |
| `deepseek/deepseek-chat` | Budget tasks, bulk processing | $0.14/M in, $0.28/M out |
| `google/gemini-2.5-flash` | Long documents (1M+ tokens) | $$ |
| `openai/dall-e-3` | Photorealistic images | $0.04/image |
| `google/nano-banana` | Artistic, fast images | $0.01/image |

*Prices in USDC per million tokens (M = 1,000,000 tokens)*

---

## Security

- 🔐 Private key stored locally at `~/.blockrun/`
- ✍️ Only signatures sent to server (key never transmitted)
- 💵 Recommend keeping $5-20 balance
- 🔍 All payments verifiable on [Basescan](https://basescan.org)

---

## Alternative: MCP Server

Prefer MCP over Skills? See [@blockrun/mcp](https://github.com/blockrunai/blockrun-mcp).

Same wallet, same models, different interface.

---

## Links

| Resource | URL |
|----------|-----|
| Website | https://blockrun.ai |
| USDC Guide | [USDC_ON_BASE.md](USDC_ON_BASE.md) |
| Buy USDC | https://coinbase.com |
| Bridge to Base | https://bridge.base.org |
| x402 Protocol | https://x402.org |
| Support | care@blockrun.ai |

---

## A Note from the Builder

I built BlockRun because I got tired of juggling API keys.

Five accounts. Five billing dashboards. Five sets of credentials to rotate. For what? To use AI models that should just work together.

So I made them work together. One wallet. All models. No keys.

If this helps you build something cool, I'd love to hear about it.

— [@bc1beat](https://x.com/bc1beat) | [@1bcMax](https://github.com/1bcMax) | [care@blockrun.ai](mailto:care@blockrun.ai)

---

## License

MIT
