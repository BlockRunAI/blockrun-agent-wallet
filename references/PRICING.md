# BlockRun Pricing Guide

## Live Pricing

**Always up-to-date at:** https://blockrun.ai/api/pricing

View in terminal:
```bash
python run.py --models
```

## How Pricing Works

1. **No Subscriptions** - Pay per request only
2. **No API Keys** - Your wallet IS your API key
3. **Transparent** - Prices from API
4. **Instant** - Payments settle on Base chain

## Cost Optimization Tips

### Use `--cheap` Flag
```bash
python run.py "Simple task" --cheap
# Routes to DeepSeek (cheapest)
```

### Use `--fast` Flag
```bash
python run.py "Quick question" --fast
# Routes to GPT-5-mini (fastest)
```

### Choose Right Model for Task
- **Quick questions**: gpt-5-mini, claude-haiku
- **Bulk processing**: deepseek-chat
- **Quality matters**: gpt-5.2, claude-sonnet-4

## Funding Your Wallet

1. Buy USDC on Coinbase
2. Send to your wallet address (shown on first run)
3. Start using models

Check balance:
```bash
python run.py --balance
```

## What $1 USDC Gets You

Approximate calls per $1:
- GPT-5: ~1,000 calls
- DeepSeek: ~10,000 calls
- Grok: ~500 calls
- DALL-E images: ~20 images

**$1 is enough for weeks of normal use.**

---

*Prices from live API - always current.*
