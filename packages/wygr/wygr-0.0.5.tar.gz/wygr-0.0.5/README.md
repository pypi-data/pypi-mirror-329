# trip Travelplanner app

This is a Travel Planner App built with Streamlit that generates personalized travel itineraries based on user input. The app takes a user's travel request (destination and duration) and provides detailed information, including weather data, itinerary recommendations, accommodations, local attractions, and more.

<br>
Example Usage
Here’s an example of how you can use the Travel Planner agent in your own code:
<br>

```
from trip_travel_planner import TravelPlannerAgent

openai_api_key = "your_openai_api_key"
weather_api_key = "your_weather_api_key"
geolocation_api_key = "your_geolocation_api_key"

planner = TravelPlannerAgent(weather_api_key, geolocation_api_key, openai_api_key)
prompt = "travel plan to Paris for 5 days"
travel_plan = planner.generate_travel_plan(prompt)

print(travel_plan)

```
