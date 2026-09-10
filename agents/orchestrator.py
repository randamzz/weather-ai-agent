import json

from llm import ask_llm
from context.agent_context import AgentContext


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
  pour les questions générales.

Tu dois également déterminer si des informations
météorologiques sont nécessaires.

Réponds UNIQUEMENT avec un objet JSON valide :

{
    "route": "weather | recommendation | general",
    "needs_weather": true | false
}

Ne donne aucune explication.
"""
            }
        ]

    async def run(self, user_message):

        context = AgentContext(
            user_request=user_message
        )

        decision = self.decide(user_message)

        route = decision["route"]
        needs_weather = decision["needs_weather"]


        if route == "weather":

            return await self.weather_agent.run(
                user_message
            )

        if route == "recommendation":

            if needs_weather:


                await self.weather_agent.update_context(
                    context
                )

            await self.recommendation_agent.run(
                context
            )

            return context.recommendation

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