import anyio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters


# Racine du projet weather-ai-agent
PROJECT_ROOT = Path(__file__).resolve().parent.parent

server = StdioServerParameters(
    command=sys.executable,
    args=["-m", "mcp_layer.mcp_server"],
    cwd=str(PROJECT_ROOT),
)

async def create_client():
    """
    Create and connect an MCP client to the MCP server.
    """

    client = Client(server)

    await client.__aenter__()

    return client


async def close_client(client):
    """
    Close the MCP client connection.
    """

    await client.__aexit__(None, None, None)


async def get_tools(client):
    """
    Get the tools available on the MCP server
    and convert them to Ollama format.
    """

    result = await client.list_tools()

    tools = []

    for tool in result.tools:

        tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema
            }
        })

    return tools


async def call_tool(client, tool_name, arguments):
    """
    Call a tool through the MCP server.
    """

    result = await client.call_tool(
        tool_name,
        arguments
    )

    return result


