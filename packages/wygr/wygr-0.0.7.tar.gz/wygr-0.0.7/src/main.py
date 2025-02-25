

import os
import time
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from wygr.agents.teaching_agent import teaching_agent_fun
from wygr.tools.generating_syllabus import generate_syllabus

# import your OpenAI key (put in your .env file)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.5, openai_api_key=openai_api_key)
teaching_agent=teaching_agent_fun(llm)

with gr.Blocks() as demo:
    gr.Markdown("# Your AI Instructor")
    with gr.Tab("Input Your Information"):

        def perform_task(input_text):
            # Perform the desired task based on the user input
            task = (
                "Generate a course syllabus to teach the topic: " + input_text
            )
            syllabus = generate_syllabus(llm, input_text, task)
            teaching_agent.seed_agent(syllabus, task)
            return syllabus

        text_input = gr.Textbox(
            label="State the name of topic you want to learn:"
        )
        text_output = gr.Textbox(label="Your syllabus will be showed here:")
        text_button = gr.Button("Build the Bot!!!")
        text_button.click(perform_task, text_input, text_output)
    with gr.Tab("AI Instructor"):
        #       inputbox = gr.Textbox("Input your text to build a Q&A Bot here.....")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="What do you concern about?")
        clear = gr.Button("Clear")

        def user(user_message, history):
            teaching_agent.human_step(user_message)
            return "", history + [[user_message, None]]

        def bot(history):
            bot_message = teaching_agent.instructor_step()
            history[-1][1] = ""
            for character in bot_message:
                history[-1][1] += character
                time.sleep(0.05)
                yield history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
demo.queue().launch(debug=True, share=True)





# AI MEDICAL WYGR AGENT ------------------------------------------------------------------------

'''
from wygr.agents.medical_agent import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='.env')

with open("src\Medical Reports\Medical Rerort - Michael Johnson - Panic Attack Disorder.txt", "r") as file:
    medical_report = file.read()


agents = {
    "Cardiologist": Cardiologist(medical_report),
    "Psychologist": Psychologist(medical_report),
    "Pulmonologist": Pulmonologist(medical_report)
}

# Function to run each agent and get their response
def get_response(agent_name, agent):
    response = agent.run()
    return agent_name, response

# Run the agents concurrently and collect responses
responses = {}
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
    
    for future in as_completed(futures):
        agent_name, response = future.result()
        responses[agent_name] = response

team_agent = MultidisciplinaryTeam(
    cardiologist_report=responses["Cardiologist"],
    psychologist_report=responses["Psychologist"],
    pulmonologist_report=responses["Pulmonologist"]
)

# Run the MultidisciplinaryTeam agent to generate the final diagnosis
final_diagnosis = team_agent.run()
final_diagnosis_text = "### Final Diagnosis:\n\n" + final_diagnosis
txt_output_path = "results/final_diagnosis.txt"

# Ensure the directory exists
os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)

# Write the final diagnosis to the text file
with open(txt_output_path, "w") as txt_file:
    txt_file.write(final_diagnosis_text)

print(f"Final diagnosis has been saved to {txt_output_path}")

'''


# TRAVEL PLANNER WYGR AGENT ----------------------------------------------------------------------------------- 


'''
from wygr.agents.travel_planner import fetch_lat_long,fetch_weather,generate_itinerary_tool,get_location_info_tool,parse_user_input
#from wygr.agents.travel_planner import fetch_lat_long
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    weather_api_key = os.getenv("WEATHER_API_KEY")
    geolocation_api_key = os.getenv("GEOLOCATION_API_KEY")
    openai_api_key = os.getenv("OPEN_API_KEY")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, openai_api_key=openai_api_key)

    user_prompt = input("Enter your travel request (e.g., 'travel plan to Paris for 5 days.'): ")
    destination, days = parse_user_input(user_prompt)

    if destination:
        location_info = get_location_info_tool(destination, geolocation_api_key, weather_api_key)
        if isinstance(location_info, str):
            print(location_info)
        else:
            context = {
                "lat": location_info["lat"],
                "lon": location_info["lon"],
                "weather": location_info["weather"]
            }
            itinerary = generate_itinerary_tool(destination, days, context,llm)
            print(itinerary)
    else:
        print("Error: Invalid input format.")
'''