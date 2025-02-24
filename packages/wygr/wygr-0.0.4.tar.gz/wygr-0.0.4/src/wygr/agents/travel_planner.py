'''
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from tools.prebuilt_tools import get_location_info_tool
from tools.ititnerary_tools import generate_itinerary_tool

def main_agent(weather_api_key, geolocation_api_key, openai_api_key):
    if not openai_api_key:
        raise ValueError("OpenAI API key is missing! Please set it in secrets or as an environment variable.")
    
    tools = [
        Tool(
            name="GetLocationInfo",
            func=lambda location: get_location_info_tool(location, geolocation_api_key, weather_api_key),
            description="Fetch location coordinates and weather information. Input: location name."
        ),
        Tool(
            name="GenerateItinerary",
            func=lambda input: generate_itinerary_tool(
                input['destination'], 
                input['days'], 
                input['context'],
                openai_api_key
            ),
            description="Generate a travel itinerary. Input: destination, days, and location context."
        )
    ]

    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=OpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.5),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent


#medical agent


class Agent:
    def __init__(self, medical_report=None, role=None, extra_info=None):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info or {}  # Ensure extra_info is always a dictionary
        # Initialize the prompt based on role and other info
        self.prompt_template = self.create_prompt_template()
        # Initialize the model
        self.model = ChatOpenAI(temperature=0, model="gpt-4o")

    def create_prompt_template(self):
        templates = {
            "MultidisciplinaryTeam": """
                Act like a multidisciplinary team of healthcare professionals.
                You will receive a medical report of a patient visited by a Cardiologist, Psychologist, and Pulmonologist.
                Task: Review the patient's medical report from the Cardiologist, Psychologist, and Pulmonologist, analyze them and come up with a list of 3 possible health issues of the patient.
                Just return a list of bullet points of 3 possible health issues of the patient and for each issue provide the reason.
                
                Cardiologist Report: {cardiologist_report}
                Psychologist Report: {psychologist_report}
                Pulmonologist Report: {pulmonologist_report}
            """,
            "Cardiologist": """
                Act like a cardiologist. You will receive a medical report of a patient.
                Task: Review the patient's cardiac workup, including ECG, blood tests, Holter monitor results, and echocardiogram.
                Focus: Determine if there are any subtle signs of cardiac issues that could explain the patient’s symptoms. Rule out any underlying heart conditions, such as arrhythmias or structural abnormalities, that might be missed on routine testing.
                Recommendation: Provide guidance on any further cardiac testing or monitoring needed to ensure there are no hidden heart-related concerns. Suggest potential management strategies if a cardiac issue is identified.
                Please only return the possible causes of the patient's symptoms and the recommended next steps.
                Medical Report: {medical_report}
            """,
            "Psychologist": """
                Act like a psychologist. You will receive a patient's report.
                Task: Review the patient's report and provide a psychological assessment.
                Focus: Identify any potential mental health issues, such as anxiety, depression, or trauma, that may be affecting the patient's well-being.
                Recommendation: Offer guidance on how to address these mental health concerns, including therapy, counseling, or other interventions.
                Please only return the possible mental health issues and the recommended next steps.
                Patient's Report: {medical_report}
            """,
            "Pulmonologist": """
                Act like a pulmonologist. You will receive a patient's report.
                Task: Review the patient's report and provide a pulmonary assessment.
                Focus: Identify any potential respiratory issues, such as asthma, COPD, or lung infections, that may be affecting the patient's breathing.
                Recommendation: Offer guidance on how to address these respiratory concerns, including pulmonary function tests, imaging studies, or other interventions.
                Please only return the possible respiratory issues and the recommended next steps.
                Patient's Report: {medical_report}
            """
        }

        if self.role not in templates:
            raise ValueError(f"Invalid role: {self.role}")

        return PromptTemplate.from_template(templates[self.role])

    def run(self):
        print(f"{self.role} is running...")
        try:
            if self.role == "MultidisciplinaryTeam":
                prompt = self.prompt_template.format(**self.extra_info)
            else:
                prompt = self.prompt_template.format(medical_report=self.medical_report)

            response = self.model.invoke(prompt)
            return response.content
        except Exception as e:
            print("Error occurred:", e)
            return None

# Define specialized agent classes
class Cardiologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Cardiologist")

class Psychologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Psychologist")

class Pulmonologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Pulmonologist")

class MultidisciplinaryTeam(Agent):
    def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report):
        extra_info = {
            "cardiologist_report": cardiologist_report,
            "psychologist_report": psychologist_report,
            "pulmonologist_report": pulmonologist_report
        }
        super().__init__(role="MultidisciplinaryTeam", extra_info=extra_info)
'''


import os
from dotenv import load_dotenv
import re
import requests
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.prompts import PromptTemplate
#from wygr.models.openai import ChatOpenAI
from opencage.geocoder import OpenCageGeocode


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

        return {
            "temperature": "N/A",
            "condition": "Weather data unavailable",
        }

    except requests.RequestException as e:
        return {
            "temperature": "N/A",
            "condition": f"Network error: {str(e)}",
        }

def parse_user_input(prompt):
    """Parse the user's input for destination and duration."""
    match = re.search(r'travel plan to (\w+)(?: for (\d+) days)?', prompt, re.IGNORECASE)

    if match:
        destination = match.group(1)
        days = int(match.group(2)) if match.group(2) else 3
        return destination, days

    return None, None

def get_location_info_tool(location: str, geolocation_api_key: str, weather_api_key: str):
    """Tool to gather information about a location."""
    lat, lon = fetch_lat_long(location, geolocation_api_key)
    if lat is None or lon is None:
        return f"Error: Unable to retrieve location coordinates for {location}."

    weather = fetch_weather(lat, lon, weather_api_key)

    return {
        "lat": lat,
        "lon": lon,
        "weather": weather,
    }

def generate_itinerary_tool(destination: str, days: int, context: dict,llm: ChatOpenAI):
    """Tool to generate a detailed travel itinerary."""
    prompt_template = PromptTemplate.from_template(
        "Create a comprehensive travel itinerary for {destination} over {days} days.\n\n"
        "Destination Details:\n"
        "- Location: {destination}\n"
        "- Duration: {days} days\n"
        "- Latitude: {lat}\n"
        "- Longitude: {lon}\n"
        "- Temperature: {temperature}°C\n"
        "- Weather Condition: {condition}\n\n"
        "Itinerary Guidelines:\n"
        "1. Provide a description of {destination}\n"
        "2. Create a day-by-day plan\n"
        "3. Suggest attractions, food, and travel tips\n"
        "4. Adapt to weather conditions\n\n"
        "Format your response in clear markdown."
    )

   # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, openai_api_key=openai_api_key)

    itinerary_prompt = prompt_template.format(
        destination=destination,
        days=days,
        lat=context.get("lat", "N/A"),
        lon=context.get("lon", "N/A"),
        temperature=f"{context['weather']['temperature']:.1f}",
        condition=context['weather']['condition']
    )

    return llm.predict(itinerary_prompt)