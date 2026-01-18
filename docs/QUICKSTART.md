# BlockRun Quickstart (Can't Fail)

**Time:** 60 seconds | **Difficulty:** Zero | **Prerequisites:** None

---

## Step 1: Install (One Command)

```bash
curl -fsSL https://raw.githubusercontent.com/BlockRunAI/blockrun-agent-wallet/main/install.sh | bash
```

This auto-detects Claude Code or Antigravity and installs everything.

**Verify:**
```bash
python3 -c "from blockrun_llm import status; status()"
```

You should see your wallet address and balance.

---

## Step 2: Fund Your Wallet (one-time)

Copy your wallet address from Step 1. Send **$1-5 USDC on Base network** to it.

### What $1 Gets You

| $1 USDC = | Calls |
|-----------|-------|
| GPT-5 queries | ~1,000 |
| DeepSeek queries | ~10,000 |
| Grok queries | ~500 |
| DALL-E images | ~20 |

**$1 is enough for weeks of normal use.**

### How to Get USDC on Base

**Already have USDC on Base?** Send to your wallet address. Done.

**New to crypto?** (5 minutes, one-time):
1. Download [Coinbase](https://coinbase.com) app
2. Buy $5 USDC (debit card works)
3. Send to your wallet address
4. Select **Base network** when sending

> **Step-by-step with screenshots:** [USDC_ON_BASE.md](USDC_ON_BASE.md)

---

## Step 3: Use It

Open Claude Code or Antigravity and say:

```
"blockrun generate an image of a sunset over mountains"
```

Claude will call DALL-E and save the image.

> **Tip:** Just ask for what you need — Claude will suggest BlockRun when it can't do something itself.

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

### Check status
```bash
python3 -c "from blockrun_llm import status; status()"
```

### "ModuleNotFoundError"
Run the install script again:
```bash
curl -fsSL https://raw.githubusercontent.com/BlockRunAI/blockrun-agent-wallet/main/install.sh | bash
```

### QR code for funding
```bash
python3 -c "from blockrun_llm import generate_wallet_qr_ascii, get_wallet_address; print(generate_wallet_qr_ascii(get_wallet_address()))"
```

---

## Need Help?

- Email: care@blockrun.ai
- Twitter: [@BlockRunAI](https://x.com/BlockRunAI)

---

**Total time:** Under 2 minutes (after USDC setup)

**Zero config. Zero API keys. Just works.**
