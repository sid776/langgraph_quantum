from langgraph_project.agent import Agent
from langgraph_project.telecom_tools import quantum_route_query, solve_complex_problem, translate_content

class QueryRoutingAgent(Agent):
    """
    An agent that uses quantum-powered routing to direct customer queries
    to the most appropriate specialized agent.
    """
    def __init__(self, name="Query Router"):
        super().__init__(name=name, skill="Intelligently routes customer queries to the most appropriate agent using quantum algorithms")
        self.categories = {
            "billing": "Handles billing inquiries, payment issues, and plan changes",
            "technical": "Resolves technical issues with internet, devices, and connections",
            "account": "Manages account information, passwords, and personal details",
            "service": "Assists with service plans, upgrades, and feature changes",
            "international": "Specializes in international services, roaming, and overseas support"
        }
    
    def perform_task(self, query):
        print(f"\n🔄 {self.name} analyzing query...")
        print(f"❓ Query: {query}")
        
        # Use quantum routing to determine the best category
        best_category = quantum_route_query(query)
        
        result = {
            "query": query,
            "routed_to": best_category,
            "category_description": self.categories.get(best_category, "General inquiry"),
            "confidence": "high" if any(keyword in query.lower() for keyword in ["bill", "internet", "account", "plan", "international"]) else "medium"
        }
        
        print(f"✅ Query routed to: {best_category.upper()} department")
        return result


class ComplexProblemSolver(Agent):
    """
    An agent that solves multi-parameter customer issues involving
    interdependent systems using quantum-inspired algorithms.
    """
    def __init__(self, name="Complex Problem Solver"):
        super().__init__(name=name, skill="Analyzes and resolves complex issues with multiple interdependent factors")
        self.issue_types = {
            "intermittent_connection": "Problems with inconsistent internet or service connection",
            "billing_discrepancy": "Issues with unexpected charges or billing confusion",
            "device_compatibility": "Problems with devices working properly with our services"
        }
    
    def perform_task(self, query):
        print(f"\n🧩 {self.name} analyzing complex problem...")
        print(f"❓ Query: {query}")
        
        # Use quantum-inspired problem solving
        solution = solve_complex_problem(query)
        
        # Format the response
        response = {
            "query": query,
            "issue_type": solution["issue"],
            "key_factors": solution["factors"],
            "recommendations": [solution["solutions"][factor] for factor in solution["factors"]]
        }
        
        print(f"✅ Solution found for: {solution['issue']}")
        return response


class LanguageTranslator(Agent):
    """
    An agent that enhances global customer support with quantum-accelerated translation.
    """
    def __init__(self, name="Language Translator"):
        super().__init__(name=name, skill="Provides real-time translation services for global customer support")
        self.supported_languages = ["spanish", "french"]
    
    def perform_task(self, query, source_lang="english", target_lang=None):
        print(f"\n🌐 {self.name} translating content...")
        print(f"❓ Original query: {query}")
        
        # Detect target language from query if not specified
        if target_lang is None:
            if "spanish" in query.lower() or "español" in query.lower():
                target_lang = "spanish"
            elif "french" in query.lower() or "français" in query.lower():
                target_lang = "french"
            else:
                target_lang = "spanish"  # Default
        
        # Perform quantum-enhanced translation
        translation_result = translate_content(query, source_lang, target_lang)
        
        # Format the response
        response = {
            "original_query": query,
            "translated_query": translation_result["translated_text"],
            "source_language": translation_result["source_language"],
            "target_language": translation_result["target_language"]
        }
        
        print(f"✅ Translation complete: {translation_result['source_language']} → {translation_result['target_language']}")
        return response 