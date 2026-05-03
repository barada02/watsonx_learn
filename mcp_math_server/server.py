import os
from mcp.server.fastmcp import FastMCP

# Cloud Run provides the port in the PORT environment variable
port = int(os.environ.get("PORT", 8080))

# Create a FastMCP server
mcp = FastMCP("Math Server", host="0.0.0.0", port=port)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

@mcp.tool()
def get_personal_information() -> dict:
    """Get personal information in JSON formatting."""
    return {
        "name": "chandan",
        "age": 28,
        "email": "chandan@example.com",
        "role": "Cloud Architect",
        "location": "Earth"
    }

if __name__ == "__main__":
    # We use SSE transport for a cloud deployment so it can be exposed over HTTP
    mcp.run(transport='sse')
