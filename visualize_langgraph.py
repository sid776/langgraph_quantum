from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

# Define the state type
class State(TypedDict):
    current_step: str

# Create the graph
workflow = StateGraph(State)

# Add nodes for our quantum workflow
def input_processing(state: State):
    return {"current_step": "input_processed"}

def quantum_processing(state: State):
    return {"current_step": "quantum_processed"}

def output_generation(state: State):
    return {"current_step": "complete"}

# Add nodes to the graph
workflow.add_node("input", input_processing)
workflow.add_node("quantum", quantum_processing)
workflow.add_node("output", output_generation)

# Add edges
workflow.add_edge(START, "input")
workflow.add_edge("input", "quantum")
workflow.add_edge("quantum", "output")
workflow.add_edge("output", END)

# Compile the graph
app = workflow.compile()

# Generate PNG using Mermaid.ink API
graph_png = app.get_graph().draw_mermaid_png(
    curve_style=CurveStyle.LINEAR,
    node_colors=NodeStyles(
        first="#ffdfba",  # Start node color
        last="#baffc9",   # End node color
        default="#f2f0ff" # Default node color
    ),
    draw_method=MermaidDrawMethod.API,
    background_color="white",
    padding=10
)

# Save the PNG
with open("quantum_workflow.png", "wb") as f:
    f.write(graph_png)

print("Graph has been saved as 'quantum_workflow.png'") 