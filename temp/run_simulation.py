from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def run_simulation(input_dict):
    # Create your quantum circuit
    cr = ClassicalRegister(1, 'cr')
    qr = QuantumRegister(1, 'qr')
    qc = QuantumCircuit(qr, cr)

    if input_dict['alice_bit'] == 1:
        qc.x(0)
    if input_dict['alice_base'] == 'X':
        qc.h(0)
    qc.measure(0, 0)

    # Initialize the AerSimulator
    simulator = AerSimulator()

    # Transpile the circuit for the simulator
    transpiled_qc = transpile(qc, simulator)

    # Run the simulation
    result = simulator.run(transpiled_qc, shots=1024).result()

    # Process the result to get counts
    counts = result.get_counts()

    print("Counts:", counts)
    return {'counts': counts}

print(run_simulation({'alice_bit': 1, 'alice_base': 'X'}))
