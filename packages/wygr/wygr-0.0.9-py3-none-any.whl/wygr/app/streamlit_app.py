import streamlit as st
from wygr.agents.travel_planner import main_agent
from utils.helpers import parse_user_input
from tools.prebuilt_tools import get_location_info_tool
from tools.ititnerary_tools import generate_itinerary_tool
import os

# Load environment variables
weather_api_key = os.getenv("WEATHER_API_KEY")
geolocation_api_key = os.getenv("GEOLOCATION_API_KEY")
openai_api_key = os.getenv("OPEN_API_KEY")

st.title("Travel Itinerary Planner")
user_prompt = st.text_input("Enter your travel request (e.g., 'travel plan to Paris for 5 days.')")

if user_prompt:
    destination, days = parse_user_input(user_prompt)

    if destination:
        st.write(f"### Travel Plan for {destination}")
        location_info = get_location_info_tool(destination, geolocation_api_key, weather_api_key)
        if isinstance(location_info, str):
            st.error(location_info)
        else:
            context = {
                "lat": location_info["lat"],
                "lon": location_info["lon"],
                "weather": location_info["weather"]
            }
            itinerary = generate_itinerary_tool(destination, days, context, openai_api_key)
            st.markdown(itinerary)
    else:
        st.error("Error: Invalid input format. Please provide a destination and optional duration.")
