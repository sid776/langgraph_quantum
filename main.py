import sys
import os

# Make sure our module directories are in the path
sys.path.append(os.path.abspath('.'))

from langgraph_project.supervisor import Supervisor
from langgraph_project.agent import Agent
from langgraph_project.quantum_tools import (
    run_qiskit_circuit, 
    grover_search, 
    shor_simulation, 
    run_azure_quantum
)
from langgraph_project.team import create_team_graph, run_team
# Import the new telecom agents
from langgraph_project.telecom_agents import QueryRoutingAgent, ComplexProblemSolver, LanguageTranslator
from langgraph_project.quantum_router import QuantumRouter

def main():
    print("Initializing Quantum-Enhanced LangGraph System with LLM Agent...")
    
    # Create supervisor
    supervisor = Supervisor()
    
    # Create specialized quantum agents
    agents = {}
    
    bell_state_agent = Agent("BellState", "Bell State Generation")
    bell_state_agent.add_tool("Bell State Circuit", run_qiskit_circuit)
    agents["BellState"] = bell_state_agent
    
    grover_agent = Agent("Grover", "Quantum Search")
    grover_agent.add_tool("Grover's Algorithm", grover_search)
    agents["Grover"] = grover_agent
    
    shor_agent = Agent("Shor", "Quantum Factoring")
    shor_agent.add_tool("Shor's Algorithm", shor_simulation)
    agents["Shor"] = shor_agent
    
    azure_agent = Agent("Azure", "Cloud Quantum")
    azure_agent.add_tool("Azure Quantum", run_azure_quantum)
    agents["Azure"] = azure_agent
    
    # Add new LLM agent for general knowledge
    general_knowledge_agent = Agent("Knowledge", "General Knowledge & Common Sense")
    general_knowledge_agent.add_tool("Answer General Question", lambda: f"Answering: {QuantumRouter.get_current_query()}")
    agents["Knowledge"] = general_knowledge_agent
    
    # Add new telecom agents
    query_router_agent = QueryRoutingAgent("QueryRouter")
    agents["QueryRouter"] = query_router_agent
    
    complex_problem_solver = ComplexProblemSolver("ComplexSolver")
    agents["ComplexSolver"] = complex_problem_solver
    
    language_translator = LanguageTranslator("Translator")
    agents["Translator"] = language_translator
    
    # Add agents to supervisor
    for agent in agents.values():
        supervisor.add_agent(agent)
    
    # Create the team graph
    app = create_team_graph(supervisor, agents)
    
    # Run the team with a query
    while True:
        print("\nQuantum-Enhanced LangGraph Chat System")
        print("=====================================")
        print("Example queries:")
        print("1. Can you explain Bell states?")
        print("2. How does Grover's algorithm work?")
        print("3. What is the capital of France?")
        print("4. My internet connection keeps dropping every few minutes.")
        print("5. I need help with my bill, there's an extra charge I don't recognize.")
        print("6. Can you translate this to Spanish: 'I need help with my account password'?")
        print("Type 'exit' to quit.\n")
        
        query = input("Enter your question: ")
        if query.lower() == 'exit':
            break
            
        result = run_team(app, query)
        print("\nQuery processed. Final state:")
        print(f"Agent: {result['current_agent']}")
        print(f"Status: {result['status']}")
        print("Messages:")
        for msg in result['messages']:
            print(f"- {msg['role']}: {msg['content']}")
            
if __name__ == "__main__":
    main() 