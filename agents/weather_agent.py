from llm import ask_llm
from mcp_layer.mcp_client import call_tool
import json

class WeatherAgent:

    def __init__(self, client, tools):

        self.client = client
        self.tools = tools

        self.messages = [
            {
                "role": "system",
                "content": """
Tu es un agent spécialisé dans la météo.

Ta responsabilité est uniquement de traiter les questions
concernant la météo.

Règles :
- Réponds en français.
- Utilise les outils MCP lorsque nécessaire.
- Si la localisation de l'utilisateur est nécessaire,
  utilise get_user_location().
- Après avoir obtenu la latitude et la longitude,
  utilise le tool météo approprié.
- Réponds de manière courte et claire.
- Ne montre jamais ton raisonnement.
"""
            }
        ]

    async def run(self, user_message):

        self.messages.append({
            "role": "user",
            "content": user_message
        })

        while True:

            response = ask_llm(
                messages=self.messages,
                tools=self.tools
            )

            self.messages.append(response)

            if not response.tool_calls:
                return response.content

            for tool_call in response.tool_calls:

                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

             

                result = await call_tool(
                    self.client,
                    tool_name,
                    arguments
                )

                self.messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result)
                })

    async def get_weather_context(self): #pour fournir des informations météo à un autre agent

        result = await call_tool(
            self.client,
            "get_user_location",
            {}
        )

        location = json.loads(
            result.content[0].text
        )

        forecast_result = await call_tool(
            self.client,
            "get_weather_forecast",
            {
                "latitude": location["latitude"],
                "longitude": location["longitude"]
            }
        )

        forecast = json.loads(
            forecast_result.content[0].text
        )

        return {
            "location": location,
            "forecast": forecast
        }