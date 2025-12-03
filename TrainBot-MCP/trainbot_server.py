"""
TrainBot MCP Server
An AI-powered training course generation tool built with FastMCP.

This server provides tools for generating educational content like flashcards.
"""

from fastmcp import FastMCP

# Initialize the FastMCP server
# The server name will be displayed to clients connecting to this MCP server
mcp = FastMCP("TrainBot")


# Define a tool using the @mcp.tool() decorator
# Tools are functions that can be called by MCP clients (like Claude Desktop)
@mcp.tool()
def generate_flashcards(topic: str, count: int = 10) -> str:
    """
    Generate flashcards for a given topic.

    This tool creates educational flashcards to help learners study a topic.

    Parameters:
    -----------
    topic : str
        The subject or topic for which to generate flashcards.
        Example: "Python programming", "World War II", "Photosynthesis"

    count : int, optional
        The number of flashcards to generate (default: 10).
        Must be a positive integer.

    Returns:
    --------
    str
        A formatted string containing the generated flashcards.
        (Currently returns a placeholder - real logic will be added later)
    """
    # Validate the count parameter
    if count <= 0:
        return "Error: count must be a positive integer"

    # Placeholder response - you'll add real AI logic here later
    # This could integrate with OpenAI, Anthropic, or other AI APIs
    return f"Generated {count} flashcards for topic: {topic}\n\n[Flashcard generation logic will be implemented here]"


# Entry point for running the server
# When this script is run directly (not imported), start the MCP server
if __name__ == "__main__":
    # Run the server
    # FastMCP handles all the MCP protocol communication automatically
    mcp.run()
