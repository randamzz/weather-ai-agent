
import anyio

from llm import ask_llm
from mcp_client import (
    create_client,
    close_client,
    get_tools,
    call_tool
)


messages = [
    {
        "role": "system",
        "content": """
Tu es un assistant météo.

Règles :
- Réponds en français et de manière courte.
- Utilise les outils météo lorsque la question nécessite des informations météo.
- Si la localisation de l'utilisateur est nécessaire et inconnue,
  utilise automatiquement get_user_location().
- Ne demande pas à l'utilisateur sa ville si get_user_location()
  peut obtenir sa localisation.
- Après avoir obtenu la latitude et la longitude,
  utilise le tool météo approprié.
- Pour une question qui ne concerne pas la météo,
  réponds directement sans utiliser les tools.
- Ne montre jamais ton raisonnement.
"""
    }
]


async def run_agent(user_message, client, tools):

    messages.append({
        "role": "user",
        "content": user_message
    })

    while True:

        # LLM
        response = ask_llm(
            messages=messages,
            tools=tools
        )

        messages.append(response)

        # Si aucun tool n'est demandé
        if not response.tool_calls:
            return response.content

        # Si le LLM demande un ou plusieurs tools
        for tool_call in response.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            # Appel du tool via MCP
            result = await call_tool(
                client,
                tool_name,
                arguments
            )

            # Résultat envoyé au LLM
            messages.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": str(result)
            })


async def main():

    print("\n🌤️ Weather AI Agent - V3")
    print("Tape 'exit' pour quitter.\n")

    # Connexion au MCP Server
    client = await create_client()

    print("✅ Connected to MCP Server")

    # Découverte des tools
    tools = await get_tools(client)


    try:

        while True:

            user_message = input("\n👤 Vous : ")

            if user_message.lower() == "exit":
                break

            response = await run_agent(
                user_message,
                client,
                tools
            )

            print(f"\n🤖 Agent : {response}")

    finally:

        await close_client(client)


if __name__ == "__main__":
    anyio.run(main)
