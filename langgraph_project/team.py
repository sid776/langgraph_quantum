from typing import Dict, List, TypedDict, Any, Annotated
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
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
    """Create a team graph using a simpler approach"""
    
    # Initialize the graph with our AgentState
    builder = StateGraph(AgentState)
    
    # Add supervisor node
    def supervisor_node(state: AgentState) -> AgentState:
        query = state.get("task", "")
        best_agent, rankings = supervisor.process_query(query)
        
        # Set the chosen agent and return updated state
        state = {
            "messages": state.get("messages", []) + [{
                "content": f"Supervisor routing to: {best_agent}",
                "role": "supervisor"
            }],
            "current_agent": best_agent,
            "task": query,
            "status": "RUNNING"
        }
        
        # Execute the chosen agent node directly
        if best_agent in agents:
            agent = agents[best_agent]
            
            # Execute the agent
            if hasattr(agent, 'perform_task') and callable(agent.perform_task):
                # Get the number of parameters the function accepts
                import inspect
                sig = inspect.signature(agent.perform_task)
                if len(sig.parameters) > 0:
                    # Call with the query if it accepts parameters
                    result = agent.perform_task(query)
                else:
                    # Call without parameters if it doesn't accept any
                    result = agent.perform_task()
            else:
                # Fallback if there's no perform_task method
                result = f"{best_agent} processed the query but doesn't have a perform_task method"
            
            # Add result to response if available
            response_content = f"Agent {best_agent} completed task"
            if result:
                if isinstance(result, dict):
                    response_content = f"Agent {best_agent} result: {json.dumps(result, indent=2)}"
                else:
                    response_content = f"Agent {best_agent} result: {result}"
            
            state["messages"].append({
                "content": response_content,
                "role": "agent"
            })
            state["status"] = "COMPLETED"
        
        return state
    
    # Add nodes to graph
    builder.add_node("supervisor", supervisor_node)
    
    # Just set the entry point - all work is done in the supervisor node
    builder.set_entry_point("supervisor")
    
    # Compile the graph
    graph = builder.compile()
    
    return graph

def run_team(app, query: str):
    """Execute the team workflow for a given query"""
    initial_state = {
        "messages": [],
        "current_agent": None,
        "task": query,
        "status": "RUNNING"
    }
    result = app.invoke(initial_state)
    return result 