import json

from llm import ask_llm


class Orchestrator:

    def __init__(
        self,
        weather_agent,
        recommendation_agent
    ):

        self.weather_agent = weather_agent
        self.recommendation_agent = recommendation_agent

        self.messages = [
            {
                "role": "system",
                "content": """
Tu es un orchestrateur d'agents.

Ton rôle est d'analyser la demande de l'utilisateur
et de déterminer comment elle doit être traitée.

Agents disponibles :

- weather :
  pour les questions qui demandent des informations
  météorologiques.

- recommendation :
  pour les demandes de conseil ou de recommandation.

- general :
  pour les questions générales qui ne nécessitent
  ni météo ni recommandation.

Tu dois également déterminer si des informations
météorologiques sont nécessaires pour répondre
correctement à la demande.

Réponds UNIQUEMENT avec un objet JSON valide
respectant exactement ce format :

{
    "route": "weather | recommendation | general",
    "needs_weather": true | false
}

Exemples :

Question :
"Quelle sera la température demain ?"

Réponse :
{
    "route": "weather",
    "needs_weather": true
}

Question :
"Est-ce que je peux faire un picnic demain ?"

Réponse :
{
    "route": "recommendation",
    "needs_weather": true
}

Question :
"Que me conseilles-tu pour une journée chaude ?"

Réponse :
{
    "route": "recommendation",
    "needs_weather": false
}

Question :
"C'est quoi une API ?"

Réponse :
{
    "route": "general",
    "needs_weather": false
}

Ne donne aucune explication.
"""
            }
        ]

    async def run(self, user_message):

        decision = self.decide(user_message)

        route = decision["route"]
        needs_weather = decision["needs_weather"]

        # -------------------------
        # WEATHER
        # -------------------------

        if route == "weather":

            return await self.weather_agent.run(
                user_message
            )

        # -------------------------
        # RECOMMENDATION
        # -------------------------

        if route == "recommendation":

            context = "Aucune information météo nécessaire."

            if needs_weather:


                context = (
                    await self.weather_agent
                    .get_weather_context()
                )

            return await self.recommendation_agent.run(
                user_message,
                context
            )

        # -------------------------
        # GENERAL
        # -------------------------

        return self.answer_general(user_message)

    def decide(self, user_message):

        messages = self.messages + [
            {
                "role": "user",
                "content": user_message
            }
        ]

        response = ask_llm(
            messages=messages
        )

        content = response.content.strip()

        try:

            decision = json.loads(content)

            return decision

        except json.JSONDecodeError:

            print(
                "\n⚠️ Orchestrator : "
                "réponse JSON invalide"
            )

            return {
                "route": "general",
                "needs_weather": False
            }

    def answer_general(self, user_message):

        messages = [
            {
                "role": "system",
                "content": """
Tu es un assistant général.

Réponds en français,
de manière courte et claire.
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