import anyio

from agents.weather_agent import WeatherAgent
from agents.orchestrator import Orchestrator
from agents.recommendation_agent import RecommendationAgent

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

    # Création du Weather Agent
    weather_agent = WeatherAgent(
        client=client,
        tools=tools
    )
    recommendation_agent = RecommendationAgent()
    # Création de l'Orchestrator
    orchestrator = Orchestrator(
        weather_agent=weather_agent,
        recommendation_agent=recommendation_agent
    )

    try:

        while True:

            user_message = input("\n👤 Vous : ")

            if user_message.lower() == "exit":
                break

            response = await orchestrator.run(
                user_message
            )

            print(f"\n🤖 Agent : {response}")

    finally:

        await close_client(client)


if __name__ == "__main__":
    anyio.run(main)