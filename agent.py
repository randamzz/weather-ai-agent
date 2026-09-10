import anyio

from agents.weather_agent import WeatherAgent

from mcp_layer.mcp_client import (
    create_client,
    close_client,
    get_tools
)


async def main():

    print("\n🌤️ Weather AI Agent - V4")
    print("Tape 'exit' pour quitter.\n")

    # Connexion au MCP Server
    client = await create_client()

    print("✅ Connected to MCP Server")

    # Découverte des tools MCP
    tools = await get_tools(client)

    print("🛠️ Available tools:")

    for tool in tools:
        print(f"- {tool['function']['name']}")

    # Création du Weather Agent
    weather_agent = WeatherAgent(
        client=client,
        tools=tools
    )

    try:

        while True:

            user_message = input("\n👤 Vous : ")

            if user_message.lower() == "exit":
                break

            response = await weather_agent.run(
                user_message
            )

            print(f"\n🤖 Weather Agent : {response}")

    finally:

        await close_client(client)


if __name__ == "__main__":
    anyio.run(main)