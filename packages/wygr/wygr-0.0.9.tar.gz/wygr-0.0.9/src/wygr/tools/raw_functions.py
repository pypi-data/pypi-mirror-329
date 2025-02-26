from opencage.geocoder import OpenCageGeocode
import requests

def fetch_lat_long(location, geolocation_api_key):
    """Fetch latitude and longitude for a location using OpenCage API."""
    geocoder = OpenCageGeocode(geolocation_api_key)
    results = geocoder.geocode(location)
    if results:
        lat = results[0]['geometry']['lat']
        lon = results[0]['geometry']['lng']
        return lat, lon
    return None, None

def fetch_weather(lat, lon, weather_api_key):
    """Fetch weather information for given latitude and longitude."""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return {
                "temperature": weather_data["main"]["temp"] - 273.15,  # Kelvin to Celsius
                "condition": weather_data["weather"][0]["description"].capitalize(),
            }
        return {"temperature": "N/A", "condition": "Weather data unavailable"}
    except requests.RequestException as e:
        return {"temperature": "N/A", "condition": f"Network error: {str(e)}"}

def get_location_info_tool(location, geolocation_api_key, weather_api_key):
    """Tool to gather information about a location."""
    lat, lon = fetch_lat_long(location, geolocation_api_key)
    if lat is None or lon is None:
        return f"Error: Unable to retrieve location coordinates for {location}."
    weather = fetch_weather(lat, lon, weather_api_key)
    return {"lat": lat, "lon": lon, "weather": weather}
