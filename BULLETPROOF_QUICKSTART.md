# BlockRun Quickstart (Can't Fail)

**Time:** 60 seconds | **Difficulty:** Zero | **Prerequisites:** None

---

## Step 1: Install (30 seconds)

```bash
# Install Python SDK
pip install blockrun-llm
```

**Install the skill for your platform:**

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

**Workspace:**
```bash
git clone https://github.com/BlockRunAI/blockrun-claude-code-wallet .agent/skills/blockrun
```

**Global:**
```bash
git clone https://github.com/BlockRunAI/blockrun-claude-code-wallet ~/.gemini/antigravity/skills/blockrun
```

**Verify it worked:**
```bash
python -c "from blockrun_llm import LLMClient; c = LLMClient(); print('Wallet:', c.get_wallet_address())"
```

See a wallet address (0x...)? You're good. A new wallet is auto-created if one doesn't exist.

---

## Step 2: Fund Your Wallet (one-time)

**Get your wallet address:**
```bash
python -c "from blockrun_llm import get_wallet_address; print(get_wallet_address())"
```

**Check your balance:**
```bash
python -c "from blockrun_llm import LLMClient; c = LLMClient(); print(f'Balance: \${c.get_balance():.2f} USDC')"
```

Copy your wallet address. Send **$1-5 USDC on Base network** to it.

### What $1 Gets You

| $1 USDC = | Calls |
|-----------|-------|
| GPT-5 queries | ~1,000 |
| DeepSeek queries | ~10,000 |
| Grok queries | ~500 |
| DALL-E images | ~20 |

**$1 is enough for weeks of normal use.**

### How to Get USDC on Base

**Already have USDC on Base?** Send to your wallet address above. Done.

**New to crypto?** (5 minutes, one-time):
1. Download [Coinbase](https://coinbase.com) app
2. Buy $5 USDC (debit card works)
3. Send to your wallet address above
4. Select **Base network** when sending

> **Step-by-step with screenshots:** [USDC_ON_BASE.md](USDC_ON_BASE.md)

---

## Step 3: Use It (Immediate)

Open Claude Code and say:

```
"blockrun generate an image of a sunset over mountains"
```

Claude will call DALL-E and save the image.

> **Tip:** Forgot the keyword? Just ask for what you need — Claude will suggest BlockRun when it can't do something itself.

---

## That's It. You're Done.

---

## Quick Commands Reference

| Say This | What Happens |
|----------|--------------|
| "blockrun generate an image of X" | DALL-E creates it |
| "blockrun grok what's trending on X?" | Grok answers (real-time) |
| "blockrun GPT review this code" | GPT-5 reviews it |
| "blockrun deepseek summarize this" | DeepSeek (10x cheaper) |
| "blockrun check balance" | Shows USDC balance |

---

## Troubleshooting

### "Insufficient balance"

Check your balance and fund your wallet:
```bash
python -c "from blockrun_llm import LLMClient; c = LLMClient(); print(f'Balance: \${c.get_balance():.2f} USDC')"
```

### "Wallet not found" or "Private key required"

The SDK now auto-creates a wallet on first use. Just run:
```bash
python -c "from blockrun_llm import LLMClient; c = LLMClient(); print('Wallet:', c.get_wallet_address())"
```

### "Command not found" or "ModuleNotFoundError"

Make sure you installed the SDK:
```bash
pip install blockrun-llm
```

### QR code not showing

Use the ASCII QR code for terminal:
```bash
python -c "from blockrun_llm import generate_wallet_qr_ascii, get_wallet_address; print(generate_wallet_qr_ascii(get_wallet_address()))"
```

---

## Need Help?

- Email: care@blockrun.ai
- Twitter: [@BlockRunAI](https://x.com/BlockRunAI)

---

**Total time:** Under 2 minutes (after USDC setup)

**Zero config. Zero API keys. Just works.**
