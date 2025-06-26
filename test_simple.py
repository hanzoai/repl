#!/usr/bin/env python3
"""Simple test of REPL components."""

import os

print("Testing Hanzo REPL environment...")

# Check for API keys
print("\n1. Checking API keys:")
api_keys = {
    "OpenAI": "OPENAI_API_KEY",
    "Anthropic": "ANTHROPIC_API_KEY", 
    "Groq": "GROQ_API_KEY",
    "Google": "GOOGLE_API_KEY"
}

found_keys = []
for name, env_var in api_keys.items():
    if os.getenv(env_var):
        print(f"   ✓ {name} API key found")
        found_keys.append(name)
    else:
        print(f"   ✗ {name} API key not found")

if not found_keys:
    print("\n⚠️  No API keys found! The REPL will need API keys to function.")
    print("   Set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.")
else:
    print(f"\n✓ Found {len(found_keys)} API key(s)")

print("\n2. REPL is ready to run!")
print("   Run: make dev")
print("   Or:  uv run hanzo-repl")
print("\nCommands:")
print("   ? - Show shortcuts")
print("   Ctrl+K - Open command palette")
print("   /auth - Authenticate with Claude personal account")
print("   /backend - Switch AI backends")
print("   /voice - Enable voice mode")
print("   Ctrl+C - Quit")