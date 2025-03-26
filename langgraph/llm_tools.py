import requests
import json
import os

# This is a simple implementation that simulates LLM responses
# In a real application, you would use an actual LLM API like OpenAI, HuggingFace, etc.
class SimpleLLM:
    def __init__(self):
        self.knowledge_base = {
            "capital": {
                "france": "Paris",
                "japan": "Tokyo",
                "india": "New Delhi",
                "usa": "Washington D.C.",
                "uk": "London",
                "germany": "Berlin",
                "italy": "Rome"
            },
            "planet": {
                "closest to sun": "Mercury",
                "largest": "Jupiter",
                "with rings": "Saturn, Jupiter, Uranus, Neptune",
                "we live on": "Earth",
                "red planet": "Mars"
            },
            "element": {
                "lightest": "Hydrogen",
                "most abundant in universe": "Hydrogen",
                "most abundant in earth crust": "Oxygen",
                "in water": "Hydrogen and Oxygen"
            }
        }
    
    def query(self, question):
        """Process a natural language query and return a response"""
        question = question.lower()
        
        # Basic pattern matching for capital questions
        if "capital" in question:
            for country, capital in self.knowledge_base["capital"].items():
                if country in question:
                    return f"The capital of {country.title()} is {capital}."
        
        # Basic pattern matching for planet questions
        if "planet" in question:
            for descriptor, planet in self.knowledge_base["planet"].items():
                if descriptor in question:
                    return f"The planet {descriptor} is {planet}."
        
        # Basic pattern matching for element questions
        if "element" in question:
            for descriptor, element in self.knowledge_base["element"].items():
                if descriptor in question:
                    return f"The element {descriptor} is {element}."
        
        # Default response for unrecognized questions
        return "I don't have enough information to answer that question specifically. Please try asking about capitals of countries, planets in our solar system, or chemical elements."

def answer_general_question(question):
    """Use a simple LLM to answer general knowledge questions"""
    llm = SimpleLLM()
    answer = llm.query(question)
    
    print(f"\nGeneral Knowledge Question: {question}")
    print(f"Answer: {answer}")
    
    return answer

# In a real implementation, you might use an actual LLM API like this:
def call_openai_api(question):
    """Call OpenAI API to get an answer (example implementation)"""
    # Replace with your actual API key
    api_key = os.environ.get("OPENAI_API_KEY", "your-api-key")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 150
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}" 