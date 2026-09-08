from llm import ask_llm

from location import get_location
from weather import (
    get_current_weather,
    get_forecast
)


tools = [
    get_location,
    get_current_weather,
    get_forecast
]


available_functions = {
    "get_location": get_location,
    "get_current_weather": get_current_weather,
    "get_forecast": get_forecast
}


messages = [
    {
        "role": "system",
        "content": """
Tu es un assistant météo.

Règles :
- Réponds en français et de manière courte.
- Utilise les outils météo lorsque la question nécessite des informations météo.
- Si la localisation de l'utilisateur est nécessaire et inconnue, utilise automatiquement get_location().
- Ne demande pas à l'utilisateur sa ville si get_location() peut obtenir sa localisation.
- Après avoir obtenu la latitude et la longitude, utilise le tool météo approprié.
- Pour une question qui ne concerne pas la météo, réponds directement sans utiliser les tools.
- Ne montre jamais ton raisonnement.
"""
    }
]


def run_agent(user_message):

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

        # Si aucun tool n'est demandé → réponse finale
        if not response.tool_calls:
            return response.content

        # Si le LLM demande un ou plusieurs tools
        for tool_call in response.tool_calls:

            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            function_to_call = available_functions.get(
                function_name
            )

            if function_to_call:

                # Exécution du tool
                result = function_to_call(**arguments)

                # Résultat envoyé au LLM
                messages.append({
                    "role": "tool",
                    "tool_name": function_name,
                    "content": str(result)
                })


def main():

    print("\n🌤️ Weather AI Agent - V2")
    print("Tape 'exit' pour quitter.\n")

    while True:

        user_message = input("👤 Vous : ")

        if user_message.lower() == "exit":
            break

        response = run_agent(user_message)

        print(f"\n🤖 Agent : {response}\n")


if __name__ == "__main__":
    main()

