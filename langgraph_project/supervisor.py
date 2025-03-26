from typing import Dict, List, Tuple, Optional
from langgraph_project.quantum_router import QuantumRouter

class SupervisorNode:
    def __init__(self):
        self.agents = {}
        self.router = None
        self.current_agent = None
    
    def initialize_router(self):
        self.router = QuantumRouter(self.agents)
    
    def route_query(self, query: str) -> Tuple[str, List[Tuple[str, int]]]:
        rankings = self.router.rank_agents(query)
        best_agent = rankings[0][0]
        return best_agent, rankings
    
    def execute_command(self, command: str, current_agent: str) -> Optional[str]:
        if command.lower().startswith("goto"):
            target = command.split()[1]
            if target in self.agents:
                return target
        return None

class Supervisor:
    def __init__(self):
        self.node = SupervisorNode()
        
    def add_agent(self, agent):
        agent_name = agent.name
        self.node.agents[agent_name] = agent
        
    def connect_agents(self, from_agent: str, to_agent: str):
        # Just a placeholder for potential future connections
        pass
        
    def process_query(self, query: str):
        if not self.node.router:
            self.node.initialize_router()
            
        best_agent, rankings = self.node.route_query(query)
        
        print("\nAgent Rankings based on Quantum Router:")
        for agent, score in rankings:
            print(f"{agent}: {score} votes")
            
        return best_agent, rankings
    
    def execute_workflow(self, query: str):
        current_agent = self.process_query(query)
        current_agent.perform_task()
        
        while True:
            command = input("\nEnter command (e.g., 'goto AgentName' or 'exit'): ")
            if command.lower() == 'exit':
                break
                
            next_agent = self.node.execute_command(command, current_agent.name)
            if next_agent:
                print(f"\nMoving to {next_agent}...")
                current_agent = self.node.agents[next_agent]
                current_agent.perform_task()
            else:
                print("Invalid command or agent not found.") 