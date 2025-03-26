import sys
import os

# Make sure directories are in the path
sys.path.append(os.path.abspath('.'))

from langgraph_project.supervisor import Supervisor
from langgraph_project.agent import Agent
from langgraph_project.quantum_tools import (
    run_qiskit_circuit, 
    grover_search, 
    shor_simulation, 
    run_azure_quantum
)
from langgraph.llm_tools import answer_general_question

def main():
    print("Initializing Quantum-Enhanced LangGraph System with LLM Agent...")
    
    # Create supervisor
    supervisor = Supervisor()
    
    # Create specialized quantum agents
    bell_state_agent = Agent("BellState", "Bell State Generation")
    bell_state_agent.add_tool("Bell State Circuit", run_qiskit_circuit)
    
    grover_agent = Agent("Grover", "Quantum Search")
    grover_agent.add_tool("Grover's Algorithm", grover_search)
    
    shor_agent = Agent("Shor", "Quantum Factoring")
    shor_agent.add_tool("Shor's Algorithm", shor_simulation)
    
    azure_agent = Agent("Azure", "Cloud Quantum")
    azure_agent.add_tool("Azure Quantum", run_azure_quantum)
    
    # Add LLM agent for general knowledge
    knowledge_agent = Agent("Knowledge", "General Knowledge & Common Sense")
    
    # Add agents to supervisor
    supervisor.add_agent(bell_state_agent)
    supervisor.add_agent(grover_agent)
    supervisor.add_agent(shor_agent)
    supervisor.add_agent(azure_agent)
    supervisor.add_agent(knowledge_agent)
    
    # Connect agents
    supervisor.connect_agents("BellState", "Grover")
    supervisor.connect_agents("Grover", "Shor")
    supervisor.connect_agents("Shor", "Azure")
    supervisor.connect_agents("Azure", "Knowledge")
    
    # Run the interactive loop
    print("\nEnter a question to route it to the best agent.")
    print("- Quantum computing questions will be routed to quantum agents")
    print("- General knowledge questions will be routed to the Knowledge agent")
    print("- Type 'exit' to quit")
    
    while True:
        query = input("\nYour question: ")
        if query.lower() == 'exit':
            break
        
        # Store query for the knowledge agent
        knowledge_agent.add_tool("Answer Question", lambda: answer_general_question(query))
        
        try:
            # Process the query through supervisor
            best_agent, _ = supervisor.process_query(query)
            
            # Execute the agent's task
            agents = {
                "BellState": bell_state_agent,
                "Grover": grover_agent,
                "Shor": shor_agent,
                "Azure": azure_agent,
                "Knowledge": knowledge_agent
            }
            
            # Get the selected agent and execute its task
            selected_agent = agents[best_agent]
            selected_agent.perform_task()
            
            # Ask for commands
            while True:
                command = input("\nEnter command (e.g., 'goto AgentName' or 'exit' or 'new'): ")
                if command.lower() == 'exit':
                    return
                elif command.lower() == 'new':
                    break
                    
                next_agent = supervisor.node.execute_command(command, best_agent)
                if next_agent:
                    print(f"\nMoving to {next_agent}...")
                    best_agent = next_agent
                    agents[best_agent].perform_task()
                else:
                    print("Invalid command or agent not found.")
                    
        except Exception as e:
            print(f"\nError: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main() 