# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from crewai import Agent, Task, Crew, Process
# from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
# from langchain_community.tools.tavily_search.tool import TavilySearchResults
# import os
# from crewai_tools import SerperDevTool
# from dotenv import load_dotenv
# import sys
# import threading
# import queue
# from langchain_groq import ChatGroq

# crew_result_store = {}

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "https://tripbharat.netlify.app"}}, supports_credentials=True)
# load_dotenv()

# groq_api_key = os.environ.get("GROQ_API_KEY")
# tavily_api_key = os.environ.get("TAVILY_API_KEY")
# serper_api_key = os.environ.get("SERPER_API_KEY")

# llm = ChatGroq(api_key=groq_api_key, model="llama3-8b-8192")
# search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
# tavily_tool = TavilySearchResults(api_wrapper=search)
# tool = SerperDevTool(serper_api_key=serper_api_key)


# output_queue = queue.Queue()

# class StreamToQueue:
#     def __init__(self, queue):
#         self.queue = queue

#     def write(self, message):
#         self.queue.put(message)

#     def flush(self):
#         pass

# sys.stdout = StreamToQueue(output_queue)
# sys.stderr = StreamToQueue(output_queue)

# def create_crewai_setup(category, budget, num_people, trip_type, month):
#     Travel_Agent = Agent(
#         role="Trip Maker Expert",
#         goal=f"""Recommend place in India for planning a trip, considering the category, budget per head, number of people traveling, and type of trip.
#                 Category: {category}
#                 Budget: {budget}
#                 Number of People: {num_people}
#                 Type: {trip_type}
#                 Time: {month}

#                 Important:
#                     - Final output must contain all the detailed key insights of the locations perfect for customs, culture 
#                     information, tourist attractions, activities, food.
#                     - The final output must contain detailed reasoning why you are recommending that places.
#                     - The final output must contain a proper breakdown of expenses.
#                     - Avoid reusing the same input.

# """,
#         backstory=f"""Expert at understanding the users demand like {category}, 
#                     {budget}, {num_people}, {trip_type}, {month} and recommending 
#                     the place in  India they must visit.Skilled in recommending with detailed 
#                     insights of the place.""",
#         verbose=True,
#         allow_delegation=True,
#         tools=[tavily_tool, tool],
#         llm=llm,
#     )

#     city_insights = Agent(
#         role="Local City Expert",
#         goal=f"""Provide the BEST insights about the cities of India.
#             Important:
#                     - Once you know the selected city, provide keenly researched insights of the city.
#                     - Research local events, activities, food, transport, and accommodation information.
#                     - Keep the information detailed.
#                     - Avoid reusing the same input.""",
#         backstory=f"""A knowledgeable local guide with extensive information 
#                     about the every city of India, its attractions, customs and always updated 
#                     about current events in city.""",
#         verbose=True,
#         allow_delegation=True,
#         tools=[tavily_tool, tool],
#         llm=llm,
#     )

#     task1 = Task(
#         description=f"""Research about the recommended place and provide keen insights into the place, 
#         including food, costs, accommodation, tourist attractions, transport, and dos and don'ts.
            
#                 Helpful Tips:
#                 - To find blog articles and Google results, perform searches on Google such as the following:
#                 - "Trip to {category} as {trip_type} in India under {budget}"
                
#                 Important:
#                 - Do not generate fake information or improper budget breakdown. Only return the information you find. Nothing else!""",
#         expected_output="Detailed information of the city.",
#         agent=city_insights,
#     )

#     task2 = Task(
#         description=f"""Based on the factors like {category}, 
#         in budget of {budget}, number of people traveling are {num_people}, and type of trip {trip_type}, 
#         in the month of {month} use the results from the Trip Maker Expert to compile all the information in a 
#         well-formatted manner. The pointers should be detailed.""",
#         expected_output="Detailed and clear report of recommendation.",
#         agent=Travel_Agent,
#         context= [task1]
#     )

#     travel_crew = Crew(
#         agents=[Travel_Agent, city_insights],
#         tasks=[task1, task2],
#         verbose=2,
#         process=Process.sequential,
#     )

#     crew_result = travel_crew.kickoff()
#     crew_result_store[(category, trip_type, month, budget, num_people)] = crew_result
#     return crew_result

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.get_json()
#     category = data.get('category')
#     budget = data.get('budget')
#     num_people = data.get('num_people')
#     trip_type = data.get('trip_type')
#     month = data.get('month')

#     if not (category and budget and num_people and trip_type and month):
#         return jsonify({'error': 'There is a missing identity'}), 400

#     threading.Thread(target=create_crewai_setup, args=(category, budget, num_people, trip_type, month)).start()
#     return jsonify({'status': 'Processing started'})

# @app.route('/logs', methods=['GET'])
# def get_logs():
#     logs = []
#     while not output_queue.empty():
#         logs.append(output_queue.get())
#     return jsonify({'logs': logs})

# # @app.before_request
# # def before_request_func():
# #     if request.method == 'OPTIONS':
# #         response = make_response()
# #         response.headers.add("Access-Control-Allow-Origin", "https://tripbharat.netlify.app")
# #         response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
# #         response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
# #         return response


# @app.route('/crew_result', methods=['GET'])
# def get_crew_result():
#     category = request.args.get('category')
#     budget = request.args.get('budget')
#     num_people = request.args.get('num_people')
#     trip_type = request.args.get('trip_type')
#     month = request.args.get('month')

#     key = (category, trip_type, month, budget, num_people)
#     result = crew_result_store.get(key, "Result not available yet.")
#     return jsonify({'crew_result': result})
from flask import Flask, request, jsonify
from flask_cors import CORS
from crewai import Agent, Task, Crew, Process
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search.tool import TavilySearchResults
import os
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import sys
import threading
import queue
from langchain_groq import ChatGroq
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

# Set up Flask app with CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://tripbharat.netlify.app"}})

# Initialize API keys from environment
groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# Initialize Language Model and Tools
llm = ChatGroq(api_key=groq_api_key, model="llama3-8b-8192")
search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
tavily_tool = TavilySearchResults(api_wrapper=search)
tool = SerperDevTool(serper_api_key=serper_api_key)

# Global result storage
crew_result_store = {}

# Queue for logging output
output_queue = queue.Queue()

# Setup ThreadPoolExecutor for better thread management
executor = ThreadPoolExecutor(max_workers=5)

class StreamToQueue:
    def __init__(self, queue):
        self.queue = queue

    def write(self, message):
        if message.strip():  # Avoid empty log messages
            self.queue.put(message.strip())

    def flush(self):
        pass

sys.stdout = StreamToQueue(output_queue)
sys.stderr = StreamToQueue(output_queue)

def create_crewai_setup(category, budget, num_people, trip_type, month):
    """Setup CrewAI agents and tasks."""
    Travel_Agent = Agent(
        role="Trip Maker Expert",
        goal=f"""Recommend a place in India for planning a trip, considering the category, budget per head, 
                number of people traveling, and type of trip.""",
        backstory=f"""Expert at understanding users' demands like {category}, {budget}, {num_people}, 
                    {trip_type}, {month} and recommending the best places in India.""",
        verbose=True,
        allow_delegation=True,
        tools=[tavily_tool, tool],
        llm=llm,
    )

    city_insights = Agent(
        role="Local City Expert",
        goal=f"""Provide detailed insights about cities in India, including events, activities, food, 
                 transport, and accommodation.""",
        backstory=f"""A knowledgeable local guide with extensive information about every city in India, 
                    its attractions, customs, and current events.""",
        verbose=True,
        allow_delegation=True,
        tools=[tavily_tool, tool],
        llm=llm,
    )

    task1 = Task(
        description=f"""Research the recommended place and provide keen insights into the location.""",
        expected_output="Detailed information of the city.",
        agent=city_insights,
    )

    task2 = Task(
        description=f"""Compile information based on the given factors into a well-formatted report.""",
        expected_output="Detailed and clear report of recommendation.",
        agent=Travel_Agent,
        context=[task1]
    )

    travel_crew = Crew(
        agents=[Travel_Agent, city_insights],
        tasks=[task1, task2],
        verbose=2,
        process=Process.sequential,
    )

    # Execute tasks and store results
    crew_result = travel_crew.kickoff()
    key = (category, trip_type, month, budget, num_people)
    crew_result_store[key] = crew_result
    return crew_result

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle analyze request to setup and execute CrewAI tasks."""
    data = request.get_json()
    category = data.get('category')
    budget = data.get('budget')
    num_people = data.get('num_people')
    trip_type = data.get('trip_type')
    month = data.get('month')

    if not all([category, budget, num_people, trip_type, month]):
        return jsonify({'error': 'There is a missing identity'}), 400

    # Use ThreadPoolExecutor to handle requests in a thread-safe manner
    executor.submit(create_crewai_setup, category, budget, num_people, trip_type, month)
    return jsonify({'status': 'Processing started'})

@app.route('/logs', methods=['GET'])
def get_logs():
    """Retrieve and return logs."""
    logs = []
    while not output_queue.empty():
        logs.append(output_queue.get())
    return jsonify({'logs': logs})

@app.route('/crew_result', methods=['GET'])
def get_crew_result():
    """Retrieve and return the result of a CrewAI task."""
    category = request.args.get('category')
    budget = request.args.get('budget')
    num_people = request.args.get('num_people')
    trip_type = request.args.get('trip_type')
    month = request.args.get('month')

    key = (category, trip_type, month, budget, num_people)
    result = crew_result_store.get(key, "Result not available yet.")
    return jsonify({'crew_result': result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


