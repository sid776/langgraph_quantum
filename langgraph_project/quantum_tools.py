from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import GroverOperator
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run_qiskit_circuit():
    # Original bell state circuit implementation
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    print("Bell State Results:")
    for state, count in counts.items():
        print(f"State {state}: {count} shots")
    
    # Save plot to file instead of displaying
    plt.figure(figsize=(8, 6))
    plot_histogram(counts)
    plt.title("Bell State Results")
    output_file = os.path.join('output', 'bell_state.png')
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved to {output_file}")
    
    return counts

def grover_search():
    # Implementation of Grover's search algorithm
    n_qubits = 3  # Number of qubits
    target_state = '101'  # State we're searching for
    
    # Create circuit
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Initialize superposition
    qc.h(range(n_qubits))
    
    # Oracle - flip the phase of the target state
    # Convert target state to bit positions that are 0
    for qubit, bit in enumerate(target_state):
        if bit == '0':
            qc.x(qubit)  # Flip qubits that should be 0
    
    # Apply multi-controlled-Z operation (phase flip on target state)
    qc.h(n_qubits-1)
    qc.mcx(list(range(n_qubits-1)), n_qubits-1)  # Multi-controlled-X
    qc.h(n_qubits-1)
    
    # Undo the qubit flips
    for qubit, bit in enumerate(target_state):
        if bit == '0':
            qc.x(qubit)
    
    # Diffusion operator (amplification)
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    
    qc.h(n_qubits-1)
    qc.mcx(list(range(n_qubits-1)), n_qubits-1)
    qc.h(n_qubits-1)
    
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))
    
    # Measure
    qc.measure(range(n_qubits), range(n_qubits))
    
    # Execute
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    print("\nGrover's Search Results:")
    print(f"Searching for state: {target_state}")
    for state, count in counts.items():
        print(f"State {state}: {count} shots")
    
    # Save plot to file instead of displaying
    plt.figure(figsize=(8, 6))
    plot_histogram(counts)
    plt.title(f"Grover's Search Results (Target: {target_state})")
    output_file = os.path.join('output', 'grover_search.png')
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved to {output_file}")
    
    return counts

def shor_simulation():
    # Simplified simulation of Shor's algorithm concepts
    # (Note: Full Shor's algorithm implementation would be much more complex)
    n_qubits = 3
    
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Create quantum Fourier transform circuit
    for i in range(n_qubits):
        qc.h(i)
        for j in range(i+1, n_qubits):
            qc.cp(np.pi/float(2**(j-i)), i, j)
    
    # Measure
    qc.measure(range(n_qubits), range(n_qubits))
    
    # Execute
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    print("\nQuantum Fourier Transform Results (Shor's Algorithm Component):")
    for state, count in counts.items():
        print(f"State {state}: {count} shots")
    
    # Save plot to file instead of displaying
    plt.figure(figsize=(8, 6))
    plot_histogram(counts)
    plt.title("Quantum Fourier Transform Results")
    output_file = os.path.join('output', 'shor_simulation.png')
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved to {output_file}")
    
    return counts

def run_azure_quantum():
    print("Azure Quantum integration requires additional setup:")
    print("1. Azure subscription")
    print("2. Azure Quantum workspace")
    print("3. Proper credentials configuration")
    print("\nSkipping Azure Quantum execution for now.") 