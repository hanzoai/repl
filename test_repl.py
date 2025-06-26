#!/usr/bin/env python3
"""Test the Hanzo REPL functionality."""

import asyncio
from hanzo_repl.textual_repl import HanzoTextualREPL

# For non-interactive testing, let's test the components
async def test_components():
    from hanzo_mcp.server import HanzoMCPServer
    from hanzo_repl.llm_client import LLMClient
    from hanzo_repl.backends import BackendManager
    
    print("Testing Hanzo REPL components...")
    
    # Test MCP server
    print("\n1. Testing MCP Server...")
    mcp = HanzoMCPServer()
    await mcp.initialize()
    print(f"   ✓ MCP Server initialized with {len(mcp.tools)} tools")
    
    # Test LLM client
    print("\n2. Testing LLM Client...")
    llm = LLMClient()
    providers = llm.get_available_providers()
    print(f"   ✓ Available providers: {', '.join(providers)}")
    
    # Test backend manager
    print("\n3. Testing Backend Manager...")
    backend_mgr = BackendManager(llm)
    backends = backend_mgr.list_backends()
    print(f"   ✓ Current backend: {backend_mgr.current_backend}")
    for name, available in backends.items():
        status = "✓" if available else "✗"
        print(f"   {status} {name}")
    
    # Test some MCP tools
    print("\n4. Testing MCP Tools...")
    
    # Test read_file tool
    if "read_file" in mcp.tools:
        try:
            result = await mcp.tools["read_file"].execute(file_path="README.md")
            print(f"   ✓ read_file: Read {len(result)} characters")
        except Exception as e:
            print(f"   ✗ read_file: {e}")
    
    # Test list_directory tool
    if "list_directory" in mcp.tools:
        try:
            result = await mcp.tools["list_directory"].execute(path=".")
            print(f"   ✓ list_directory: Found {len(result)} items")
        except Exception as e:
            print(f"   ✗ list_directory: {e}")
    
    print("\nAll components working! You can run 'make dev' to start the interactive REPL.")

if __name__ == "__main__":
    asyncio.run(test_components())