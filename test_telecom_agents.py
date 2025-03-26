import sys
import os

# Make sure the module directories are in the path
sys.path.append(os.path.abspath('.'))

from langgraph_project.telecom_agents import QueryRoutingAgent, ComplexProblemSolver, LanguageTranslator

def main():
    print("Testing Telecom Agents...\n")
    
    # Create agents
    query_router = QueryRoutingAgent()
    complex_solver = ComplexProblemSolver()
    translator = LanguageTranslator()
    
    # Test queries
    routing_query = "I need help with my bill, who should I talk to?"
    complex_query = "My internet connection keeps dropping every few minutes, especially when it rains."
    translation_query = "Can you translate this to Spanish: 'I need help with my account password'"
    
    # Test each agent
    print("\n===== Testing Query Routing Agent =====")
    routing_result = query_router.perform_task(routing_query)
    print(f"\nQuery: {routing_query}")
    print(f"Result: {routing_result}")
    
    print("\n===== Testing Complex Problem Solver =====")
    complex_result = complex_solver.perform_task(complex_query)
    print(f"\nQuery: {complex_query}")
    print(f"Result: {complex_result}")
    
    print("\n===== Testing Language Translator =====")
    translation_result = translator.perform_task(translation_query)
    print(f"\nQuery: {translation_query}")
    print(f"Result: {translation_result}")
    
if __name__ == "__main__":
    main() 