from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# Create server instance
server = Server("test-server")

# Define a simple tool
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="say_hello",
            description="Says hello with a custom message",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to greet"
                    }
                },
                "required": ["name"]
            }
        )
    ]

# Implement the tool
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "say_hello":
        user_name = arguments.get("name", "World")
        return [TextContent(
            type="text",
            text=f"Hello, {user_name}! This is your MCP server working!"
        )]
    
    raise ValueError(f"Unknown tool: {name}")

# Run the server
if __name__ == "__main__":
    mcp.server.stdio.stdio_server(server)
