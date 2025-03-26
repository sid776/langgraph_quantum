from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import numpy as np
import re

class QuantumRouter:
    def __init__(self, agents):
        self.agents = agents if isinstance(agents, (list, tuple)) else list(agents)
        self.n_agents = len(self.agents)
        self.n_qubits = int(np.ceil(np.log2(self.n_agents)))
        
        # Define knowledge patterns
        self.knowledge_patterns = [
            r"what is",
            r"who is",
            r"where is",
            r"when",
            r"why",
            r"how",
            r"can you tell me",
            r"explain",
            r"capital of",
            r"country",
            r"planet",
            r"element",
            r"largest",
            r"tallest",
            r"biggest"
        ]
        
        # Define quantum computing patterns
        self.quantum_patterns = [
            r"qubit",
            r"quantum",
            r"superposition",
            r"entanglement",
            r"grover",
            r"shor",
            r"algorithm",
            r"circuit",
            r"factoring",
            r"search"
        ]
        
        # Define telecom routing patterns
        self.routing_patterns = [
            r"route",
            r"direct",
            r"transfer",
            r"connect",
            r"agent",
            r"department",
            r"specialist",
            r"appropriate",
            r"right person"
        ]
        
        # Define complex problem patterns
        self.complex_problem_patterns = [
            r"intermittent",
            r"keeps dropping",
            r"inconsistent",
            r"unreliable",
            r"multiple issues",
            r"complex",
            r"several problems",
            r"combination of",
            r"both.*and",
            r"not working properly",
            r"troubleshoot",
            r"diagnostic",
            r"unexpected",
            r"unusual",
            r"weird"
        ]
        
        # Define translation patterns
        self.translation_patterns = [
            r"translate",
            r"spanish",
            r"french",
            r"language",
            r"en español",
            r"en français",
            r"habla",
            r"parle"
        ]
        
        # Define telecom billing patterns
        self.billing_patterns = [
            r"bill",
            r"payment",
            r"charge",
            r"invoice",
            r"subscription",
            r"plan",
            r"cost",
            r"price",
            r"fee",
            r"credit",
            r"refund",
            r"overcharge"
        ]
        
        # Define technical issues patterns
        self.technical_patterns = [
            r"internet",
            r"connection",
            r"wifi",
            r"speed",
            r"router",
            r"signal",
            r"device",
            r"data",
            r"outage",
            r"slow",
            r"down",
            r"not working"
        ]
    
    def analyze_query(self, query):
        """Analyze a query to determine its category"""
        query_lower = query.lower()
        
        # Check for pattern matches
        knowledge_matches = sum(1 for pattern in self.knowledge_patterns if re.search(pattern, query_lower))
        quantum_matches = sum(1 for pattern in self.quantum_patterns if re.search(pattern, query_lower))
        routing_matches = sum(1 for pattern in self.routing_patterns if re.search(pattern, query_lower))
        complex_matches = sum(1 for pattern in self.complex_problem_patterns if re.search(pattern, query_lower))
        translation_matches = sum(1 for pattern in self.translation_patterns if re.search(pattern, query_lower))
        billing_matches = sum(1 for pattern in self.billing_patterns if re.search(pattern, query_lower))
        technical_matches = sum(1 for pattern in self.technical_patterns if re.search(pattern, query_lower))
        
        # Determine the primary category
        categories = {
            "Knowledge": knowledge_matches,
            "Quantum": quantum_matches,
            "Routing": routing_matches,
            "Complex": complex_matches,
            "Translation": translation_matches,
            "Billing": billing_matches,
            "Technical": technical_matches
        }
        
        # Return the highest matching category
        primary_category = max(categories.items(), key=lambda x: x[1])
        
        # Consider telecom relevance for category decision
        telecom_relevance = routing_matches + complex_matches + translation_matches + billing_matches + technical_matches
        
        # If this has telecom relevance, determine which telecom agent is appropriate
        if telecom_relevance > 0:
            # Billing issues should go to the ComplexSolver
            if billing_matches > 0 and "ComplexSolver" in self.agents:
                return "ComplexSolver", primary_category[0]
                
            # Technical issues should go to the ComplexSolver
            if technical_matches > 0 and "ComplexSolver" in self.agents:
                return "ComplexSolver", primary_category[0]
                
            # Translation queries
            if translation_matches > 0 and "Translator" in self.agents:
                return "Translator", primary_category[0]
                
            # Complex problems
            if complex_matches > 0 and "ComplexSolver" in self.agents:
                return "ComplexSolver", primary_category[0]
                
            # Routing questions
            if routing_matches > 0 and "QueryRouter" in self.agents:
                return "QueryRouter", primary_category[0]
                
            # Default to routing agent for general telecom queries
            if "QueryRouter" in self.agents:
                return "QueryRouter", primary_category[0]
        
        # For non-telecom queries, determine if it's knowledge or quantum
        if knowledge_matches > 0 and knowledge_matches >= quantum_matches:
            if "Knowledge" in self.agents:
                return "Knowledge", primary_category[0]
        
        # For quantum computing related queries
        if quantum_matches > 0:
            # Check for specific quantum topics
            if "grover" in query_lower and "Grover" in self.agents:
                return "Grover", primary_category[0]
            elif "shor" in query_lower and "Shor" in self.agents:
                return "Shor", primary_category[0]
            elif "bell" in query_lower and "BellState" in self.agents:
                return "BellState", primary_category[0]
            elif "azure" in query_lower and "Azure" in self.agents:
                return "Azure", primary_category[0]
        
        # Default to a generic quantum agent if available
        for agent in ["BellState", "Grover", "Shor", "Azure"]:
            if agent in self.agents:
                return agent, primary_category[0]
                
        # Final fallback to Knowledge
        if "Knowledge" in self.agents:
            return "Knowledge", primary_category[0]
            
        # If nothing else, return the first available agent
        return self.agents[0], primary_category[0]
        
    def rank_agents(self, query: str, task_name=None, task_id=None):
        # Add fallback if query is blank or None
        if not query or query.strip() == "":
            query = "default knowledge query"  # Fallback value
        
        # Analyze query to determine category
        selected_agent, primary_category = self.analyze_query(query)
        
        # Store the query globally as a class attribute that Knowledge agent can access
        if not hasattr(QuantumRouter, 'current_query'):
            setattr(QuantumRouter, 'current_query', query)
        else:
            QuantumRouter.current_query = query
        
        # Create rankings based on category match
        rankings = []
        scores = {}
        
        # Initialize all agents with base score
        for agent in self.agents:
            scores[agent] = 0.1
        
        # Check for billing patterns
        query_lower = query.lower()
        if any(re.search(pattern, query_lower) for pattern in self.billing_patterns):
            if "ComplexSolver" in self.agents:
                scores["ComplexSolver"] = scores.get("ComplexSolver", 0) + 1.0
                
        # Check for technical patterns
        if any(re.search(pattern, query_lower) for pattern in self.technical_patterns):
            if "ComplexSolver" in self.agents:
                scores["ComplexSolver"] = scores.get("ComplexSolver", 0) + 1.0
        
        # Check for translation patterns
        if any(re.search(pattern, query_lower) for pattern in self.translation_patterns):
            if "Translator" in self.agents:
                scores["Translator"] = scores.get("Translator", 0) + 1.0
        
        # Check for complex problem patterns
        if any(re.search(pattern, query_lower) for pattern in self.complex_problem_patterns):
            if "ComplexSolver" in self.agents:
                scores["ComplexSolver"] = scores.get("ComplexSolver", 0) + 0.8
        
        # Check for routing patterns
        if any(re.search(pattern, query_lower) for pattern in self.routing_patterns):
            if "QueryRouter" in self.agents:
                scores["QueryRouter"] = scores.get("QueryRouter", 0) + 0.8
        
        # Check for knowledge patterns
        if any(re.search(pattern, query_lower) for pattern in self.knowledge_patterns):
            if "Knowledge" in self.agents:
                scores["Knowledge"] = scores.get("Knowledge", 0) + 0.5
        
        # Check for quantum computing patterns
        if any(re.search(pattern, query_lower) for pattern in self.quantum_patterns):
            if "grover" in query_lower and "Grover" in self.agents:
                scores["Grover"] = scores.get("Grover", 0) + 0.9
            elif "shor" in query_lower and "Shor" in self.agents:
                scores["Shor"] = scores.get("Shor", 0) + 0.9
            elif "bell" in query_lower and "BellState" in self.agents:
                scores["BellState"] = scores.get("BellState", 0) + 0.9
            elif "azure" in query_lower and "Azure" in self.agents:
                scores["Azure"] = scores.get("Azure", 0) + 0.9
            else:
                # Distribute scores across quantum agents
                for agent in ["BellState", "Grover", "Shor", "Azure"]:
                    if agent in self.agents:
                        scores[agent] = scores.get(agent, 0) + 0.3
        
        # Boost the selected agent
        if selected_agent in scores:
            scores[selected_agent] = max(scores[selected_agent], 1.0)
        
        # Convert scores to rankings
        for agent, score in scores.items():
            if agent in self.agents:
                rankings.append((agent, score * 100))  # Scale up for display
        
        # Sort rankings by score
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        return rankings

    @classmethod
    def get_current_query(cls):
        """Helper method for Knowledge agent to get the current query"""
        if hasattr(cls, 'current_query'):
            return cls.current_query
        return "default knowledge query"

    # Remove create_quantum_circuit method entirely
    # Remove handle_grover_task and handle_translator_task functions 