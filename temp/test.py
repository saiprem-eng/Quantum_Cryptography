# from qiskit import QuantumCircuit
# from qiskit_ibm_runtime import SamplerV2, QiskitRuntimeService, Session

# # Simulation Function
# def run_simulation(input_dict):
#     # Create your quantum circuit
#     qc = QuantumCircuit(1, 1)
#     if input_dict['alice_base'] == 'X':
#         qc.h(0)
#     if input_dict['alice_bit'] == 1:
#         qc.x(0)
#     qc.measure(0, 0)

#     # Initialize the Qiskit Runtime service
#     service = QiskitRuntimeService(channel="ibm_quantum")

#     # Retrieve available backends
#     available_backends = service.backends()
#     for backend in available_backends:
#         print(backend)

#     # Select the backend (you can choose any from the available ones)
#     backend = available_backends[0]  # Using the first backend as an example

#     # Start a session with the backend
#     with Session(service=service, backend=backend) as session:
#         sampler = SamplerV2(service=service)  # Initialize with the service, not session
        
#         # Pass the circuit as a list
#         result = sampler.run([qc], shots=1024).result()
        
#         # Get the counts from the result
#         counts = result.quasi_dists[0].nearest_probability_distribution().binary_probabilities()

#     return {'counts': counts}

# # Test the simulation
# print(run_simulation({"alice_bit": 1, "alice_base": "X"}))


from qiskit import QuantumCircuit, transpile, ClassicalRegister, QuantumRegister
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2

def run_simulation(input_dict):
    # Create your quantum circuit
    cr = ClassicalRegister(1, 'cr')
    qr = QuantumRegister(1, 'qr')
    qc = QuantumCircuit(qr, cr)
    if input_dict['alice_base'] == 'X':
        qc.h(0)
    if input_dict['alice_bit'] == 1:
        qc.x(0)
    qc.measure(0, 0)

    # Initialize the Qiskit Runtime service
    service = QiskitRuntimeService(channel="ibm_quantum")

    #     # Retrieve available backends
    available_backends = service.backends()
    for backend in available_backends:
        print(backend)

    # Select the least busy backend
    # backend = service.least_busy(min_num_qubits = 127, operational=True, simulator=True)
    backend = service.backend("ibm_kyiv")

        # Transpile the circuit for the target backend
    transpiled_qc = transpile(qc, backend=backend)

    # Start a session with the selected backend
    with Session(backend=backend) as session:
        # Initialize the SamplerV2 with the session as mode
        sampler = SamplerV2(mode=session)
        
        # Run the sampler with the circuit wrapped in a list
        result = sampler.run([transpiled_qc], shots=1024).result()
        
        # Process the result to get counts
        counts = result[0].data.cr.get_counts()


    return {'counts': counts}

# Example usage
print(run_simulation({"alice_bit": 1, "alice_base": "X"}))
