#!/usr/bin/env python3
"""
BlockRun Skill Plus - Unified CLI Entry Point

Access unlimited LLM models and image generation through USDC micropayments.
Your private key never leaves your machine - only signatures are transmitted.

Usage:
    python run.py "Your prompt here"
    python run.py "Prompt" --model openai/gpt-4o
    python run.py "Description" --image
    python run.py --balance
    python run.py --models

Environment:
    BLOCKRUN_WALLET_KEY: Your Base chain wallet private key (required)
    BLOCKRUN_API_URL: API endpoint (optional, default: https://blockrun.ai/api)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Optional

# Plugin version (keep in sync with plugin.json)
__version__ = "1.0.0"
GITHUB_PLUGIN_URL = "https://raw.githubusercontent.com/blockrunai/blockrun-agent-skill/main/plugin.json"

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.utils.branding import branding
except ImportError:
    # Fallback if running directly
    from utils.branding import branding

# Try to import blockrun_llm SDK
try:
    from blockrun_llm import LLMClient, ImageClient, APIError, PaymentError
    HAS_SDK = True
except ImportError:
    HAS_SDK = False


def check_environment() -> bool:
    """Check if required environment variables are set."""
    key = os.environ.get("BLOCKRUN_WALLET_KEY") or os.environ.get("BASE_CHAIN_WALLET_KEY")
    if not key:
        branding.print_error(
            "BLOCKRUN_WALLET_KEY environment variable not set",
            help_link="https://blockrun.ai/docs/setup"
        )
        print("  Set your wallet private key:")
        print("    export BLOCKRUN_WALLET_KEY=\"0x...\"")
        print()
        return False
    return True


def get_smart_model(prompt: str, cheap: bool = False, fast: bool = False) -> str:
    """
    Smart model routing based on prompt content and preferences.

    Args:
        prompt: User's prompt text
        cheap: Prefer cost-effective models
        fast: Prefer low-latency models

    Returns:
        Model ID string
    """
    prompt_lower = prompt.lower()

    # Cost-optimized routing
    if cheap:
        return "deepseek/deepseek-chat"

    # Speed-optimized routing
    if fast:
        return "openai/gpt-4o-mini"

    # Content-based routing
    if any(word in prompt_lower for word in ["twitter", "x.com", "trending", "elon", "musk"]):
        return "xai/grok-3"

    if any(word in prompt_lower for word in ["code", "python", "javascript", "function", "debug"]):
        return "anthropic/claude-sonnet-4"

    if any(word in prompt_lower for word in ["math", "proof", "logic", "reasoning", "solve"]):
        return "openai/o1-mini"

    if any(word in prompt_lower for word in ["long", "document", "summarize", "analyze file"]):
        return "google/gemini-2.0-flash"

    # Default: GPT-4o for general tasks
    return "openai/gpt-4o"


def cmd_chat(
    prompt: str,
    model: Optional[str] = None,
    system: Optional[str] = None,
    cheap: bool = False,
    fast: bool = False,
    max_tokens: int = 1024,
    temperature: Optional[float] = None,
):
    """Execute chat command."""
    if not HAS_SDK:
        branding.print_error(
            "blockrun_llm SDK not installed",
            help_link="https://github.com/blockrunai/blockrun-llm"
        )
        print("  Install with: pip install blockrun-llm")
        return 1

    if not check_environment():
        return 1

    # Determine model
    selected_model = model or get_smart_model(prompt, cheap=cheap, fast=fast)

    try:
        client = LLMClient()

        # Print header
        branding.print_header(
            model=selected_model,
            wallet=client.get_wallet_address(),
        )

        # Execute chat
        response = client.chat(
            model=selected_model,
            prompt=prompt,
            system=system,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Print response
        branding.print_response(response)
        branding.print_footer()

        client.close()
        return 0

    except PaymentError as e:
        branding.print_error(f"Payment failed: {e}", help_link="https://blockrun.ai")
        return 1
    except APIError as e:
        branding.print_error(f"API error: {e}")
        return 1
    except Exception as e:
        branding.print_error(f"Unexpected error: {e}")
        return 1


def cmd_image(
    prompt: str,
    model: Optional[str] = None,
    size: str = "1024x1024",
):
    """Execute image generation command."""
    if not HAS_SDK:
        branding.print_error(
            "blockrun_llm SDK not installed",
            help_link="https://github.com/blockrunai/blockrun-llm"
        )
        print("  Install with: pip install blockrun-llm")
        return 1

    if not check_environment():
        return 1

    selected_model = model or "google/nano-banana"

    try:
        client = ImageClient()

        # Print header
        branding.print_header(
            model=selected_model,
            wallet=client.get_wallet_address(),
        )

        branding.print_info(f"Generating image: \"{prompt[:50]}...\"")
        print()

        # Generate image
        result = client.generate(
            prompt=prompt,
            model=selected_model,
            size=size,
        )

        # Print result
        if result.data:
            image_url = result.data[0].url
            branding.print_success("Image generated!")
            print(f"\n  URL: {image_url}\n")
        else:
            branding.print_error("No image data returned")

        branding.print_footer()
        client.close()
        return 0

    except PaymentError as e:
        branding.print_error(f"Payment failed: {e}", help_link="https://blockrun.ai")
        return 1
    except APIError as e:
        branding.print_error(f"API error: {e}")
        return 1
    except Exception as e:
        branding.print_error(f"Unexpected error: {e}")
        return 1


def cmd_balance():
    """Show wallet balance."""
    if not HAS_SDK:
        branding.print_error(
            "blockrun_llm SDK not installed",
            help_link="https://github.com/blockrunai/blockrun-llm"
        )
        return 1

    if not check_environment():
        return 1

    try:
        client = LLMClient()
        wallet = client.get_wallet_address()

        # Note: Balance query would need to be added to SDK
        # For now, show wallet address
        branding.print_balance(
            wallet=wallet,
            balance="(check at blockrun.ai)",
            network="Base"
        )

        client.close()
        return 0

    except Exception as e:
        branding.print_error(f"Error: {e}")
        return 1


def cmd_models():
    """List available models."""
    if not HAS_SDK:
        branding.print_error(
            "blockrun_llm SDK not installed",
            help_link="https://github.com/blockrunai/blockrun-llm"
        )
        return 1

    if not check_environment():
        return 1

    try:
        client = LLMClient()

        # Fetch models
        models = client.list_models()

        if models:
            branding.print_models_list(models)
        else:
            branding.print_info("No models returned. Check API connection.")

        client.close()
        return 0

    except Exception as e:
        branding.print_error(f"Error: {e}")
        return 1


def cmd_check_update():
    """Check for plugin updates from GitHub."""
    print(f"\n  BlockRun Plugin v{__version__}")
    print("  Checking for updates...\n")

    try:
        req = urllib.request.Request(
            GITHUB_PLUGIN_URL,
            headers={"User-Agent": "BlockRun-Plugin"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            remote_plugin = json.loads(response.read().decode())
            remote_version = remote_plugin.get("version", "unknown")

        if remote_version == __version__:
            branding.print_success(f"You're up to date! (v{__version__})")
        elif remote_version > __version__:
            branding.print_info(f"Update available: v{__version__} → v{remote_version}")
            print("\n  To update, run:")
            print("    /plugin update blockrun\n")
        else:
            branding.print_info(f"Local: v{__version__}, Remote: v{remote_version}")

        return 0

    except urllib.error.URLError as e:
        branding.print_error(f"Could not check for updates: {e.reason}")
        return 1
    except json.JSONDecodeError:
        branding.print_error("Invalid response from GitHub")
        return 1
    except Exception as e:
        branding.print_error(f"Error checking updates: {e}")
        return 1


def cmd_version():
    """Show current version."""
    print(f"BlockRun Plugin v{__version__}")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="blockrun-skill-plus",
        description="BlockRun Skill Plus - Access unlimited LLMs via USDC micropayments",
        epilog="""
Examples:
  %(prog)s "What is quantum computing?"
  %(prog)s "Analyze this code" --model anthropic/claude-sonnet-4
  %(prog)s "A sunset over mountains" --image
  %(prog)s --balance
  %(prog)s --models

More info: https://blockrun.ai
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Positional argument: prompt
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt for chat or image generation",
    )

    # Mode flags
    parser.add_argument(
        "--image", "-i",
        action="store_true",
        help="Generate an image instead of chat",
    )
    parser.add_argument(
        "--balance", "-b",
        action="store_true",
        help="Show wallet balance",
    )
    parser.add_argument(
        "--models", "-m",
        action="store_true",
        help="List available models with pricing",
    )
    parser.add_argument(
        "--check-update",
        action="store_true",
        help="Check for plugin updates from GitHub",
    )
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show plugin version",
    )

    # Chat options
    parser.add_argument(
        "--model",
        help="Specific model ID (e.g., openai/gpt-4o, xai/grok-3)",
    )
    parser.add_argument(
        "--system", "-s",
        help="System prompt for chat",
    )
    parser.add_argument(
        "--cheap",
        action="store_true",
        help="Use most cost-effective model",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use fastest model",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        help="Maximum tokens to generate (default: 1024)",
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        help="Sampling temperature (0.0-2.0)",
    )

    # Image options
    parser.add_argument(
        "--size",
        default="1024x1024",
        help="Image size (default: 1024x1024)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle commands
    if args.version:
        return cmd_version()

    if args.check_update:
        return cmd_check_update()

    if args.balance:
        return cmd_balance()

    if args.models:
        return cmd_models()

    if not args.prompt:
        parser.print_help()
        return 1

    if args.image:
        return cmd_image(
            prompt=args.prompt,
            model=args.model,
            size=args.size,
        )

    return cmd_chat(
        prompt=args.prompt,
        model=args.model,
        system=args.system,
        cheap=args.cheap,
        fast=args.fast,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  Interrupted by user")
        sys.exit(130)
