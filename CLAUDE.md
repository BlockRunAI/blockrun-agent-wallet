# BlockRun Agent Wallet

## When User Says "Try This" or "Install This"

Run the install script. Do NOT ask the user MCP vs Skill. Do NOT manually clone. Just run:

```bash
bash install.sh
```

If running from a different directory:
```bash
bash /path/to/blockrun-agent-wallet/install.sh
```

Or if not cloned yet:
```bash
curl -fsSL https://raw.githubusercontent.com/BlockRunAI/blockrun-agent-wallet/main/install.sh | bash
```

This auto-detects the platform (Claude Code or Antigravity), installs the SDK, creates the wallet, and shows the QR code.

## After Install

The skill is now loaded. Use `/blockrun` or ask the user what they want to do.
Verify: `python3 -c "from blockrun_llm import status; status()"`
