from typing import Dict, List, TypedDict, Any
from langgraph.graph import StateGraph, END
from operator import itemgetter
import json

class AgentState(TypedDict):
    messages: List[dict]
    current_agent: str
    task: str
    status: str

def create_team_graph(supervisor, agents):
    workflow = StateGraph(AgentState)
    
    def supervisor_node(state):
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
    
    workflow.add_node("supervisor", supervisor_node)
    
    for name, agent in agents.items():
        def create_agent_node(a=agent, n=name):
            def node(state):
                a.perform_task()
                return {
                    "messages": state["messages"] + [{
                        "content": f"Agent {n} completed task",
                        "role": "agent"
                    }],
                    "current_agent": n,
                    "task": state["task"],
                    "status": "COMPLETED"
                }
            return node
        workflow.add_node(name, create_agent_node())
    
    def route(state):
        return state["current_agent"]
    
    workflow.add_conditional_edges("supervisor", route, list(agents.keys()))
    
    for name in agents:
        workflow.add_edge(name, END)
    
    workflow.set_entry_point("supervisor")
    return workflow.compile()

def run_team(app, query: str):
    state = AgentState(
        messages=[],
        current_agent=None,
        task=query,
        status="RUNNING"
    )
    return app.invoke(state) 