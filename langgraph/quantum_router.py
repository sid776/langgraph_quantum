from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import numpy as np
import re

class QuantumRouter:
    def __init__(self, agents):
        self.agents = agents
        self.n_agents = len(agents)
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
    
    def analyze_query(self, query):
        """Analyze a query to determine if it's likely a knowledge question"""
        query_lower = query.lower()
        
        # Check for knowledge patterns
        knowledge_matches = sum(1 for pattern in self.knowledge_patterns if re.search(pattern, query_lower))
        
        # Check for quantum patterns
        quantum_matches = sum(1 for pattern in self.quantum_patterns if re.search(pattern, query_lower))
        
        # Determine if this is a knowledge question
        is_knowledge_question = knowledge_matches > 0 and knowledge_matches > quantum_matches
        
        return is_knowledge_question
        
    def rank_agents(self, query: str):
        # First check if this is a general knowledge question
        is_knowledge_question = self.analyze_query(query)
        
        # Create quantum circuit for superposition and measurement
        qr = QuantumRegister(self.n_qubits)
        cr = ClassicalRegister(self.n_qubits)
        qc = QuantumCircuit(qr, cr)
        
        # Create superposition
        qc.h(range(self.n_qubits))
        
        # Apply bias if this is a knowledge question
        if is_knowledge_question and "Knowledge" in self.agents:
            # Find the index of the Knowledge agent
            knowledge_idx = list(self.agents).index("Knowledge")
            
            # Convert to binary representation
            knowledge_bin = format(knowledge_idx, f'0{self.n_qubits}b')
            
            # Apply X gates to qubits that should be 0 in the target state
            for i in range(self.n_qubits):
                if knowledge_bin[i] == '0':
                    qc.x(i)
            
            # Apply a phase shift to increase probability
            qc.h(self.n_qubits-1)
            qc.mct(list(range(self.n_qubits-1)), self.n_qubits-1)
            qc.h(self.n_qubits-1)
            
            # Undo the X gates
            for i in range(self.n_qubits):
                if knowledge_bin[i] == '0':
                    qc.x(i)
        else:
            # Apply regular phase rotations based on query relevance
            for i in range(self.n_qubits):
                # Calculate relevance score (simplified)
                relevance = sum(1 for agent in self.agents if agent.lower() in query.lower())
                angle = (relevance * np.pi) / self.n_agents
                qc.rz(angle, i)
        
        qc.measure(range(self.n_qubits), range(self.n_qubits))
        
        # Execute
        simulator = Aer.get_backend('qasm_simulator')
        job = simulator.run(qc, shots=1000)
        result = job.result()
        counts = result.get_counts(qc)
        
        # Convert results to agent rankings
        rankings = []
        for state, count in counts.items():
            agent_idx = int(state, 2) % self.n_agents
            if agent_idx < len(self.agents):
                agent_name = list(self.agents)[agent_idx]
                rankings.append((agent_name, count))
        
        # Sort by count (highest first)
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        # If it's a knowledge question, make sure Knowledge agent is first
        if is_knowledge_question and "Knowledge" in self.agents:
            # Find the Knowledge agent in the rankings
            for i, (agent, count) in enumerate(rankings):
                if agent == "Knowledge":
                    # If not already first, move it to the front
                    if i > 0:
                        knowledge_agent = rankings.pop(i)
                        rankings.insert(0, knowledge_agent)
                    break
        
        return rankings 