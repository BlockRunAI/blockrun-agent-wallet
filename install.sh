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

# Print WHY/HOW immediately - before any pip noise gets collapsed
cat << 'EOF'

Why BlockRun?
--------------------------------------------------
BlockRun gives your AI agent a crypto wallet so it can pay
for premium APIs directly. No API keys needed - just fund
the wallet and use capabilities like DALL-E, Grok, GPT-5.

How to use: Just ask "blockrun <request>"
--------------------------------------------------

EOF

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
from blockrun_llm import setup_agent_wallet, save_wallet_qr, get_wallet_address

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
    print('NEXT STEP: Fund your wallet')
    print('-' * 50)
    print()
    print('Send USDC (Base network) to:')
    print(f'  {addr}')
    print()
    print('Start with $1-5 USDC - that\'s 25-125 images or 100+ API calls!')
    print()
    print('-' * 50)
    print('Scan QR code with your crypto wallet app:')
    print('-' * 50)
    # Save QR without opening - bash will open AFTER all text prints
    qr_path = save_wallet_qr(addr)
    print(f'QR code saved: {qr_path}')
    print(f'Or view on Base: https://basescan.org/address/{addr}')

else:
    print('Ready to use! Try these:')
    print('-' * 50)
    print('  "blockrun generate an image of a cyberpunk cityscape"')
    print('  "blockrun check @blockrunai on X for latest posts"')
    print('  "blockrun what\'s the latest news about AI agents"')
    print('  "blockrun GPT explain this error message"')
    print('  "blockrun deepseek solve this algorithm"')
    print()
    print('Full docs: https://github.com/BlockRunAI/blockrun-agent-wallet')

print()
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
