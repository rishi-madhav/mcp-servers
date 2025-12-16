#!/usr/bin/env python3
"""
Simplest working MCP server using FastMCP
"""

from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("test-server")

@mcp.tool()
def say_hello(name: str = "World") -> str:
    """
    Say hello to someone.
    
    Args:
        name: Name to greet (default: World)
    
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Your MCP server is working!"

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of the two numbers
    """
    return a + b

# Run the server
if __name__ == "__main__":
    mcp.run()