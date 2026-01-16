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
    git clone --depth 1 https://github.com/BlockRunAI/blockrun-agent-wallet "$SKILLS_DIR"
else
    echo "Updating skill..."
    cd "$SKILLS_DIR" && git pull --ff-only
fi

# Install SDK with fallbacks for different Python setups
echo "Installing Python SDK..."
if pip install --upgrade blockrun-llm 2>/dev/null; then
    :
elif pip install --user --upgrade blockrun-llm 2>/dev/null; then
    :
elif pip install --user --break-system-packages --upgrade blockrun-llm 2>/dev/null; then
    :
elif python3 -m pip install --upgrade blockrun-llm 2>/dev/null; then
    :
elif python3 -m pip install --user --upgrade blockrun-llm 2>/dev/null; then
    :
elif python3 -m pip install --user --break-system-packages --upgrade blockrun-llm 2>/dev/null; then
    :
else
    echo "ERROR: Could not install blockrun-llm. Please install manually:"
    echo "  pip install blockrun-llm"
    exit 1
fi

# Verify installation and show status
echo "Verifying..."
python3 <<'PYEOF'
from blockrun_llm import setup_agent_wallet, open_wallet_qr, get_wallet_address

client = setup_agent_wallet(silent=True)
addr = client.get_wallet_address()
bal = client.get_balance()

print()
print('=' * 50)
print('BlockRun installed!')
print('=' * 50)
print(f'Wallet: {addr}')
print(f'Balance: ${bal:.2f} USDC')
print()

if bal == 0:
    # Use SDK's QR generator (EIP-681 format - works with MetaMask)
    qr_path = open_wallet_qr(addr)

    print('NEXT STEP: Fund your wallet to unlock capabilities')
    print('-' * 50)
    print()
    print('Send USDC (Base network) to:')
    print(f'  {addr}')
    print()
    print('What you get:')
    print('  "blockrun generate image of..."    -> DALL-E ($0.04/image)')
    print('  "blockrun what\'s trending on X"   -> Grok Live Search')
    print('  "blockrun GPT review this code"    -> GPT-5 second opinion')
    print()
    print('Start with $1-5 USDC. That\'s 25-125 images or 100+ GPT calls.')
    print()
    print(f'QR code: {qr_path}')
    print(f'View on Base: https://basescan.org/address/{addr}')

else:
    print('Ready to use! Try:')
    print('  "blockrun generate an image of a robot"')
    print('  "blockrun check X for @blockrunai posts"')

print()
print('=' * 50)
PYEOF
