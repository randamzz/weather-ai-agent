#v3.1 start (test comm ente server et client)
# import anyio

# from mcp import Client, StdioServerParameters


# server = StdioServerParameters(
#     command="python",
#     args=["mcp_server.py"]
# )


# async def main():

#     async with Client(server) as client:

#         print("\n✅ Connected to MCP Server\n")

#         result = await client.list_tools()

#         print("🛠️ Available tools:")

#         for tool in result.tools:
#             print(f"- {tool.name}")

#         result = await client.call_tool(
#             "get_user_location",
#             {}
#         )

#         print("\n📍 Tool result:")
#         print(result)


# if __name__ == "__main__":
#     anyio.run(main)

#v3.1 end

#V3 start
import anyio

from mcp import Client, StdioServerParameters


server = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
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

#V3 end

