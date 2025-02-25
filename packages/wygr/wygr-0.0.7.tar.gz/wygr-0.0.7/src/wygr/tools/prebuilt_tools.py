from wygr.tools.base_tool import Tool
from pydantic import BaseModel, Field
from wygr.tools.base_tool import add_function, Tool

#for travel planner agent
def get_location_info():
    try:
        import requests
    except ImportError as e:
        raise ImportError(f"Required library for get_location_info is not installed: {e}. Please install it using `pip install requests`.")
    from wygr.tools.raw_functions import get_location_info_tool as rf
    decorated_model = add_function(rf)(GetLocationInfo)
    tool = Tool(decorated_model)()
    return tool

class GetLocationInfo(BaseModel):
    """This tool gathers information about a given location using geolocation and weather APIs."""
    location: str = Field(description="Name of the location to retrieve information for")
    geolocation_api_key: str = Field(description="API key for the geolocation service")
    weather_api_key: str = Field(description="API key for the weather service")
