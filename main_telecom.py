import sys
import os
import json

# Make sure module directories are in the path
sys.path.append(os.path.abspath('.'))

# Import the mock telecom modules from our test file
from test_telecom_agents_mock import (
    MockAgent, MockQuantumRouter, 
    QueryRoutingAgent, ComplexProblemSolver, LanguageTranslator
)

class SimpleSupervisor:
    def __init__(self):
        # Initialize with our agents
        self.agent_names = [
            "QueryRouter", "ComplexSolver", "Translator", "Knowledge"
        ]
        self.router = MockQuantumRouter(self.agent_names)
    
    def process_query(self, query):
        # Use the router to rank agents
        rankings = self.router.rank_agents(query)
        best_agent = rankings[0][0]
        
        print("\nAgent Rankings based on Quantum Router:")
        for agent, score in rankings:
            print(f"- {agent}: {score} votes")
            
        return best_agent, rankings

def main():
    print("Quantum-Enhanced Telecom Agent System")
    print("====================================")
    
    # Create supervisor
    supervisor = SimpleSupervisor()
    
    # Create agents
    agents = {}
    
    # Add telecom agents
    agents["QueryRouter"] = QueryRoutingAgent("QueryRouter")
    agents["ComplexSolver"] = ComplexProblemSolver("ComplexSolver")
    agents["Translator"] = LanguageTranslator("Translator")
    
    # Add knowledge agent
    agents["Knowledge"] = MockAgent("Knowledge", "General Knowledge & Common Sense")
    
    # Simple execution function
    def execute_query(query):
        # Route the query
        best_agent, rankings = supervisor.process_query(query)
        print(f"\n🔄 Routing to: {best_agent}")
        
        # Execute the best agent
        agent = agents[best_agent]
        result = agent.perform_task(query)
        
        # Print the result
        print(f"\n✅ Result from {best_agent}:")
        if isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(result)
            
        return {
            "agent": best_agent,
            "result": result
        }
    
    # Run the interactive demo
    print("\nExample queries:")
    print("1. I need help with my bill, who should I talk to?")
    print("2. My internet connection keeps dropping every few minutes, especially when it rains.")
    print("3. Can you translate this to Spanish: 'I need help with my account password'")
    print("4. What's the capital of France? (Knowledge)")
    print("Type 'exit' to quit.\n")
    
    while True:
        query = input("\nEnter your question: ")
        if query.lower() == 'exit':
            break
            
        # Process the query
        execute_query(query)
            
if __name__ == "__main__":
    main() 