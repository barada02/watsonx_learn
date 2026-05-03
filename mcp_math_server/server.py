import os
from mcp.server.fastmcp import FastMCP

# Create a FastMCP server
mcp = FastMCP("Math Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

if __name__ == "__main__":
    # Cloud Run provides the port in the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    # We use SSE transport for a cloud deployment so it can be exposed over HTTP
    mcp.run(transport='sse', host='0.0.0.0', port=port)
