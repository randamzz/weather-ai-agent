from llm import ask_llm


class Orchestrator:

    def __init__(self, weather_agent):

        self.weather_agent = weather_agent

        self.messages = [
            {
                "role": "system",
                "content": """
Tu es un orchestrateur d'agents.

Ton rôle est de déterminer quel agent doit traiter
la demande de l'utilisateur.

Agents disponibles :

- weather : pour les questions concernant la météo,
  température, pluie, vent, soleil, prévisions,
  picnic, vêtements selon la météo, etc.

- general : pour les questions qui ne concernent pas
  la météo.

Réponds UNIQUEMENT avec :
weather
ou
general

Ne donne aucune autre réponse.
"""
            }
        ]

    async def run(self, user_message):

        route = self.route(user_message)

        if route == "weather":

            return await self.weather_agent.run(
                user_message
            )

        return self.answer_general(user_message)

    def route(self, user_message):

        messages = self.messages + [
            {
                "role": "user",
                "content": user_message
            }
        ]

        response = ask_llm(
            messages=messages
        )

        route = response.content.strip().lower()

        if "weather" in route:
            return "weather"

        return "general"

    def answer_general(self, user_message):

        messages = [
            {
                "role": "system",
                "content": """
Tu es un assistant général.

Réponds en français, de manière courte et claire.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        response = ask_llm(
            messages=messages
        )

        return response.content