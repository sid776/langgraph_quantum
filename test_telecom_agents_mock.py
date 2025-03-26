import sys
import os
import json

# Make sure the module directories are in the path
sys.path.append(os.path.abspath('.'))

# First, let's create simple mock modules to replace the quantum libraries
class MockQuantumRouter:
    def __init__(self, agents):
        self.agents = agents
    
    def rank_agents(self, query):
        # Return query routing for billing-related questions
        if "bill" in query.lower() or "payment" in query.lower():
            return [("QueryRouter", 500), ("Knowledge", 200)]
        # Return complex solver for technical issues
        elif "internet" in query.lower() or "connection" in query.lower():
            return [("ComplexSolver", 600), ("Knowledge", 150)]
        # Return translator for translation requests
        elif "translate" in query.lower() or "spanish" in query.lower():
            return [("Translator", 700), ("Knowledge", 100)]
        # Default to knowledge for other queries
        else:
            return [("Knowledge", 400), ("QueryRouter", 300)]

# Mock the Agent class from langgraph_project.agent
class MockAgent:
    def __init__(self, name, skill):
        self.name = name
        self.skill = skill
        self.tools = {}
    
    def add_tool(self, name, function):
        self.tools[name] = function
    
    def perform_task(self, query=None):
        print(f"\n{self.name} is performing task: {self.skill}")
        if query:
            print(f"Working on query: {query}")
        print("Tools available:", list(self.tools.keys()))
        
        result = f"{self.name} processed the task successfully"
        return result

# Now let's create our mock telecom agents with simpler functionality

class QueryRoutingAgent(MockAgent):
    def __init__(self, name="Query Router"):
        super().__init__(name=name, skill="Routing customer queries to the appropriate agent")
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
        
        # Simple keyword matching to determine the best category
        query_lower = query.lower()
        best_category = "general"
        
        if any(word in query_lower for word in ["bill", "payment", "charge", "cost", "price"]):
            best_category = "billing"
        elif any(word in query_lower for word in ["internet", "connection", "wifi", "router", "slow"]):
            best_category = "technical"
        elif any(word in query_lower for word in ["password", "account", "login", "profile"]):
            best_category = "account"
        elif any(word in query_lower for word in ["plan", "service", "upgrade", "feature"]):
            best_category = "service"
        elif any(word in query_lower for word in ["international", "roaming", "abroad", "overseas"]):
            best_category = "international"
        
        result = {
            "query": query,
            "routed_to": best_category,
            "category_description": self.categories.get(best_category, "General inquiry"),
            "confidence": "high" if any(keyword in query_lower for keyword in ["bill", "internet", "account", "plan", "international"]) else "medium"
        }
        
        print(f"✅ Query routed to: {best_category.upper()} department")
        return result

class ComplexProblemSolver(MockAgent):
    def __init__(self, name="Complex Problem Solver"):
        super().__init__(name=name, skill="Analyzes and resolves complex issues with multiple interdependent factors")
        self.issue_types = {
            "intermittent_connection": {
                "factors": ["router_placement", "device_compatibility", "network_congestion", "weather_conditions", "infrastructure"],
                "solutions": {
                    "router_placement": "Reposition router for better signal distribution",
                    "device_compatibility": "Update device drivers or consider compatible equipment",
                    "network_congestion": "Suggest off-peak usage or bandwidth optimization",
                    "weather_conditions": "Acknowledge temporary nature and suggest alternatives",
                    "infrastructure": "Schedule technician visit to check local infrastructure"
                }
            },
            "billing_discrepancy": {
                "factors": ["promotion_expiration", "service_changes", "usage_patterns", "billing_cycle", "taxes_fees"],
                "solutions": {
                    "promotion_expiration": "Explain promotion end date and offer current promotions",
                    "service_changes": "Review recent service modifications affecting billing",
                    "usage_patterns": "Analyze usage patterns that caused excess charges",
                    "billing_cycle": "Explain prorated charges or billing cycle changes",
                    "taxes_fees": "Detail regulatory fees or tax changes affecting bill"
                }
            }
        }
    
    def perform_task(self, query):
        print(f"\n🧩 {self.name} analyzing complex problem...")
        print(f"❓ Query: {query}")
        
        # Identify issue type based on keywords
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["internet", "connection", "wifi", "drops", "intermittent"]):
            issue_type = "intermittent_connection"
        elif any(word in query_lower for word in ["bill", "charge", "payment", "cost"]):
            issue_type = "billing_discrepancy"
        else:
            issue_type = "intermittent_connection"  # Default
        
        # Identify relevant factors
        factors = self.issue_types[issue_type]["factors"]
        top_factors = []
        
        for factor in factors:
            factor_lower = factor.lower().replace("_", " ")
            if factor_lower in query_lower or any(word in factor_lower for word in query_lower.split()):
                top_factors.append(factor)
        
        # If no factors match, select the first 3
        if not top_factors:
            top_factors = factors[:3]
        
        # Get solutions for the top factors
        solutions = self.issue_types[issue_type]["solutions"]
        top_solutions = {factor: solutions[factor] for factor in top_factors}
        
        # Format the issue name for readability
        issue_readable = issue_type.replace("_", " ").title()
        
        print(f"\nComplex Problem Analysis:")
        print(f"Identified Issue: {issue_readable}")
        print(f"Key Factors:")
        for factor in top_factors:
            factor_readable = factor.replace("_", " ").title()
            print(f"- {factor_readable}: {solutions[factor]}")
        
        result = {
            "issue": issue_readable,
            "key_factors": top_factors,
            "recommendations": [solutions[factor] for factor in top_factors]
        }
        
        return result

class LanguageTranslator(MockAgent):
    def __init__(self, name="Language Translator"):
        super().__init__(name=name, skill="Provides real-time translation services for global customer support")
        self.translations = {
            "english_spanish": {
                "hello": "hola",
                "help": "ayuda",
                "need": "necesito",
                "account": "cuenta",
                "password": "contraseña",
                "internet": "internet",
                "problem": "problema",
                "thank you": "gracias",
                "service": "servicio",
                "please": "por favor",
                "my": "mi",
                "with": "con",
                "i": "yo",
                "for": "para",
                "the": "el",
                "this": "esto"
            }
        }
    
    def perform_task(self, query, source_lang="english", target_lang=None):
        print(f"\n🌐 {self.name} translating content...")
        print(f"❓ Original query: {query}")
        
        # Detect target language from query
        if "spanish" in query.lower() or "español" in query.lower():
            target_lang = "spanish"
        else:
            target_lang = "spanish"  # Default
        
        # Extract the text to translate (after "translate" or "to Spanish")
        if "translate" in query.lower():
            # Extract text after "translate"
            text_parts = query.lower().split("translate", 1)
            if len(text_parts) > 1:
                text_to_translate = text_parts[1].strip()
                # If there's a colon, extract after the colon
                if ":" in text_to_translate:
                    text_to_translate = text_to_translate.split(":", 1)[1].strip().strip('"\'')
            else:
                text_to_translate = query
        else:
            text_to_translate = query
        
        # Simple word-by-word translation
        words = text_to_translate.lower().split()
        translated_words = []
        
        for word in words:
            clean_word = word.strip('.,?!:;()"\'')
            if clean_word in self.translations["english_spanish"]:
                translated_words.append(self.translations["english_spanish"][clean_word])
            else:
                translated_words.append(clean_word)
        
        translated_text = " ".join(translated_words)
        
        # Prepare the response
        print(f"\nLanguage Translation ({source_lang.title()} to {target_lang.title()}):")
        print(f"Original: {text_to_translate}")
        print(f"Translated: {translated_text}")
        
        result = {
            "source_language": source_lang,
            "target_language": target_lang,
            "original_text": text_to_translate,
            "translated_text": translated_text
        }
        
        return result

def main():
    print("Testing Mock Telecom Agents...\n")
    
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
    print(f"\nResult: {json.dumps(routing_result, indent=2)}")
    
    print("\n===== Testing Complex Problem Solver =====")
    complex_result = complex_solver.perform_task(complex_query)
    print(f"\nResult: {json.dumps(complex_result, indent=2)}")
    
    print("\n===== Testing Language Translator =====")
    translation_result = translator.perform_task(translation_query)
    print(f"\nResult: {json.dumps(translation_result, indent=2)}")
    
if __name__ == "__main__":
    main() 