from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

def generate_itinerary_tool(destination, days, context, openai_api_key):
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
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, openai_api_key=openai_api_key)
    itinerary_prompt = prompt_template.format(
        destination=destination,
        days=days,
        lat=context.get("lat", "N/A"),
        lon=context.get("lon", "N/A"),
        temperature=f"{context['weather']['temperature']:.1f}",
        condition=context['weather']['condition']
    )
    return llm.predict(itinerary_prompt)
