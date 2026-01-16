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
python3 - "$SKILLS_DIR" <<'PYEOF'
import subprocess
import sys
from pathlib import Path
from blockrun_llm import setup_agent_wallet
import qrcode
from PIL import Image

skills_dir = Path(sys.argv[1])
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
    # Generate QR code with EIP-681 format for MetaMask compatibility
    # Format: ethereum:USDC_CONTRACT@CHAIN_ID/transfer?address=RECIPIENT
    USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    BASE_CHAIN_ID = 8453
    eip681_uri = f"ethereum:{USDC_BASE}@{BASE_CHAIN_ID}/transfer?address={addr}"

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(eip681_uri)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='black', back_color='white').convert('RGB')

    # Add BlockRun logo in center
    logo_path = skills_dir / 'assets' / 'logo.png'
    if logo_path.exists():
        logo = Image.open(logo_path)
        # Resize logo to fit in center (about 20% of QR size)
        logo_size = qr_img.size[0] // 5
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        # Calculate center position
        pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
        qr_img.paste(logo, pos)

    # Save QR code
    qr_path = Path.home() / '.blockrun' / 'wallet_qr.png'
    qr_path.parent.mkdir(parents=True, exist_ok=True)
    qr_img.save(str(qr_path))

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

    # Open QR code
    try:
        subprocess.run(['open', str(qr_path)], check=True)
    except:
        pass

else:
    print('Ready to use! Try:')
    print('  "blockrun generate an image of a robot"')
    print('  "blockrun check X for @blockrunai posts"')

print()
print('=' * 50)
PYEOF
