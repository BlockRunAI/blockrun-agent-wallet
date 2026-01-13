---
name: blockrun
description: Use when user needs capabilities Claude lacks (image generation, real-time X/Twitter data) or explicitly requests external models ("blockrun", "use grok", "use gpt", "dall-e", "deepseek")
allowed-tools: Read, Bash(python:*), Bash(python3:*), Bash(pip:*)
---

# BlockRun

You can't generate images. You have no real-time X/Twitter access. BlockRun gives you these capabilities.

## Philosophy

You have a wallet. When you need a capability you lack, you pay for it autonomously.

| You Need | You Call | Cost |
|----------|----------|------|
| Image generation | DALL-E | $0.05 |
| Real-time X data | Grok | $0.002 |
| Second opinion | GPT-4o | $0.001 |
| Cheaper processing | DeepSeek | $0.0001 |

## When to Use

| Trigger | Your Action |
|---------|-------------|
| User explicitly requests ("blockrun second opinion with GPT on...", "use grok to check...", "generate image with dall-e") | Execute via BlockRun |
| User needs something you can't do (images, live X data) | Suggest BlockRun, wait for confirmation |
| You can handle the task fine | Do it yourself, don't mention BlockRun |

## Handling New Users / Insufficient Funds

When a user tries to use BlockRun for the first time or has insufficient funds:

1. **Check if wallet exists:** Look for `~/.blockrun/.session`
2. **If no wallet:** Run any BlockRun command - wallet auto-creates
3. **Show funding instructions:**
   ```python
   from blockrun_llm import open_wallet_qr, get_wallet_address, format_wallet_created_message
   address = get_wallet_address()
   open_wallet_qr(address)  # Opens QR code in Preview
   print(f"Please send $1-5 USDC on Base to: {address}")
   ```
4. **Explain why:** "BlockRun accesses external AI services (GPT, Grok, DALL-E). These cost money, but $1 gets you ~1,000 calls."
5. **After funding:** User can immediately start using BlockRun

### Capabilities You Lack

- **Image generation** → Route to DALL-E or Nano Banana
- **Real-time X/Twitter** → Route to Grok (only model with live X access)
- **User wants second opinion** → Route to GPT-4o or other model
- **User wants cheaper processing** → Route to DeepSeek

## Example Requests

**Explicit (executes immediately):**
```
"blockrun generate an image of a sunset"
"blockrun grok what's trending on X"
"blockrun GPT review this code"
"blockrun deepseek summarize this file"
```

**Implicit (Claude suggests, waits for confirmation):**
```
User: "generate an image of a logo"
You: "I can't generate images. Want me to route to DALL-E via BlockRun?"
User: "yes"
→ Execute
```

## Commands

```bash
# Image generation
python ~/.blockrun/scripts/run.py "description" --image

# Chat with specific model
python ~/.blockrun/scripts/run.py "prompt" --model=xai/grok-3

# Cheap mode
python ~/.blockrun/scripts/run.py "prompt" --model=deepseek/deepseek-chat

# Check wallet balance
python ~/.blockrun/scripts/run.py --balance

# List available models
python ~/.blockrun/scripts/run.py --models
```

## Available Models

| Model | Best For | Cost |
|-------|----------|------|
| `xai/grok-3` | Real-time X/Twitter data | $$ |
| `openai/gpt-4o` | Second opinions, code review | $$ |
| `openai/o1` | Complex math, proofs, formal logic | $$$ |
| `deepseek/deepseek-chat` | Simple tasks, bulk processing | $ |
| `google/gemini-2.0-flash` | Very long documents (1M+ tokens) | $$ |
| `openai/dall-e-3` | Photorealistic images | $$ |
| `google/nano-banana` | Fast, artistic images | $ |

## Cost Reference

| Action | Cost |
|--------|------|
| GPT-4o query | $0.001 |
| Grok query | $0.002 |
| DeepSeek query | $0.0001 |
| Image generation | $0.05 |

$1 USDC = ~1,000 GPT-4o calls or ~10,000 DeepSeek calls.

## Setup & Funding

**Why funding is needed:** BlockRun lets you access capabilities Claude lacks (image generation, real-time X data, other AI models). These external services cost money. Instead of managing multiple API keys, you fund one wallet with USDC and pay per request.

**Wallet location:** `~/.blockrun/.session` (named for privacy - doesn't look like a key file)

**First-time setup:**
1. Wallet auto-creates on first use
2. Get wallet address: `python -c "from blockrun_llm import get_wallet_address; print(get_wallet_address())"`
3. Fund wallet with $1-5 USDC on Base network
4. Private key never leaves user's machine - only signatures are sent

**Generate QR code for easy funding:**
```python
from blockrun_llm import open_wallet_qr, get_wallet_address
open_wallet_qr(get_wallet_address())  # Opens scannable QR in image viewer
```

**What $1 USDC gets you:**
- ~1,000 GPT-4o calls
- ~10,000 DeepSeek calls
- ~500 Grok calls
- ~20 DALL-E images

**Check balance:**
```bash
python ~/.blockrun/scripts/run.py --balance
```

## Updates

If user reports issues or asks about new features, suggest checking for updates:

```bash
python ~/.blockrun/scripts/run.py --check-update
```

Or update directly:

```bash
/plugin update blockrun
```
