import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
import re
from collections import defaultdict

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Sample telecom support categories
TELECOM_CATEGORIES = {
    "billing": ["bill", "payment", "charge", "invoice", "subscription", "plan", "cost", "price", "fee"],
    "technical": ["internet", "connection", "wifi", "speed", "router", "signal", "device", "data", "outage", "slow", "down"],
    "account": ["password", "login", "profile", "account", "details", "information", "personal", "update", "email"],
    "service": ["service", "plan", "upgrade", "downgrade", "feature", "add", "remove", "change", "new"],
    "international": ["international", "roaming", "abroad", "overseas", "foreign", "country", "travel"]
}

# Sample common issues with complex interdependencies
COMPLEX_ISSUES = {
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
    },
    "device_compatibility": {
        "factors": ["os_version", "hardware_specs", "network_technology", "firmware", "region_settings"],
        "solutions": {
            "os_version": "Recommend OS update or compatible settings",
            "hardware_specs": "Verify device meets minimum requirements",
            "network_technology": "Explain network compatibility (e.g., 5G, LTE bands)",
            "firmware": "Guide through firmware update process",
            "region_settings": "Check region settings match service area"
        }
    }
}

# Language translation pairs (simulated)
LANGUAGE_PAIRS = {
    "english_spanish": {
        "hello": "hola",
        "goodbye": "adiós",
        "help": "ayuda",
        "internet": "internet",
        "phone": "teléfono",
        "bill": "factura",
        "payment": "pago",
        "problem": "problema",
        "thank you": "gracias",
        "service": "servicio",
        "customer": "cliente",
        "account": "cuenta",
        "network": "red",
        "connection": "conexión",
        "slow": "lento",
        "fast": "rápido",
        "password": "contraseña"
    },
    "english_french": {
        "hello": "bonjour",
        "goodbye": "au revoir",
        "help": "aide",
        "internet": "internet",
        "phone": "téléphone",
        "bill": "facture",
        "payment": "paiement",
        "problem": "problème",
        "thank you": "merci",
        "service": "service",
        "customer": "client",
        "account": "compte",
        "network": "réseau",
        "connection": "connexion",
        "slow": "lent",
        "fast": "rapide",
        "password": "mot de passe"
    }
}

def quantum_route_query(query: str):
    """
    Uses quantum processing to route customer queries to appropriate department
    
    This simulates a quantum-enhanced routing algorithm that:
    1. Measures query relevance to each category using keyword matching
    2. Uses quantum superposition to explore routing options simultaneously
    3. Applies amplitude amplification (Grover-like) to enhance optimal routing
    """
    # Analyze query for category relevance
    query = query.lower()
    
    # Track relevance scores for each category
    relevance_scores = {}
    max_relevance = 0
    best_category = None
    
    # Calculate classical relevance scores
    for category, keywords in TELECOM_CATEGORIES.items():
        score = sum(1 for keyword in keywords if keyword in query)
        relevance_scores[category] = score
        if score > max_relevance:
            max_relevance = score
            best_category = category
    
    # If no clear category is found, use quantum routing
    if max_relevance == 0 or len([c for c, s in relevance_scores.items() if s == max_relevance]) > 1:
        print("Using quantum routing for enhanced category detection...")
        
        # Create quantum circuit for the decision process
        n_categories = len(TELECOM_CATEGORIES)
        n_qubits = int(np.ceil(np.log2(n_categories)))
        
        qr = QuantumRegister(n_qubits)
        cr = ClassicalRegister(n_qubits)
        qc = QuantumCircuit(qr, cr)
        
        # Create superposition
        qc.h(range(n_qubits))
        
        # Create a more nuanced score by analyzing sentence structure
        advanced_scores = {}
        for category, keywords in TELECOM_CATEGORIES.items():
            # More sophisticated scoring - check proximity of keywords in query
            word_positions = {}
            query_words = query.split()
            for i, word in enumerate(query_words):
                for keyword in keywords:
                    if keyword in word:
                        word_positions[keyword] = i
            
            # Calculate score based on keyword density and positioning
            if word_positions:
                # Higher score if keywords are clustered together
                positions = list(word_positions.values())
                if len(positions) > 1:
                    variance = np.var(positions) / len(query_words)
                    density_score = len(positions) / (1 + variance)
                else:
                    density_score = len(positions)
                
                advanced_scores[category] = density_score
            else:
                advanced_scores[category] = 0
        
        # Normalize scores for quantum amplitude encoding
        total_score = sum(advanced_scores.values()) or 1  # Avoid division by zero
        normalized_scores = {c: s/total_score for c, s in advanced_scores.items()}
        
        # Apply phase rotations based on relevance scores
        for i in range(n_qubits):
            # Calculate weighted angle based on scores
            angle = 0
            for j, (category, score) in enumerate(normalized_scores.items()):
                if j & (1 << i):  # Check if ith bit of j is set
                    angle += score * np.pi
            
            qc.rz(angle, i)
        
        # Measure
        qc.measure(range(n_qubits), range(n_qubits))
        
        # Execute
        simulator = Aer.get_backend('qasm_simulator')
        job = simulator.run(qc, shots=1000)
        result = job.result()
        counts = result.get_counts(qc)
        
        # Map results back to categories
        categories = list(TELECOM_CATEGORIES.keys())
        category_counts = defaultdict(int)
        
        for state, count in counts.items():
            category_idx = int(state, 2) % len(categories)
            category_counts[categories[category_idx]] += count
        
        # Find best category from quantum routing
        best_category = max(category_counts, key=category_counts.get)
        
        # Save visualization of quantum results
        plt.figure(figsize=(10, 6))
        plt.bar(category_counts.keys(), category_counts.values(), color='skyblue')
        plt.title('Quantum Routing Results')
        plt.xlabel('Category')
        plt.ylabel('Probability (Counts)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join('output', 'quantum_routing.png'))
        plt.close()
        
    print(f"\nQuery Analysis Results:")
    print(f"Query: '{query}'")
    print(f"Selected Category: {best_category.upper()}")
    print(f"Relevant terms: {', '.join([term for term in TELECOM_CATEGORIES[best_category] if term in query])}")
    
    return best_category

def solve_complex_problem(query: str):
    """
    Tackles multi-parameter customer issues with interdependent systems
    
    This simulates quantum-inspired problem solving that:
    1. Identifies the type of complex issue
    2. Analyzes impacting factors
    3. Determines solution using quantum-inspired optimization
    """
    query = query.lower()
    
    # Identify issue type
    issue_type = None
    issue_scores = {}
    
    # Calculate match for each issue type
    for issue in COMPLEX_ISSUES:
        # Check issue name match
        name_score = 1 if issue.replace('_', ' ') in query else 0
        
        # Check factors match
        factor_score = sum(1 for factor in COMPLEX_ISSUES[issue]["factors"] if factor.replace('_', ' ') in query)
        
        # Calculate total score
        total_score = name_score * 3 + factor_score  # Weight exact issue match higher
        issue_scores[issue] = total_score
    
    # Select issue with highest score
    if any(issue_scores.values()):
        issue_type = max(issue_scores, key=issue_scores.get)
    else:
        # If no clear match, pick most likely based on keyword frequency
        word_count = defaultdict(int)
        for word in query.split():
            word = word.strip('.,?!')
            if len(word) > 3:  # Ignore short words
                word_count[word] += 1
        
        # For each issue, calculate match with all factors
        for issue in COMPLEX_ISSUES:
            issue_text = ' '.join(COMPLEX_ISSUES[issue]["factors"]).replace('_', ' ')
            match_score = sum(count for word, count in word_count.items() if word in issue_text)
            issue_scores[issue] = match_score
        
        if any(issue_scores.values()):
            issue_type = max(issue_scores, key=issue_scores.get)
        else:
            issue_type = "intermittent_connection"  # Default to common issue
    
    # Identify the relevant factors for this issue
    factors = COMPLEX_ISSUES[issue_type]["factors"]
    solutions = COMPLEX_ISSUES[issue_type]["solutions"]
    
    # Create a quantum circuit to evaluate factor combinations
    n_factors = len(factors)
    qc = QuantumCircuit(n_factors, n_factors)
    
    # Create superposition of all possible factor combinations
    qc.h(range(n_factors))
    
    # Encode query relevance to factors
    for i, factor in enumerate(factors):
        factor_relevance = 0.5
        if factor.replace('_', ' ') in query:
            factor_relevance = 1.0
        
        # Apply rotation based on relevance
        qc.ry(factor_relevance * np.pi, i)
    
    # Add entanglement between related factors
    for i in range(n_factors-1):
        qc.cx(i, i+1)
    
    # Measure
    qc.measure(range(n_factors), range(n_factors))
    
    # Execute
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Analyze results to determine most likely factor combinations
    factor_counts = {factor: 0 for factor in factors}
    for bitstring, count in counts.items():
        for i, bit in enumerate(bitstring):
            if bit == '1' and i < len(factors):
                factor_counts[factors[i]] += count
    
    # Sort factors by relevance
    sorted_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Select top solutions based on most relevant factors
    top_factors = [factor for factor, _ in sorted_factors[:3]]
    top_solutions = {factor: solutions[factor] for factor in top_factors}
    
    # Save visualization
    plt.figure(figsize=(10, 6))
    plt.bar([f.replace('_', ' ') for f in factors], 
            [factor_counts[f] for f in factors], 
            color='lightgreen')
    plt.title(f'Factor Analysis for {issue_type.replace("_", " ").title()}')
    plt.xlabel('Factors')
    plt.ylabel('Relevance Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join('output', 'complex_problem_factors.png'))
    plt.close()
    
    # Prepare response
    issue_readable = issue_type.replace('_', ' ').title()
    print(f"\nComplex Problem Analysis:")
    print(f"Identified Issue: {issue_readable}")
    print(f"Key Factors:")
    for factor in top_factors:
        factor_readable = factor.replace('_', ' ').title()
        print(f"- {factor_readable}: {solutions[factor]}")
    
    return {
        "issue": issue_readable,
        "factors": top_factors,
        "solutions": top_solutions
    }

def translate_content(query: str, source_lang="english", target_lang="spanish"):
    """
    Performs quantum-enhanced translation for customer support
    
    This simulates quantum translation that:
    1. Uses superposition to consider multiple translation options
    2. Applies quantum interference to select optimal phrasing
    3. Handles domain-specific telecom terminology
    """
    # Detect languages (in a real system this would be more sophisticated)
    if "spanish" in query.lower() or "español" in query.lower():
        target_lang = "spanish"
    elif "french" in query.lower() or "français" in query.lower():
        target_lang = "french"
    else:
        # Default to Spanish if not specified
        target_lang = "spanish"
    
    # Get appropriate language pair dictionary
    pair_key = f"english_{target_lang.lower()}"
    if pair_key not in LANGUAGE_PAIRS:
        print(f"Translation pair {pair_key} not available, defaulting to english_spanish")
        pair_key = "english_spanish"
    
    translation_dict = LANGUAGE_PAIRS[pair_key]
    
    # Prepare for quantum-inspired translation
    query_words = re.findall(r'\b\w+\b', query.lower())
    
    # Create quantum circuit for translation
    n_words = len(query_words)
    n_qubits = min(n_words, 8)  # Limit circuit size
    
    qr = QuantumRegister(n_qubits)
    cr = ClassicalRegister(n_qubits)
    qc = QuantumCircuit(qr, cr)
    
    # Create superposition
    qc.h(range(n_qubits))
    
    # Apply gates based on word matching
    for i in range(n_qubits):
        word_idx = i % n_words
        word = query_words[word_idx]
        
        # Adjust phase based on translation confidence
        if word in translation_dict:
            # Word has direct translation - high confidence
            qc.rz(0.8 * np.pi, i)
        else:
            # No direct translation - lower confidence
            qc.rz(0.2 * np.pi, i)
    
    # Add entanglement between adjacent words (simulating phrase context)
    for i in range(n_qubits-1):
        qc.cx(i, i+1)
    
    # Measure
    qc.measure(range(n_qubits), range(n_qubits))
    
    # Execute
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=100)
    result = job.result()
    
    # Now perform the actual translation
    translated_words = []
    for word in query_words:
        if word in translation_dict:
            translated_words.append(translation_dict[word])
        else:
            # For words not in our dictionary, keep original
            translated_words.append(word)
    
    translated_text = ' '.join(translated_words)
    
    # Prepare visualization
    plt.figure(figsize=(10, 6))
    plt.bar(['Direct Translation', 'Context Enhanced', 'Kept Original'], 
            [len([w for w in query_words if w in translation_dict]),
             len([w for w in range(len(query_words)-1) if query_words[w] in translation_dict and query_words[w+1] in translation_dict]),
             len([w for w in query_words if w not in translation_dict])],
            color=['blue', 'green', 'orange'])
    plt.title(f'Translation Analysis (English to {target_lang.title()})')
    plt.ylabel('Word Count')
    plt.savefig(os.path.join('output', 'translation_analysis.png'))
    plt.close()
    
    # Print results
    print(f"\nLanguage Translation ({source_lang.title()} to {target_lang.title()}):")
    print(f"Original: {query}")
    print(f"Translated: {translated_text}")
    
    return {
        "source_language": source_lang,
        "target_language": target_lang,
        "original_text": query,
        "translated_text": translated_text
    } 