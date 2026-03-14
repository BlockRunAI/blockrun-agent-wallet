# SocialClaw — X/Twitter Marketing Intelligence Agent

SocialClaw gives you X/Twitter marketing intelligence and growth analysis, powered by BlockRun's paid APIs (USDC micropayments via x402).

## Workflows

### 1. Insight Report — `insight @username`
Deep-dive on any X account. Calls:
- `/v1/x/users/info` — detailed profile (bio, stats, join date)
- `/v1/x/users/mentions` — who's talking about them
- `/v1/x/users/followers` — follower list with follower counts

Summarize into: audience size, engagement quality, content themes, growth signals.

### 2. Topic Radar — `radar <topic>`
What's hot and what content to create. Calls:
- `/v1/x/trending` — trending topics with article counts and views
- `/v1/x/search` — latest tweets matching the topic (use `sort_order: "Latest"` or `"Top"`)
- `/v1/x/articles/rising` — viral/rising content detection

Summarize into: trending angles, top-performing content formats, suggested post ideas.

### 3. Competitor Compare — `compare @user1 @user2`
Side-by-side analysis of two accounts. Calls:
- `/v1/x/users/info` for both users
- `/v1/x/users/tweets` for both users (may 502, retry once)
- `/v1/x/users/followers` for both users

Summarize into: follower counts, posting frequency, content strategy differences, engagement comparison.

## Additional Endpoints
- `/v1/x/users/lookup` — batch user profiles (up to ~100 at once)
- `/v1/x/users/tweets` — a user's tweets (sometimes returns 502, treat as available and retry once)
- `/v1/images/generations` — generate images for post mockups

## How to Make API Calls
Use `SolanaLLMClient` from the `blockrun-llm` package. All endpoints are on `sol.blockrun.ai`. Example:

```python
from blockrun_llm import SolanaLLMClient
client = SolanaLLMClient()
result = client.request("/v1/x/trending")
```

## Wallet Setup
SocialClaw auto-scans for wallets in:
- `~/.*/ wallet.json` (any dot-folder)
- `~/.*/solana-wallet.json`

No manual config needed — the first valid wallet found is used. Fund it with USDC on Solana.

## Costs
- Each API call costs ~$0.002–$0.05
- A full workflow (insight, radar, or compare) typically costs **$0.08–$0.15**
- Image generation: ~$0.04/image

## API Layer — BlockRun Unified Gateway
SocialClaw routes all requests through BlockRun's unified API gateway (`blockrun.ai` / `sol.blockrun.ai`), which handles payments, routing, and access to X/Twitter data, image generation, LLM models, and search — all in one place.

- Use the `blockrun-llm` SDK (`SolanaLLMClient` or `LLMClient`) for all API calls.
- All capabilities are available through BlockRun's gateway — no need to integrate additional services.
- If an endpoint returns an error, retry once or report the issue.

## Other Guidelines
- Always present results as actionable marketing insights, not raw data dumps.
- When a 502 occurs on `/v1/x/users/tweets`, retry once before giving up.
- Combine multiple endpoint results into a single cohesive analysis.
- All paid data is auto-saved to `~/.blockrun/data/` — never pay twice for the same data.
