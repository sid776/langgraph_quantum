import sys
import os
import json

# Import agent base class
from langgraph_project.agent import Agent

# Import telecom agents
from telecom_agents_demo import (
    QueryRoutingAgent, 
    ComplexProblemSolver, 
    LanguageTranslator, 
    Supervisor,
    create_team_graph,
    run_team
)

def main():
    print("Quantum-Enhanced Telecom Agent System")
    print("====================================")
    
    # Create supervisor
    supervisor = Supervisor()
    
    # Create agents
    agents = {}
    
    # Add telecom agents
    query_router = QueryRoutingAgent("QueryRouter")
    agents["QueryRouter"] = query_router
    
    complex_solver = ComplexProblemSolver("ComplexSolver")
    agents["ComplexSolver"] = complex_solver
    
    translator = LanguageTranslator("Translator")
    agents["Translator"] = translator
    
    # Add general knowledge agent
    knowledge_agent = Agent("Knowledge", "General Knowledge & Common Sense")
    agents["Knowledge"] = knowledge_agent
    
    # Add agents to supervisor
    for agent_name, agent in agents.items():
        supervisor.add_agent(agent)
    
    # Create the team graph
    app = create_team_graph(supervisor, agents)
    
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
        result = run_team(app, query)
        
        # Display the results
        print("\nQuery processed. Final state:")
        print(f"Agent: {result['current_agent']}")
        print(f"Status: {result['status']}")
        print("Messages:")
        for msg in result['messages']:
            print(f"- {msg['role']}: {msg['content']}")
            
if __name__ == "__main__":
    main() 