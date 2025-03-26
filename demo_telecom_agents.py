import sys
import os
import json
import test_telecom_agents_mock as telecom

def main():
    print("Telecom Agent Demo System")
    print("========================")
    
    # Create a mock supervisor with the router
    class Supervisor:
        def __init__(self):
            self.router = telecom.MockQuantumRouter({
                "QueryRouter": "Query Routing",
                "ComplexSolver": "Complex Problem Solving",
                "Translator": "Language Translation",
                "Knowledge": "General Knowledge"
            })
        
        def process_query(self, query):
            print(f"\n🔍 Analyzing query: '{query}'")
            rankings = self.router.rank_agents(query)
            best_agent = rankings[0][0]
            
            print("\nAgent Rankings based on Quantum Router:")
            for agent, score in rankings:
                print(f"- {agent}: {score} votes")
                
            return best_agent, rankings
    
    # Create our agent system
    supervisor = Supervisor()
    
    # Create agents
    agents = {
        "QueryRouter": telecom.QueryRoutingAgent(),
        "ComplexSolver": telecom.ComplexProblemSolver(),
        "Translator": telecom.LanguageTranslator(),
        "Knowledge": telecom.MockAgent("Knowledge", "Answering general knowledge questions")
    }
    
    # Simple routing and processing
    def process_query(query):
        # Route the query
        best_agent, rankings = supervisor.process_query(query)
        print(f"\n🔄 Routing to: {best_agent}")
        
        # Execute the agent
        agent = agents[best_agent]
        result = agent.perform_task(query)
        
        # Return the result
        print(f"\n✅ Result from {best_agent}:")
        if isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(result)
            
        return {
            "agent": best_agent,
            "result": result
        }
    
    # Interactive demo
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
            
        process_query(query)
    
if __name__ == "__main__":
    main() 