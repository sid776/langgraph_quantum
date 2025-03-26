import os

# Simple LLM implementation for answering general knowledge questions
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

# Agent class for different specialized tasks
class Agent:
    def __init__(self, name, skill, tools=None):
        self.name = name
        self.skill = skill
        self.tools = tools if tools else {}
        
    def add_tool(self, tool_name, tool_function):
        self.tools[tool_name] = tool_function
        
    def perform_task(self):
        print(f"\nAgent {self.name} is active:")
        print(f"Specialized in: {self.skill}")
        if self.tools:
            print("Available tools:")
            for tool_name in self.tools:
                print(f"- {tool_name}")
            
            # Execute tools if available
            for tool_name, tool_function in self.tools.items():
                print(f"\nExecuting {tool_name}:")
                tool_function()

# Function to answer general questions using the SimpleLLM
def answer_general_question(question):
    """Use a simple LLM to answer general knowledge questions"""
    llm = SimpleLLM()
    answer = llm.query(question)
    
    print(f"\nGeneral Knowledge Question: {question}")
    print(f"Answer: {answer}")
    
    return answer

def main():
    print("=== Quantum LangGraph with LLM Agent ===")
    print("This agent can answer general knowledge questions")
    
    # Create the knowledge agent
    knowledge_agent = Agent("Knowledge", "General Knowledge & Common Sense")
    
    # Run interactive loop
    while True:
        question = input("\nEnter your question (or 'exit' to quit): ")
        if question.lower() == 'exit':
            break
            
        # Add tool with the current question
        knowledge_agent.add_tool("Answer Question", lambda: answer_general_question(question))
        
        # Perform the task
        knowledge_agent.perform_task()

if __name__ == "__main__":
    main() 