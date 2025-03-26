from typing import Dict, List
import networkx as nx
import matplotlib.pyplot as plt

class QuantumGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.agents = {}
        
    def add_agent_node(self, agent_name: str, agent):
        self.agents[agent_name] = agent
        self.graph.add_node(agent_name)
        
    def add_edge(self, from_agent: str, to_agent: str):
        if from_agent in self.agents and to_agent in self.agents:
            self.graph.add_edge(from_agent, to_agent)
            
    def visualize(self):
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', 
                node_size=1500, font_size=10, font_weight='bold')
        plt.title("Quantum Agent Graph")
        plt.show()
        
    def execute_workflow(self):
        """Execute agents in topological order"""
        try:
            for agent_name in nx.topological_sort(self.graph):
                print(f"\nExecuting {agent_name}...")
                self.agents[agent_name].perform_task()
        except nx.NetworkXUnfeasible:
            print("Error: Graph contains a cycle!") 