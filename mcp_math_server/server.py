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
    # We use SSE transport for a cloud deployment so it can be exposed over HTTP
    mcp.run(transport='sse', host='0.0.0.0', port=8000)
