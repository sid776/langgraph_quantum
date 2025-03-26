from typing import Dict, List, TypedDict, Any
from langgraph.graph import StateGraph, END
from operator import itemgetter
import json

# Define our state
class AgentState(TypedDict):
    """The state of the system."""
    messages: List[dict]
    current_agent: str
    task: str
    status: str

def create_team_graph(supervisor, agents):
    """Create a hierarchical team graph with supervisor and agent nodes"""
    
    # Initialize the graph with the state
    builder = StateGraph(AgentState)
    
    # Add supervisor node
    def supervisor_node(state: AgentState):
        query = state["task"]
        best_agent, rankings = supervisor.process_query(query)
        
        return {
            "messages": state["messages"] + [{
                "content": f"Supervisor routing to: {best_agent}",
                "role": "supervisor"
            }],
            "current_agent": best_agent,
            "task": query,
            "status": "RUNNING"
        }
    
    # Add nodes to graph
    builder.add_node("supervisor", supervisor_node)
    
    # Add agent nodes
    for agent_name, agent in agents.items():
        def make_agent_node(agent_to_use, agent_name_to_use):
            def agent_node(state: AgentState):
                agent_to_use.perform_task()
                return {
                    "messages": state["messages"] + [{
                        "content": f"Agent {agent_name_to_use} completed task",
                        "role": "agent"
                    }],
                    "current_agent": agent_name_to_use,
                    "task": state["task"],
                    "status": "COMPLETED"
                }
            return agent_node
        
        builder.add_node(agent_name, make_agent_node(agent, agent_name))
    
    # Define possible next nodes
    next_nodes = list(agents.keys())
    
    # Add edges from supervisor to each agent
    def get_next_agent(state: AgentState) -> str:
        return state["current_agent"]
    
    builder.add_conditional_edges(
        source="supervisor",
        condition=get_next_agent,
        destinations=next_nodes
    )
    
    # Add edges from agents to END
    for agent_name in agents:
        builder.add_edge(agent_name, END)
    
    # Set entry point
    builder.set_entry_point("supervisor")
    
    # Compile the graph
    graph = builder.compile()
    
    return graph

def run_team(app, query: str):
    """Execute the team workflow for a given query"""
    initial_state = AgentState(
        messages=[],
        current_agent=None,
        task=query,
        status="RUNNING"
    )
    result = app.invoke(initial_state)
    return result 