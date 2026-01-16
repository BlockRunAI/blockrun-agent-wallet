#!/bin/bash
# BlockRun Install Script
# One command to install BlockRun skill + SDK

set -e

echo "Installing BlockRun..."

# Detect platform and set skills path
if [ -d "$HOME/.gemini/antigravity" ]; then
    SKILLS_DIR="$HOME/.gemini/antigravity/skills/blockrun"
    echo "Detected Antigravity (global)"
elif [ -d "$HOME/.claude" ]; then
    SKILLS_DIR="$HOME/.claude/skills/blockrun"
    echo "Detected Claude Code"
else
    # Default to Claude Code
    SKILLS_DIR="$HOME/.claude/skills/blockrun"
    mkdir -p "$HOME/.claude/skills"
    echo "Using Claude Code default"
fi

# Clone or update skill
if [ ! -d "$SKILLS_DIR" ]; then
    echo "Cloning skill..."
    mkdir -p "$(dirname "$SKILLS_DIR")"
    git clone --depth 1 --quiet https://github.com/BlockRunAI/blockrun-agent-wallet "$SKILLS_DIR"
else
    echo "Updating skill..."
    cd "$SKILLS_DIR" && git pull --ff-only --quiet
fi

# Install SDK with fallbacks for different Python setups
echo "Installing Python SDK..."
if pip install --upgrade blockrun-llm >/dev/null 2>&1; then
    :
elif pip install --user --upgrade blockrun-llm >/dev/null 2>&1; then
    :
elif pip install --user --break-system-packages --upgrade blockrun-llm >/dev/null 2>&1; then
    :
elif python3 -m pip install --upgrade blockrun-llm >/dev/null 2>&1; then
    :
elif python3 -m pip install --user --upgrade blockrun-llm >/dev/null 2>&1; then
    :
elif python3 -m pip install --user --break-system-packages --upgrade blockrun-llm >/dev/null 2>&1; then
    :
else
    echo "ERROR: Could not install blockrun-llm. Please install manually:"
    echo "  pip install blockrun-llm"
    exit 1
fi

# Verify installation, show status, and write getting started guide
echo "Verifying..."
python3 <<'PYEOF'
import os
from blockrun_llm import setup_agent_wallet, save_wallet_qr

client = setup_agent_wallet(silent=True)
addr = client.get_wallet_address()
bal = client.get_balance()

# Generate QR code (don't auto-open)
save_wallet_qr(addr)

# Write GETTING_STARTED.md
getting_started = f'''# BlockRun - Getting Started

## What is BlockRun?
Your AI agent's crypto wallet. Pay for premium APIs (DALL-E, Grok, GPT-5)
directly - no API keys needed.

## How to Use
Just ask: "blockrun <request>"
- "blockrun generate image of a sunset" → DALL-E ($0.04)
- "blockrun check @blockrunai on X" → Live Twitter data
- "blockrun GPT review this code" → GPT-5 second opinion

## Fund Your Wallet
Send USDC (Base network) to: {addr}
Start with $1-5 USDC (~25-125 images)

View QR: open ~/.blockrun/qr.png
View on Base: https://basescan.org/address/{addr}
'''

blockrun_dir = os.path.expanduser('~/.blockrun')
os.makedirs(blockrun_dir, exist_ok=True)
with open(os.path.join(blockrun_dir, 'GETTING_STARTED.md'), 'w') as f:
    f.write(getting_started)

# Minimal output - just the essentials
print()
print('=' * 50)
print('BlockRun installed!')
print('=' * 50)
print(f'Wallet: {addr}')
print(f'Balance: ${bal:.2f} USDC')
print()
if bal == 0:
    print('Next: Fund wallet with USDC (Base) to enable AI payments.')
print('See: ~/.blockrun/GETTING_STARTED.md')
print('=' * 50)
PYEOF
