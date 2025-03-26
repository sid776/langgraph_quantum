import json
import re
from typing import Dict, List, Any, Union, Optional

# Mock Agent class
class Agent:
    def __init__(self, name: str, skill: str):
        self.name = name
        self.skill = skill
        self.tools = {}
    
    def add_tool(self, name: str, function):
        self.tools[name] = function
    
    def perform_task(self, query=None):
        print(f"\n{self.name} is performing task: {self.skill}")
        if query:
            print(f"Working on query: {query}")
        
        result = f"{self.name} processed the task successfully"
        return result

# Telecom Agents
class QueryRoutingAgent(Agent):
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

class ComplexProblemSolver(Agent):
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

class LanguageTranslator(Agent):
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

# Quantum router mock
class QuantumRouter:
    def __init__(self, agents):
        self.agents = agents
        
        # Pre-defined patterns for matching query types
        self.patterns = {
            "billing": ["bill", "payment", "charge", "invoice", "subscription", "plan", "cost", "price", "fee"],
            "technical": ["internet", "connection", "wifi", "speed", "router", "signal", "device", "data", "outage", "slow", "down"],
            "complex": ["intermittent", "keeps dropping", "inconsistent", "unreliable", "multiple issues", "complex"],
            "translation": ["translate", "spanish", "french", "language", "en español", "en français"],
            "quantum": ["qubit", "quantum", "superposition", "entanglement", "grover", "shor", "algorithm", "circuit"]
        }
    
    def rank_agents(self, query):
        query_lower = query.lower()
        
        # Initialize scores
        scores = {agent_name: 100 for agent_name in self.agents}
        
        # Calculate pattern matches
        if any(term in query_lower for term in self.patterns["billing"]):
            scores["QueryRouter"] = scores.get("QueryRouter", 0) + 500
            
        if any(term in query_lower for term in self.patterns["technical"]):
            scores["ComplexSolver"] = scores.get("ComplexSolver", 0) + 400
            
        if any(term in query_lower for term in self.patterns["complex"]):
            scores["ComplexSolver"] = scores.get("ComplexSolver", 0) + 600
            
        if any(term in query_lower for term in self.patterns["translation"]):
            scores["Translator"] = scores.get("Translator", 0) + 700
            
        if any(term in query_lower for term in self.patterns["quantum"]):
            if "BellState" in self.agents:
                scores["BellState"] = scores.get("BellState", 0) + 300
            if "Grover" in self.agents:
                scores["Grover"] = scores.get("Grover", 0) + 300
                
        # Knowledge agent gets higher score for general questions
        if re.search(r"(what|who|when|where|why|how)", query_lower):
            scores["Knowledge"] = scores.get("Knowledge", 0) + 400
        
        # Convert to list of tuples and sort
        rankings = [(agent, score) for agent, score in scores.items()]
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        return rankings

# Supervisor
class Supervisor:
    def __init__(self):
        self.agents = {}
        self.router = None
    
    def add_agent(self, agent):
        agent_name = agent.name
        self.agents[agent_name] = agent
    
    def process_query(self, query):
        # Initialize router if not already done
        if not self.router:
            self.router = QuantumRouter(self.agents)
        
        # Get agent rankings
        rankings = self.router.rank_agents(query)
        best_agent = rankings[0][0]
        
        print("\nAgent Rankings based on Quantum Router:")
        for agent, score in rankings:
            print(f"- {agent}: {score} votes")
        
        return best_agent, rankings

# State Graph
class StateGraph:
    def __init__(self):
        self.nodes = {}
        self.entry_point = None
        self.edges = {}
    
    def add_node(self, name, func):
        self.nodes[name] = func
    
    def set_entry_point(self, name):
        self.entry_point = name
    
    def add_edge(self, source, target):
        if source not in self.edges:
            self.edges[source] = []
        self.edges[source].append(target)
    
    def add_conditional_edges(self, source, router, destinations):
        self.conditional_edges = {
            "source": source,
            "router": router,
            "destinations": destinations
        }
    
    def compile(self):
        return self
    
    def invoke(self, state):
        # Start with the entry point
        current_node = self.entry_point
        
        # Execute the entry point node
        state = self.nodes[current_node](state)
        
        # Follow the conditional edge
        if hasattr(self, 'conditional_edges') and current_node == self.conditional_edges["source"]:
            next_node = self.conditional_edges["router"](state)
            if next_node in self.conditional_edges["destinations"]:
                state = self.nodes[next_node](state)
        
        return state

# Create a team graph
def create_team_graph(supervisor, agents):
    # Create a graph
    graph = StateGraph()
    
    # Add supervisor node
    def supervisor_node(state):
        query = state.get("task", "")
        best_agent, rankings = supervisor.process_query(query)
        
        return {
            "messages": state.get("messages", []) + [{
                "content": f"Supervisor routing to: {best_agent}",
                "role": "supervisor"
            }],
            "current_agent": best_agent,
            "task": query,
            "status": "RUNNING"
        }
    
    # Add agent nodes
    def create_agent_node(agent_name):
        def agent_node(state):
            agent = agents[agent_name]
            query = state.get("task", "")
            
            # Call perform_task with the query
            result = agent.perform_task(query)
            
            # Format the result
            response_content = f"Agent {agent_name} completed task"
            if result:
                if isinstance(result, dict):
                    response_content = f"Agent {agent_name} result: {json.dumps(result, indent=2)}"
                else:
                    response_content = f"Agent {agent_name} result: {result}"
            
            return {
                "messages": state.get("messages", []) + [{
                    "content": response_content,
                    "role": "agent"
                }],
                "current_agent": agent_name,
                "task": state.get("task", ""),
                "status": "COMPLETED"
            }
        return agent_node
    
    # Add nodes to the graph
    graph.add_node("supervisor", supervisor_node)
    for agent_name in agents:
        graph.add_node(agent_name, create_agent_node(agent_name))
    
    # Define the routing function
    def conditional_edge(state):
        return state["current_agent"]
    
    # Add edges
    agent_names = list(agents.keys())
    graph.add_conditional_edges(
        source="supervisor",
        router=conditional_edge,
        destinations=agent_names
    )
    
    # Connect router to agents
    for agent_name in agents:
        graph.add_edge("router", agent_name)
    
    # Add end node
    def end_node(state):
        # Just return the state
        return state
    
    graph.add_node("end", end_node)
    
    # Add edges from each agent to end
    for agent_name in agents:
        graph.add_edge(agent_name, "end")
    
    # Set entry point
    graph.set_entry_point("supervisor")
    
    return graph.compile()

# Run team
def run_team(app, query: str):
    initial_state = {
        "messages": [],
        "current_agent": None,
        "task": query,
        "status": "RUNNING"
    }
    result = app.invoke(initial_state)
    return result

def main():
    print("Telecom Agents Demo")
    print("==================\n")
    
    # Create agents
    agents = {}
    
    query_router = QueryRoutingAgent()
    agents["QueryRouter"] = query_router
    
    complex_solver = ComplexProblemSolver()
    agents["ComplexSolver"] = complex_solver
    
    language_translator = LanguageTranslator()
    agents["Translator"] = language_translator
    
    knowledge_agent = Agent("Knowledge", "General Knowledge & Common Sense")
    agents["Knowledge"] = knowledge_agent
    
    # Create supervisor and register agents
    supervisor = Supervisor()
    for agent_name, agent in agents.items():
        supervisor.add_agent(agent)
    
    # Create team graph
    app = create_team_graph(supervisor, agents)
    
    print("Welcome to Telecom Support Chat! How may I assist you today?")
    print("Example queries:")
    print("1. I need help with my bill, who should I talk to?")
    print("2. My internet connection keeps dropping every few minutes, especially when it rains.")
    print("3. Can you translate this to Spanish: 'I need help with my account password'")
    print("4. What's the capital of France? (Knowledge)")
    print("Type 'exit' to quit.\n")
    
    # Chat history
    chat_history = []
    current_context = {"agent": None, "issue_type": None}
    
    # Initial greeting
    print("Agent: Hello! I'm your telecom support assistant. How can I help you today?")
    
    while True:
        # Get user input
        query = input("Customer: ")
        if query.lower() == 'exit':
            break
        
        # Add to chat history
        chat_history.append({"role": "customer", "content": query})
        
        # Process the query through our team
        result = run_team(app, query)
        
        # Extract the agent response from the result
        agent_name = result["current_agent"]
        messages = result["messages"]
        
        # Track conversation context
        if current_context["agent"] != agent_name:
            current_context["agent"] = agent_name
            if agent_name == "ComplexSolver":
                current_context["issue_type"] = "technical" if any(term in query.lower() for term in ["internet", "connection", "wifi"]) else "billing"
        
        # Get the latest agent message
        agent_message = None
        for msg in messages:
            if msg["role"] == "agent":
                agent_message = msg["content"]
        
        # Handle different agent types to create more natural responses
        if agent_name == "ComplexSolver":
            recommendations = None
            if agent_message and "result" in agent_message:
                try:
                    data = json.loads(agent_message.split("result: ")[1])
                    if "recommendations" in data:
                        recommendations = data["recommendations"]
                        current_context["recommendations"] = recommendations
                        current_context["issue"] = data.get("issue", "service issue")
                except:
                    pass
            
            if recommendations:
                response = f"Agent: I understand you're having an issue with {data.get('issue', 'your service')}. Based on my analysis, here are my recommendations:\n"
                for i, rec in enumerate(recommendations, 1):
                    response += f"{i}. {rec}\n"
                response += "\nIs there anything specific from these recommendations you'd like me to explain further? Or do you have other questions about your service?"
            else:
                issue_type = current_context.get("issue_type", "service")
                response = f"Agent: I understand you're experiencing a complex {issue_type} issue. I've analyzed the details and can help you troubleshoot this step by step. Could you tell me when you first noticed this problem, or do you have any specific questions about it?"
        
        elif agent_name == "Translator":
            translation = None
            if agent_message and "result" in agent_message:
                try:
                    data = json.loads(agent_message.split("result: ")[1])
                    if "translated_text" in data:
                        translation = data["translated_text"]
                except:
                    pass
            
            if translation:
                response = f"Agent: Here's your translation: \"{translation}\". Would you like me to translate anything else for you today? Or do you need help with something else?"
            else:
                response = f"Agent: I've processed your translation request. Is there anything else you'd like me to translate for you? I can also help with other telecom-related issues if needed."
        
        elif agent_name == "QueryRouter":
            routed_to = None
            if agent_message and "result" in agent_message:
                try:
                    data = json.loads(agent_message.split("result: ")[1])
                    if "routed_to" in data:
                        routed_to = data["routed_to"]
                        current_context["department"] = routed_to
                except:
                    pass
            
            if routed_to:
                response = f"Agent: Based on your question, I'll connect you with our {routed_to.upper()} department. They specialize in {data.get('category_description', 'this type of inquiry')}. What specific {routed_to} question can I help you with today? Or is there something else you'd like to know?"
            else:
                response = f"Agent: I'll help direct your inquiry to the right department. Could you provide a bit more detail about what you need help with today? For example, is this about billing, technical issues, or something else?"
        
        elif agent_name == "Knowledge":
            if agent_message:
                response = f"Agent: {agent_message} Is there anything else you'd like to know about this topic? I'm happy to provide more information."
            else:
                response = "Agent: Based on my knowledge, I can answer that for you. Do you have any follow-up questions, or would you like information on another topic?"
        
        else:
            if agent_message:
                response = f"Agent: {agent_message} Is there anything else I can help you with today?"
            else:
                response = "Agent: I understand your request and I'm here to help. Do you have any other questions or concerns I can address for you?"
        
        print(response)
        
        # Add to chat history
        chat_history.append({"role": "agent", "content": response})
        
    print("\nThank you for using Telecom Support Chat. Have a great day!")

if __name__ == "__main__":
    main() 