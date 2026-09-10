from llm import ask_llm


class RecommendationAgent:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": """
Tu es un agent spécialisé dans les recommandations.

Ta responsabilité est d'analyser les informations
qui te sont fournies et de donner une recommandation
utile à l'utilisateur.

Règles :
- Réponds en français.
- Sois court et clair.
- Base ta recommandation uniquement sur les informations
  fournies.
- Ne prétends pas avoir accès à des informations que tu
  n'as pas reçues.
- Ne montre jamais ton raisonnement.
"""
            }
        ]

    async def run(self, context):

        prompt = f"""
    Question de l'utilisateur :

    {context.user_request}

    Informations disponibles :

    Localisation :
    {context.location}

    Météo :
    {context.weather}

    Donne une recommandation adaptée à la question.
    """

        messages = self.messages + [
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = ask_llm(
            messages=messages
        )

        context.recommendation = response.content

        return response.content