# BlockRun Model Guide

## Live Model List

**Always up-to-date at:** https://blockrun.ai/api/pricing

View in terminal:
```bash
python run.py --models
```

Or fetch directly:
```bash
curl https://blockrun.ai/api/pricing | jq
```

## Smart Routing

BlockRun automatically selects models based on your request:

| Keywords in Prompt | Selected Model |
|--------------------|----------------|
| twitter, X, trending | xai/grok-3 |
| code, python, debug | anthropic/claude-sonnet-4 |
| math, proof, logic | openai/o1-mini |
| document, summarize | google/gemini-2.0-flash |

Override with `--model` flag:
```bash
python run.py "prompt" --model openai/o1
```

## Choosing the Right Model

### For Coding
- anthropic/claude-sonnet-4 (best)
- openai/gpt-5.2 (alternative)
- deepseek/deepseek-chat (budget)

### For Reasoning/Math
- openai/o1 (best)
- openai/o1-mini (balanced)
- deepseek/deepseek-r1 (budget)

### For Real-Time X/Twitter Data
- xai/grok-3 (only option with live X access)

### For Long Documents
- google/gemini-2.0-flash (1M+ context)

### For Budget Operations
- deepseek/deepseek-chat (cheapest)

## Image Generation

View available image models:
```bash
curl https://blockrun.ai/api/v1/images/models | jq
```

Common options:
- google/nano-banana (artistic, fast)
- openai/dall-e-3 (photorealistic)

---

*Model list and pricing from live API - always current.*
