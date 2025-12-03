# TrainBot MCP Server

An AI-powered training course generation tool built with FastMCP.

## What is This?

TrainBot is an MCP (Model Context Protocol) server that provides AI-powered educational content generation tools. Currently, it includes a flashcard generation tool, with more training features to come.

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or if using pyproject.toml:

```bash
pip install -e .
```

### 2. Run the server (for testing)

```bash
python trainbot_server.py
```

## Using with Claude Desktop

To use this MCP server with Claude Desktop, add it to your Claude configuration:

### macOS Configuration

Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "trainbot": {
      "command": "python",
      "args": [
        "/Users/rishimadhav/Desktop/Github/mcp-servers/TrainBot-MCP/trainbot_server.py"
      ]
    }
  }
}
```

### Windows Configuration

Edit: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "trainbot": {
      "command": "python",
      "args": [
        "C:\\path\\to\\trainbot_server.py"
      ]
    }
  }
}
```

After updating the config, restart Claude Desktop.

## Available Tools

### `generate_flashcards`

Generate flashcards for a given topic.

**Parameters:**
- `topic` (string, required): The subject or topic for flashcards
- `count` (integer, optional): Number of flashcards to generate (default: 10)

**Example usage in Claude:**
```
Can you generate 5 flashcards about Python functions?
```

## Project Structure

```
TrainBot-MCP/
├── trainbot_server.py      # Main MCP server file
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Direct dependencies
└── TRAINBOT_README.md      # This file
```

## Understanding FastMCP

### How Tools Work

1. **Decorator Pattern**: Tools are defined using `@mcp.tool()` decorator
2. **Type Hints**: Python type hints define parameter types (str, int, etc.)
3. **Docstrings**: Function docstrings become tool descriptions in MCP
4. **Parameters**: Function parameters become tool parameters automatically

### Example Tool Anatomy

```python
@mcp.tool()  # Decorator registers this function as an MCP tool
def generate_flashcards(topic: str, count: int = 10) -> str:
    """Tool description shown to AI"""  # This becomes the tool description
    # Function body contains the logic
    return "result"
```

## Next Steps

- Add real AI logic to generate_flashcards (integrate with OpenAI/Anthropic APIs)
- Add more tools (generate_quiz, create_study_guide, etc.)
- Add error handling and validation
- Add tests

## Development

To add new tools, simply add new functions with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def your_new_tool(param1: str, param2: int = 5) -> str:
    """Description of what your tool does"""
    # Your logic here
    return "result"
```

FastMCP automatically handles:
- MCP protocol communication
- Parameter validation
- Tool discovery
- Error handling (basic)
