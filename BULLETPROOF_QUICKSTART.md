# BlockRun Quickstart (Can't Fail)

**Time:** 60 seconds | **Difficulty:** Zero | **Prerequisites:** None

---

## Step 1: Install (10 seconds)

**For Claude Code:**
```bash
/plugin install github:BlockRunAI/claude-code-blockrun-wallet
pip install blockrun-llm
```

**Verify it worked:**
```bash
python -c "from blockrun_llm import LLMClient; c = LLMClient(); print('Wallet:', c.get_wallet_address())"
```

See a wallet address (0x...)? You're good. Move to step 2.

---

## Step 2: Fund Your Wallet (one-time)

**Get your wallet address:**
```bash
python -c "from blockrun_llm import LLMClient; c = LLMClient(); print(c.get_wallet_address())"
```

Copy this address. Send **$1-5 USDC on Base network** to it.

### What $1 Gets You

| $1 USDC = | Calls |
|-----------|-------|
| GPT-4o queries | ~1,000 |
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
| "blockrun GPT review this code" | GPT-4o reviews it |
| "blockrun deepseek summarize this" | DeepSeek (10x cheaper) |
| "blockrun check balance" | Shows USDC balance |

---

## Troubleshooting

### "Insufficient balance"

Send more USDC to your wallet. Check balance:
```bash
python ~/.blockrun/scripts/run.py --balance
```

### "Wallet not found"

Run any command once - wallet auto-creates:
```bash
python ~/.blockrun/scripts/run.py --models
```

### "Command not found"

Make sure you installed:
```bash
pip install blockrun-llm
```

---

## Need Help?

- Email: care@blockrun.ai
- Twitter: [@BlockRunAI](https://x.com/BlockRunAI)

---

**Total time:** Under 2 minutes (after USDC setup)

**Zero config. Zero API keys. Just works.**
