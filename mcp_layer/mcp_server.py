
from mcp.server.mcpserver import MCPServer

from tools.location import get_location
from tools.weather import (
    get_current_weather,
    get_forecast
)


mcp = MCPServer("Weather Server")

@mcp.tool() #means Cette fonction est maintenant disponible comme outil MCP
def get_user_location() -> dict:
    """
    Get the user's approximate location using their IP address.
    """
    return get_location()


@mcp.tool()
def get_weather(latitude: float, longitude: float) -> dict:
    """
    Get the current weather for a geographic location.

    Args:
        latitude: Geographic latitude.
        longitude: Geographic longitude.
    """
    return get_current_weather(latitude, longitude)


@mcp.tool()
def get_weather_forecast(latitude: float, longitude: float) -> list:
    """
    Get tomorrow's weather forecast.

    Args:
        latitude: Geographic latitude.
        longitude: Geographic longitude.
    """
    return get_forecast(latitude, longitude)


if __name__ == "__main__":
    mcp.run()

