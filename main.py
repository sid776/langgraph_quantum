import sys
import os
from typing import Literal, Annotated, Dict, List, Any

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

from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver

def format_detailed_response(agent_name, query, result=None):
    """Format a detailed response with recommendations and explanations"""
    detailed_responses = {
        "BellState": {
            "title": "Bell State Analysis and Recommendations",
            "sections": [
                "Quantum State Overview",
                "Entanglement Properties",
                "Practical Applications",
                "Next Steps"
            ],
            "content": {
                "Quantum State Overview": "Bell states are maximally entangled quantum states of two qubits. They form the foundation of many quantum protocols and are represented as superpositions of computational basis states. Our implementation uses Hadamard and CNOT gates to create this entanglement, resulting in a quantum state where measuring one qubit instantly determines the state of the other.",
                "Entanglement Properties": "The entanglement in Bell states demonstrates non-local quantum correlations that Einstein called 'spooky action at a distance.' When measured, the two qubits always show correlated results regardless of the distance between them. This quantum entanglement is a resource that powers many quantum information protocols.",
                "Practical Applications": "Bell states are fundamental to quantum teleportation, superdense coding, and quantum key distribution protocols like BB84. They're also used in quantum computing for creating entangled resources and in tests of quantum mechanics like Bell inequality experiments.",
                "Next Steps": "To further explore Bell states, we recommend:"
            },
            "recommendations": [
                "Visualize the quantum state using our interactive simulator to see probability distributions",
                "Explore different measurement bases to understand how superposition affects outcomes",
                "Learn about quantum teleportation applications which use Bell states for information transfer",
                "Try creating different entangled states (such as GHZ or W states) for multi-qubit systems"
            ]
        },
        "Grover": {
            "title": "Grover's Algorithm Analysis and Recommendations",
            "sections": [
                "Algorithm Overview",
                "Search Space Analysis",
                "Performance Metrics",
                "Optimization Opportunities"
            ],
            "content": {
                "Algorithm Overview": "Grover's algorithm provides a quadratic speedup for unstructured search problems. It uses quantum superposition to search through all possibilities simultaneously, and amplitude amplification to increase the probability of finding the correct answer. Our implementation demonstrates this with a 3-qubit system searching for a specific marked state.",
                "Search Space Analysis": "The current implementation searches through 2^3=8 possible states, targeting the state '101'. The oracle marks this state with a phase flip, and the diffusion operator amplifies its amplitude. In larger search spaces, Grover's algorithm would show even more dramatic advantages over classical search.",
                "Performance Metrics": "Grover's algorithm requires approximately √N iterations for a search space of size N, compared to O(N) for classical algorithms. Our simulator shows high probability concentration on the target state after just one Grover iteration, demonstrating the quantum advantage.",
                "Optimization Opportunities": "The algorithm can be further optimized with precise phase matching, custom oracle design for specific problems, and quantum error mitigation techniques for larger search spaces."
            },
            "recommendations": [
                "Experiment with different database sizes to see how the quantum advantage scales with problem size",
                "Analyze the quantum circuit complexity by visualizing the gates and their effects on amplitudes",
                "Compare with classical search algorithms to quantify the speedup for different problem sizes",
                "Explore real-world applications in database search, optimization problems, and cryptanalysis"
            ]
        },
        "Shor": {
            "title": "Shor's Algorithm Analysis and Recommendations",
            "sections": [
                "Algorithm Components",
                "Quantum Fourier Transform",
                "Period Finding",
                "Implementation Considerations"
            ],
            "content": {
                "Algorithm Components": "Shor's algorithm consists of two main parts: a classical part that reduces factoring to period finding, and a quantum part that efficiently solves the period finding problem. Our implementation focuses on the quantum Fourier transform component which is central to the algorithm's exponential speedup.",
                "Quantum Fourier Transform": "The QFT in our simulation transforms quantum states from the computational basis to the Fourier basis, using Hadamard gates and controlled phase rotations. This transformation is crucial for extracting the periodicity information needed for factoring large numbers.",
                "Period Finding": "The algorithm finds the period of a modular exponentiation function, which is directly related to the factors of a number. The quantum advantage comes from the QFT's ability to extract periodic information exponentially faster than classical algorithms.",
                "Implementation Considerations": "While our simulation demonstrates the principles on a small scale, practical implementations require error correction and a large number of qubits to factor numbers relevant to cryptography. Current quantum computers are still in the 'NISQ' era (Noisy Intermediate-Scale Quantum) with limited qubit counts and coherence times."
            },
            "recommendations": [
                "Study the quantum phase estimation process in detail to understand how periods are extracted",
                "Explore different number factorization scenarios to see how the algorithm scales with bit length",
                "Learn about quantum error correction requirements for reliable implementation of Shor's algorithm",
                "Understand post-quantum cryptography implications since Shor's algorithm threatens RSA encryption"
            ]
        },
        "Knowledge": {
            "title": "Knowledge Base Analysis and Recommendations",
            "sections": [
                "Topic Overview",
                "Related Concepts",
                "Additional Resources",
                "Learning Path"
            ],
            "content": {
                "Topic Overview": f"Based on your query '{query}', our knowledge base provides foundational information about this topic. Our pattern-matching system has identified key concepts and relevant information to address your specific question.",
                "Related Concepts": "Your query connects to several related topics in our knowledge base. We've identified patterns suggesting connections to complementary subjects that would enhance your understanding of this area.",
                "Additional Resources": "Our knowledge base contains supplementary materials including documentation, tutorials, academic papers, and practical examples that expand on this topic in various contexts and applications.",
                "Learning Path": "We recommend a structured approach to mastering this topic, starting with foundational concepts and progressively exploring more advanced applications."
            },
            "recommendations": [
                "Explore related topics in our knowledge base to gain a comprehensive understanding",
                "Access detailed documentation and examples through our interactive learning portal",
                "Connect with subject matter experts through our community forum for personalized guidance",
                "Follow a structured learning path customized to your current knowledge level and goals"
            ]
        },
        "QueryRouter": {
            "title": "Service Analysis and Recommendations",
            "sections": [
                "Service Assessment",
                "Available Options",
                "Best Practices",
                "Next Steps"
            ],
            "content": {
                "Service Assessment": f"Based on your query '{query}', we've analyzed the service requirements and identified the most relevant department for your needs. Our pattern-matching system has detected key terms related to specific service categories.",
                "Available Options": "We offer multiple service tiers and options tailored to different needs and scenarios. Each option provides specific features, support levels, and pricing structures designed to address various use cases.",
                "Best Practices": "For optimal service experience, we recommend following established guidelines for your specific service category. These practices have been developed based on extensive customer feedback and operational insights.",
                "Next Steps": "To proceed with your service request, consider the following recommendations:"
            },
            "recommendations": [
                "Review detailed service documentation in our knowledge center to understand capabilities and limitations",
                "Compare different service tiers using our interactive comparison tool to find the best fit for your needs",
                "Schedule a consultation with our experts for personalized service configuration advice",
                "Explore integration possibilities with your existing systems through our API documentation"
            ]
        },
        "ComplexSolver": {
            "title": "Problem Analysis and Detailed Recommendations",
            "sections": [
                "Issue Assessment",
                "Root Cause Analysis",
                "Solution Options",
                "Implementation Plan"
            ],
            "content": {
                "Issue Assessment": f"We've analyzed your issue '{query}' and identified it as a complex problem with multiple potential factors. The symptoms you've described suggest interactions between several system components or environmental conditions that require a comprehensive troubleshooting approach.",
                "Root Cause Analysis": "Based on pattern matching and historical data, we've identified several potential root causes: 1) Configuration inconsistencies between interconnected systems, 2) Resource constraints under specific conditions, 3) Timing-related issues in asynchronous processes, and 4) Environmental factors affecting normal operation.",
                "Solution Options": "We've developed multiple solution approaches tailored to address the identified causes. Each option balances implementation complexity, time requirements, and effectiveness based on the specific context of your issue.",
                "Implementation Plan": "To resolve this complex issue, we recommend a phased approach that systematically addresses potential causes while minimizing disruption to existing operations."
            },
            "recommendations": [
                "Review our detailed troubleshooting guide with step-by-step diagnostics for your specific issue type",
                "Schedule a technical consultation with our specialized engineers for personalized problem analysis",
                "Explore alternative solution approaches that may provide more efficient resolution paths",
                "Create a maintenance plan to prevent similar issues through proactive monitoring and optimization"
            ]
        },
        "Translator": {
            "title": "Translation Analysis and Recommendations",
            "sections": [
                "Translation Quality",
                "Language Options",
                "Best Practices",
                "Additional Services"
            ],
            "content": {
                "Translation Quality": f"We've analyzed your translation request '{query}' and processed it using our pattern-matching translation system. The translation quality is suitable for basic communication but may benefit from refinement for technical or nuanced content.",
                "Language Options": "Our system currently supports translations between English and Spanish with a focus on common phrases and technical terminology related to our services. We're continually expanding our language capabilities based on user needs.",
                "Best Practices": "For optimal translation results, we recommend using clear, concise statements without idioms or culture-specific references. Providing context for technical terms improves translation accuracy significantly.",
                "Additional Services": "Beyond basic translation, we offer additional language services to enhance communication effectiveness across language barriers."
            },
            "recommendations": [
                "Review translation accuracy using our feedback mechanism to help improve future translations",
                "Explore additional language options currently in beta testing for your specific needs",
                "Learn about our localization services for adapting content to specific cultural contexts",
                "Consider professional translation services for critical communications requiring perfect accuracy"
            ]
        },
        "Azure": {
            "title": "Azure Quantum Analysis and Recommendations",
            "sections": [
                "Cloud Quantum Overview",
                "Implementation Status",
                "Resource Requirements",
                "Next Steps"
            ],
            "content": {
                "Cloud Quantum Overview": "Azure Quantum provides access to quantum hardware and simulators through Microsoft's cloud platform. It supports various quantum programming languages and frameworks, enabling experimentation with quantum algorithms without investing in physical quantum hardware.",
                "Implementation Status": "The Azure Quantum integration is currently in development. When fully implemented, it will allow running our quantum algorithms on real quantum processors or advanced simulators through the Azure cloud service.",
                "Resource Requirements": "To use Azure Quantum, you'll need an Azure subscription, an Azure Quantum workspace, and proper authentication credentials. Quantum computing resources are billed based on execution time and the type of quantum processor selected.",
                "Next Steps": "While we complete the Azure Quantum integration, consider the following recommendations:"
            },
            "recommendations": [
                "Create an Azure account and explore the Azure Quantum documentation to understand available resources",
                "Practice with Q# or Qiskit locally to prepare algorithms for cloud execution",
                "Familiarize yourself with quantum resource estimation to optimize usage costs",
                "Join the Azure Quantum Network for early access to new quantum hardware and features"
            ]
        }
    }
    
    # Get the template for this agent
    template = detailed_responses.get(agent_name, {
        "title": f"{agent_name} Analysis and Recommendations",
        "sections": [
            "Overview",
            "Analysis",
            "Options",
            "Next Steps"
        ],
        "content": {
            "Overview": f"We've processed your query: '{query}' using our {agent_name} system. This agent specializes in providing specific expertise for this type of request.",
            "Analysis": f"The {agent_name} agent has analyzed your request and determined the relevant information to address your needs. We've applied specialized processing techniques to ensure accurate results.",
            "Options": "Based on your query, we've identified several options that might be relevant to your needs. Each option offers different advantages depending on your specific context and requirements.",
            "Next Steps": "To get the most value from this information, consider the following recommended next steps:"
        },
        "recommendations": [
            "Explore more detailed information through our knowledge base and documentation",
            "Consider alternative approaches that might better align with your specific requirements",
            "Review best practices from our community of users and experts",
            "Plan your next steps with our guided implementation resources"
        ]
    })
    
    # Format a simplified response for the LangGraph message system
    response = f"{template['title']}\n\n"
    
    # Add primary content from the first section
    first_section = template['sections'][0]
    if 'content' in template and first_section in template['content']:
        response += f"{template['content'][first_section]}\n\n"
    
    # Add key recommendations
    response += "Recommendations:\n"
    for i, rec in enumerate(template['recommendations'][:2], 1):
        response += f"{i}. {rec}\n"
    
    return response

def handle_follow_up(previous_agent, previous_query, previous_result):
    """Generate follow-up questions based on the previous interaction"""
    follow_up_prompts = {
        "BellState": [
            "Would you like to see a visualization of the Bell state?",
            "Would you like to learn more about quantum entanglement?",
            "Would you like to try a different quantum state?"
        ],
        "Grover": [
            "Would you like to see how Grover's algorithm performs with different search spaces?",
            "Would you like to learn more about quantum search algorithms?",
            "Would you like to try a different quantum algorithm?"
        ],
        "Shor": [
            "Would you like to see how Shor's algorithm works with different numbers?",
            "Would you like to learn more about quantum factoring?",
            "Would you like to explore other quantum algorithms?"
        ],
        "Knowledge": [
            "Would you like to know more about this topic?",
            "Would you like to explore a related subject?",
            "Would you like to ask about something else?"
        ],
        "QueryRouter": [
            "Would you like more details about this service?",
            "Would you like to explore other service options?",
            "Would you like to speak with a different department?"
        ],
        "ComplexSolver": [
            "Would you like more detailed troubleshooting steps?",
            "Would you like to explore alternative solutions?",
            "Would you like to schedule a follow-up?"
        ],
        "Translator": [
            "Would you like to translate something else?",
            "Would you like to learn more about our translation services?",
            "Would you like to try a different language?"
        ]
    }
    
    # Get relevant follow-up prompts based on the previous agent
    prompts = follow_up_prompts.get(previous_agent, [
        "Would you like more information about this topic?",
        "Would you like to explore something else?",
        "Would you like a more detailed explanation?"
    ])
    
    return prompts

# Define tools for quantum agents
def bell_state_tool():
    """Generate and analyze a Bell state"""
    result = run_qiskit_circuit()
    return format_detailed_response("BellState", "generate a Bell state", result)

def grover_tool():
    """Run Grover's search algorithm"""
    result = grover_search()
    return format_detailed_response("Grover", "explain Grover's algorithm", result)

def shor_tool():
    """Run Shor's factoring algorithm simulation"""
    result = shor_simulation()
    return format_detailed_response("Shor", "explain Shor's algorithm", result)

def azure_tool():
    """Azure Quantum information and integration"""
    result = run_azure_quantum()
    return format_detailed_response("Azure", "Azure Quantum capabilities", result)

# Define handoff tools
def make_handoff_tool(*, agent_name: str):
    """Create a tool that can return handoff via a Command"""
    tool_name = f"transfer_to_{agent_name}"
    
    def handoff_to_agent(
        state: Annotated[dict, InjectedState],
        tool_call_id: str,
    ):
        """Ask another agent for help."""
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": tool_name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            # navigate to another agent node in the PARENT graph
            goto=agent_name,
            graph=Command.PARENT,
            # This is the state update that the agent `agent_name` will see when it is invoked.
            # We're passing agent's FULL internal message history AND adding a tool message to make sure
            # the resulting chat history is valid.
            update={"messages": state["messages"] + [tool_message]},
        )
    
    return handoff_to_agent

# Human node for collecting user input
def human_node(state: MessagesState, config) -> Command[Literal["BellState", "Grover", "Shor", "Knowledge", "Azure", "QueryRouter", "ComplexSolver", "Translator"]]:
    """A node for collecting user input."""
    
    # Use interrupt to get user input
    print("\nEnter your query: ", end="")
    user_input = input()
    
    # Use QuantumRouter to analyze the query and route to appropriate agent
    router = QuantumRouter(["BellState", "Grover", "Shor", "Knowledge", "Azure", "QueryRouter", "ComplexSolver", "Translator"])
    rankings = router.rank_agents(user_input)
    
    # Get the highest ranked agent
    best_agent = rankings[0][0] if rankings else "Knowledge"
    
    # Print routing information
    print(f"\nQuantum Router selecting: {best_agent}")
    print(f"Rankings: {rankings}")
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "human",
                    "content": user_input,
                }
            ]
        },
        goto=best_agent,
    )

# Define agent nodes
def bell_state_agent(state: MessagesState) -> Command:
    """Bell State agent node"""
    response = bell_state_tool()
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]
        },
        goto="human"
    )

def grover_agent(state: MessagesState) -> Command:
    """Grover's algorithm agent node"""
    response = grover_tool()
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]
        },
        goto="human"
    )

def shor_agent(state: MessagesState) -> Command:
    """Shor's algorithm agent node"""
    response = shor_tool()
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]
        },
        goto="human"
    )

def knowledge_agent(state: MessagesState) -> Command:
    """Knowledge base agent node"""
    # Extract the last query from the message history
    last_message = None
    for msg in reversed(state.get("messages", [])):
        if hasattr(msg, "role") and msg.role == "human":
            last_message = msg
            break
        elif isinstance(msg, dict) and msg.get("role") == "human":
            last_message = msg
            break
    
    query = ""
    if last_message:
        if hasattr(last_message, "content"):
            query = last_message.content
        elif isinstance(last_message, dict):
            query = last_message.get("content", "")
    
    response = format_detailed_response("Knowledge", query)
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]
        },
        goto="human"
    )

def azure_agent(state: MessagesState) -> Command:
    """Azure Quantum agent node"""
    response = azure_tool()
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]
        },
        goto="human"
    )

def query_router_agent(state: MessagesState) -> Command:
    """Query router agent node"""
    # Extract the last query from the message history
    last_message = None
    for msg in reversed(state.get("messages", [])):
        if hasattr(msg, "role") and msg.role == "human":
            last_message = msg
            break
        elif isinstance(msg, dict) and msg.get("role") == "human":
            last_message = msg
            break
    
    query = ""
    if last_message:
        if hasattr(last_message, "content"):
            query = last_message.content
        elif isinstance(last_message, dict):
            query = last_message.get("content", "")
    
    # Create router instance
    router = QueryRoutingAgent("QueryRouter")
    result = router.perform_task(query)
    
    response = format_detailed_response("QueryRouter", query, result)
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]
        },
        goto="human"
    )

def complex_solver_agent(state: MessagesState) -> Command:
    """Complex problem solver agent node"""
    # Extract the last query from the message history
    last_message = None
    for msg in reversed(state.get("messages", [])):
        if hasattr(msg, "role") and msg.role == "human":
            last_message = msg
            break
        elif isinstance(msg, dict) and msg.get("role") == "human":
            last_message = msg
            break
    
    query = ""
    if last_message:
        if hasattr(last_message, "content"):
            query = last_message.content
        elif isinstance(last_message, dict):
            query = last_message.get("content", "")
    
    # Create solver instance
    solver = ComplexProblemSolver("ComplexSolver")
    result = solver.perform_task(query)
    
    response = format_detailed_response("ComplexSolver", query, result)
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]
        },
        goto="human"
    )

def translator_agent(state: MessagesState) -> Command:
    """Language translator agent node"""
    # Extract the last query from the message history
    last_message = None
    for msg in reversed(state.get("messages", [])):
        if hasattr(msg, "role") and msg.role == "human":
            last_message = msg
            break
        elif isinstance(msg, dict) and msg.get("role") == "human":
            last_message = msg
            break
    
    query = ""
    if last_message:
        if hasattr(last_message, "content"):
            query = last_message.content
        elif isinstance(last_message, dict):
            query = last_message.get("content", "")
    
    # Create translator instance
    translator = LanguageTranslator("Translator")
    result = translator.perform_task(query)
    
    response = format_detailed_response("Translator", query, result)
    
    return Command(
        update={
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]
        },
        goto="human"
    )

def main():
    print("Initializing Quantum-Enhanced LangGraph System...")
    
    # Create the StateGraph with MessagesState
    builder = StateGraph(MessagesState)
    
    # Add nodes for all agents
    builder.add_node("BellState", bell_state_agent)
    builder.add_node("Grover", grover_agent)
    builder.add_node("Shor", shor_agent)
    builder.add_node("Knowledge", knowledge_agent)
    builder.add_node("Azure", azure_agent)
    builder.add_node("QueryRouter", query_router_agent)
    builder.add_node("ComplexSolver", complex_solver_agent)
    builder.add_node("Translator", translator_agent)
    
    # Add human node for collecting input
    builder.add_node("human", human_node)
    
    # Add edges from START to Knowledge (default entry point)
    builder.add_edge(START, "Knowledge")
    
    # Create a graph without checkpointer
    graph = builder.compile()
    
    print("\nQuantum-Enhanced LangGraph Chat System")
    print("=====================================")
    print("Example queries:")
    print("1. Can you explain Bell states?")
    print("2. How does Grover's algorithm work?")
    print("3. What is the capital of France?")
    print("4. My internet connection keeps dropping every few minutes.")
    print("5. I need help with my bill, there's an extra charge I don't recognize.")
    print("6. Can you translate this to Spanish: 'I need help with my account password'?")
    print("Type 'exit' to quit at any prompt.\n")
    
    # Create initial state
    state = {"messages": []}
    
    # Run the graph
    try:
        # Use the stream method with standard state
        for s in graph.stream(state):
            # Allow graceful exit
            if s.get("messages", []) and s["messages"][-1].get("content", "").lower() == "exit":
                print("Exiting chat system. Goodbye!")
                break
            
            # Display conversation
            if s.get("messages", []) and s["messages"][-1].get("role") == "assistant":
                print("\nAssistant:", s["messages"][-1]["content"])
                
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting chat system. Goodbye!")
    
if __name__ == "__main__":
    main() 