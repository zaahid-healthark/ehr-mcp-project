# src/agent/mcp_runner.py
import os
import sys
from contextlib import asynccontextmanager
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@asynccontextmanager
async def mcp_session_manager():
    """
    Spawns the FastMCP server as a background subprocess and manages the connection.
    Yields an active MCP ClientSession that can send commands to the server.
    """
    # Define how to start our server
    # We use "-m src.server.fastmcp_app" to run it as a module from the project root
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.server.fastmcp_app"],
        env=os.environ.copy()  # Inherit the virtual environment variables
    )

    # Connect to the server via standard input/output
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the handshake with the MCP server
            await session.initialize()
            yield session