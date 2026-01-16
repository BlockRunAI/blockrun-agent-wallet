---
name: blockrun
description: Use when user needs capabilities Claude lacks (image generation, real-time X/Twitter data) or explicitly requests external models ("blockrun", "use grok", "use gpt", "dall-e", "deepseek"). For Antigravity users, also use when credits are exhausted, stuck in refactoring loops, or need a second opinion on Gemini's code.
allowed-tools: Read, Bash(python:*), Bash(python3:*), Bash(pip:*), Bash(source:*), Bash(open:*), Bash(xdg-open:*)
---

# BlockRun

**BlockRun works with Claude Code and Google Antigravity.**

You can't generate images. You have no real-time X/Twitter access. BlockRun gives you these capabilities.

> **CRITICAL: Always run ONE Python script per task.** Never run multiple separate Python commands - combine all operations into a single script. This avoids multiple permission prompts and provides a better user experience.

## Philosophy

You have a wallet. When you need a capability you lack, you pay for it autonomously.

| You Need | You Call | Pricing |
|----------|----------|---------|
| Image generation | DALL-E | $0.04/image |
| Real-time X data | Grok + Live Search | $0.025/source |
| Second opinion | GPT-5.2 | $1.75/M input, $14/M output |
| Cheaper processing | DeepSeek | $0.14/M input, $0.28/M output |

**How it works:** BlockRun uses x402 micropayments to route your requests to OpenAI, xAI, Google, and other providers. No API keys needed - your wallet pays per token.

## Budget Control (Optional)

If the user specifies a budget (e.g., "use at most $1"), track spending and stop when budget is reached:

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()
budget = 1.0  # User's budget

# Before each call, check if within budget
spending = client.get_spending()
if spending['total_usd'] >= budget:
    print(f"Budget reached: ${spending['total_usd']:.4f} spent")
    # Stop making calls
else:
    response = client.chat("openai/gpt-5.2", "Hello!")

# At the end, report spending
spending = client.get_spending()
print(f"💰 Total spent: ${spending['total_usd']:.4f} across {spending['calls']} calls")
```

## When to Use

| Trigger | Your Action |
|---------|-------------|
| User explicitly requests ("blockrun second opinion with GPT on...", "use grok to check...", "generate image with dall-e") | Execute via BlockRun |
| User needs something you can't do (images, live X data) | Suggest BlockRun, wait for confirmation |
| You can handle the task fine | Do it yourself, don't mention BlockRun |

### Antigravity-Specific Triggers

| Trigger | Your Action |
|---------|-------------|
| Antigravity credits exhausted / rate limited | Suggest BlockRun to continue working with DeepSeek or GPT |
| Gemini stuck in refactoring loop (repeated edits, no progress) | Call GPT or Claude via BlockRun to break the cycle |
| User wants code review on Gemini's output | Call GPT or Claude for a second opinion |
| Complex build failing with Gemini | Suggest external model review before continuing |

## Example User Prompts

Users will say things like:

| User Says | What You Do |
|-----------|-------------|
| "blockrun generate an image of a sunset" | Call DALL-E via ImageClient |
| "use grok to check what's trending on X" | Call Grok with `search=True` |
| "blockrun GPT review this code" | Call GPT-5.2 via LLMClient |
| "what's the latest news about AI agents?" | Suggest Grok (you lack real-time data) |
| "generate a logo for my startup" | Suggest DALL-E (you can't generate images) |
| "blockrun check my balance" | Show wallet balance via `get_balance()` |
| "blockrun show qr code" | Show funding QR code (save to file, open in browser) |
| "blockrun deepseek summarize this file" | Call DeepSeek for cost savings |

### Antigravity User Prompts

| User Says | What You Do |
|-----------|-------------|
| "I ran out of Antigravity credits" | Suggest BlockRun: "Your BlockRun wallet can keep you working. Want me to route this task through DeepSeek?" |
| "Gemini keeps refactoring in circles" | Call GPT/Claude: "Let me get a fresh perspective from GPT to break this loop." |
| "Review what Gemini just did" | Call GPT/Claude for second opinion on the code |
| "This complex refactor isn't working with Gemini" | Suggest external review: "GPT might catch edge cases Gemini missed." |

## Wallet & Balance

**IMPORTANT: Run ONE script per task.** Do not run multiple Python commands separately - combine them into a single script to avoid multiple permission prompts.

**Check balance (single script):**
```python
from blockrun_llm import setup_agent_wallet
client = setup_agent_wallet()
print(f"Wallet: {client.get_wallet_address()}")
print(f"Balance: ${client.get_balance():.2f} USDC")
```

**Show QR code for funding (single script):**
```python
import subprocess
from pathlib import Path
from blockrun_llm import get_wallet_address
import qrcode

addr = get_wallet_address()
qr = qrcode.make(addr)
qr_path = Path.home() / ".blockrun" / "wallet_qr.png"
qr_path.parent.mkdir(parents=True, exist_ok=True)
qr.save(str(qr_path))
subprocess.run(["open", str(qr_path)])
print(f"QR saved: {qr_path}")
print(f"Address: {addr}")
print(f"Fund: https://basescan.org/address/{addr}")
```

## SDK Usage

**Prerequisite:** Install the SDK with `pip install blockrun-llm`

### Basic Chat
```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()  # Auto-creates wallet if needed
response = client.chat("openai/gpt-5.2", "What is 2+2?")
print(response)

# Check spending
spending = client.get_spending()
print(f"Spent ${spending['total_usd']:.4f}")
```

### Real-time X/Twitter Search (xAI Live Search)

**IMPORTANT:** For real-time X/Twitter data, you MUST enable Live Search with `search=True` or `search_parameters`.

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()

# Simple: Enable live search with search=True
response = client.chat(
    "xai/grok-3",
    "What are the latest posts from @blockrunai on X?",
    search=True  # Enables real-time X/Twitter search
)
print(response)
```

### Advanced X Search with Filters

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()

response = client.chat(
    "xai/grok-3",
    "Analyze @blockrunai's recent content and engagement",
    search_parameters={
        "mode": "on",
        "sources": [
            {
                "type": "x",
                "included_x_handles": ["blockrunai"],
                "post_favorite_count": 5
            }
        ],
        "max_search_results": 20,
        "return_citations": True
    }
)
print(response)
```

### Image Generation
```python
from blockrun_llm import ImageClient

client = ImageClient()
result = client.generate("A cute cat wearing a space helmet")
print(result.data[0].url)
```

## xAI Live Search Reference

Live Search is xAI's real-time data API. Cost: **$0.025 per source** (default 10 sources = ~$0.26).

To reduce costs, set `max_search_results` to a lower value:
```python
# Only use 5 sources (~$0.13)
response = client.chat("xai/grok-3", "What's trending?",
    search_parameters={"mode": "on", "max_search_results": 5})
```

### Search Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | string | "auto" | "off", "auto", or "on" |
| `sources` | array | web,news,x | Data sources to query |
| `return_citations` | bool | true | Include source URLs |
| `from_date` | string | - | Start date (YYYY-MM-DD) |
| `to_date` | string | - | End date (YYYY-MM-DD) |
| `max_search_results` | int | 10 | Max sources to return (customize to control cost) |

### Source Types

**X/Twitter Source:**
```python
{
    "type": "x",
    "included_x_handles": ["handle1", "handle2"],  # Max 10
    "excluded_x_handles": ["spam_account"],        # Max 10
    "post_favorite_count": 100,  # Min likes threshold
    "post_view_count": 1000      # Min views threshold
}
```

**Web Source:**
```python
{
    "type": "web",
    "country": "US",  # ISO alpha-2 code
    "allowed_websites": ["example.com"],  # Max 5
    "safe_search": True
}
```

**News Source:**
```python
{
    "type": "news",
    "country": "US",
    "excluded_websites": ["tabloid.com"]  # Max 5
}
```

## Available Models

| Model | Best For | Pricing |
|-------|----------|---------|
| `openai/gpt-5.2` | Second opinions, code review, general | $1.75/M in, $14/M out |
| `openai/gpt-5-mini` | Cost-optimized reasoning | $0.30/M in, $1.20/M out |
| `openai/o4-mini` | Latest efficient reasoning | $1.10/M in, $4.40/M out |
| `openai/o3` | Advanced reasoning, complex problems | $10/M in, $40/M out |
| `xai/grok-3` | Real-time X/Twitter data | $3/M + $0.025/source |
| `deepseek/deepseek-chat` | Simple tasks, bulk processing | $0.14/M in, $0.28/M out |
| `google/gemini-2.5-flash` | Very long documents, fast | $0.15/M in, $0.60/M out |
| `openai/dall-e-3` | Photorealistic images | $0.04/image |
| `google/nano-banana` | Fast, artistic images | $0.01/image |

*M = million tokens. Actual cost depends on your prompt and response length.*

## Cost Reference

All LLM costs are per million tokens (M = 1,000,000 tokens).

| Model | Input | Output |
|-------|-------|--------|
| GPT-5.2 | $1.75/M | $14.00/M |
| GPT-5-mini | $0.30/M | $1.20/M |
| Grok-3 (no search) | $3.00/M | $15.00/M |
| DeepSeek | $0.14/M | $0.28/M |

| Fixed Cost Actions | |
|-------|--------|
| Grok Live Search | $0.025/source (default 10 = $0.25) |
| DALL-E image | $0.04/image |
| Nano Banana image | $0.01/image |

**Typical costs:** A 500-word prompt (~750 tokens) to GPT-5.2 costs ~$0.001 input. A 1000-word response (~1500 tokens) costs ~$0.02 output.

## Setup & Funding

**Wallet location:** `$HOME/.blockrun/.session`

**First-time setup (single script - does everything):**
```python
import subprocess
from pathlib import Path
from blockrun_llm import setup_agent_wallet
import qrcode

# Setup wallet and show status
client = setup_agent_wallet()
addr = client.get_wallet_address()
balance = client.get_balance()

print(f"Wallet: {addr}")
print(f"Balance: ${balance:.2f} USDC")

# Generate and open QR code
qr = qrcode.make(addr)
qr_path = Path.home() / ".blockrun" / "wallet_qr.png"
qr_path.parent.mkdir(parents=True, exist_ok=True)
qr.save(str(qr_path))
subprocess.run(["open", str(qr_path)])
print(f"QR code opened. Fund with $1-5 USDC on Base.")
```

## Troubleshooting

**"Grok says it has no real-time access"**
→ You forgot to enable Live Search. Add `search=True`:
```python
response = client.chat("xai/grok-3", "What's trending?", search=True)
```

**Module not found**
→ Install the SDK: `pip install blockrun-llm`

## Updates

```bash
pip install --upgrade blockrun-llm
```
