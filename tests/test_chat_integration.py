"""Test chat integration with MCP tools."""

import asyncio
import json
import os
import tempfile
from pathlib import Path

import pytest
from hanzo_mcp.server import HanzoMCPServer
from hanzo_repl.llm_client import LLMClient
from hanzo_repl.tool_executor import ToolExecutor


@pytest.fixture
async def mcp_server():
    """Create MCP server instance."""
    server = HanzoMCPServer()
    await server.initialize()
    return server


@pytest.fixture
def llm_client():
    """Create LLM client instance."""
    client = LLMClient()
    if not client.get_available_providers():
        pytest.skip("No LLM providers available")
    return client


@pytest.fixture
def tool_executor(mcp_server, llm_client):
    """Create tool executor instance."""
    return ToolExecutor(mcp_server, llm_client)


@pytest.mark.asyncio
async def test_chat_simple_question(tool_executor):
    """Test simple chat without tool usage."""
    response = await tool_executor.execute_with_tools("What is the capital of France?")
    assert response
    assert "paris" in response.lower()


@pytest.mark.asyncio
async def test_chat_with_file_creation(tool_executor):
    """Test chat that creates a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_chat.txt"
        
        response = await tool_executor.execute_with_tools(
            f"Create a file at {test_file} with the content 'Hello from chat test'"
        )
        
        assert response
        assert test_file.exists()
        assert test_file.read_text().strip() == "Hello from chat test"


@pytest.mark.asyncio
async def test_chat_with_file_reading(tool_executor):
    """Test chat that reads a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "read_test.txt"
        test_file.write_text("Secret content: 42")
        
        response = await tool_executor.execute_with_tools(
            f"What is the secret content in the file {test_file}?"
        )
        
        assert response
        assert "42" in response


@pytest.mark.asyncio
async def test_chat_with_code_search(tool_executor):
    """Test chat that searches for code."""
    response = await tool_executor.execute_with_tools(
        "Find Python files in the current directory that contain the word 'test'"
    )
    
    assert response
    # Should find this test file at minimum
    assert "test" in response.lower()


@pytest.mark.asyncio
async def test_chat_with_shell_command(tool_executor):
    """Test chat that runs shell commands."""
    response = await tool_executor.execute_with_tools(
        "Run the command 'echo Hello World' and tell me what it outputs"
    )
    
    assert response
    assert "hello world" in response.lower()


@pytest.mark.asyncio
async def test_chat_multi_tool_workflow(tool_executor):
    """Test chat that uses multiple tools in sequence."""
    with tempfile.TemporaryDirectory() as tmpdir:
        response = await tool_executor.execute_with_tools(
            f"Create a Python file at {tmpdir}/hello.py that prints 'Hello, World!', "
            f"then run it and tell me the output"
        )
        
        assert response
        assert "hello" in response.lower()
        assert Path(f"{tmpdir}/hello.py").exists()


@pytest.mark.asyncio
async def test_chat_error_handling(tool_executor):
    """Test chat handles tool errors gracefully."""
    response = await tool_executor.execute_with_tools(
        "Try to read a file that doesn't exist: /nonexistent/file.txt"
    )
    
    assert response
    # Should handle the error and explain it
    assert "not found" in response.lower() or "doesn't exist" in response.lower()


@pytest.mark.asyncio
async def test_chat_context_persistence(tool_executor):
    """Test chat maintains context across messages."""
    # First message
    response1 = await tool_executor.execute_with_tools(
        "Remember this number: 12345"
    )
    assert response1
    
    # Second message referring to first
    response2 = await tool_executor.execute_with_tools(
        "What was the number I asked you to remember?"
    )
    assert response2
    assert "12345" in response2


@pytest.mark.asyncio
async def test_chat_with_agent_delegation(tool_executor):
    """Test chat that delegates to an agent."""
    response = await tool_executor.execute_with_tools(
        "Use an agent to find all Python files in the current directory"
    )
    
    assert response
    # Should complete the task
    assert ".py" in response