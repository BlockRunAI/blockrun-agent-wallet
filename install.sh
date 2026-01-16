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

# Verify installation and show status
echo "Verifying..."
python3 <<'PYEOF'
from blockrun_llm import setup_agent_wallet, save_wallet_qr

client = setup_agent_wallet(silent=True)
addr = client.get_wallet_address()
bal = client.get_balance()

# Save QR for later opening
save_wallet_qr(addr)

print()
print('=' * 50)
print('BlockRun installed!')
print('=' * 50)
print(f'Wallet: {addr}')
print(f'Balance: ${bal:.2f} USDC')
print()
print('Capabilities:')
print('• Image Generation: "blockrun generate a sunset" → DALL-E')
print('• Live Twitter/X: "blockrun check @elonmusk" → Real-time data')
print('• AI Models: "blockrun GPT review this code" → GPT-5, Grok, DeepSeek')
print()
if bal == 0:
    print('Fund: Send USDC (Base) to wallet address above')
else:
    print('Ready to use!')
print('=' * 50)
import sys
sys.stdout.flush()
PYEOF

# Small delay to ensure terminal renders all text before opening QR
sleep 0.5

# Open QR code AFTER all text is printed
if [ -f "$HOME/.blockrun/qr.png" ]; then
    open "$HOME/.blockrun/qr.png" 2>/dev/null || xdg-open "$HOME/.blockrun/qr.png" 2>/dev/null || true
fi
