from qiskit import QuantumCircuit, transpile, ClassicalRegister, QuantumRegister
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2
from qiskit_aer import AerSimulator
import random
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
# on real device
def run_on_real_device(data):
    print("Received data:", data)


    N_BITS = 6  # Hardcoded
    EAVESDROP = data.get('EAVESDROP', False)
    EVE_INTERCEPT_RATE = data.get('EVE_INTERCEPT_RATE', 1.0)

    alice_bits = data['alice_bits']
    alice_bases = data['alice_bases']
    print(f"alice bits : {alice_bits}")
    print(f"alice_bases : {alice_bases}")


    # Step 2: BOB chooses random bases (still random in this case)
    bob_bases = [random.choice(['Z', 'X']) for _ in range(N_BITS)]

    # Optional: Eve intercepts and measures
    eve_bases = [random.choice(['Z', 'X']) if random.random() < EVE_INTERCEPT_RATE else None for _ in range(N_BITS)]
    eve_results = [None] * N_BITS

    circuits = []
    for i in range(N_BITS):
        qc = QuantumCircuit(1, 1)

        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 'X':
            qc.h(0)
        if bob_bases[i] == 'X':
            qc.h(0)

        qc.measure(0, 0)
        circuits.append(qc)

    # Connect to IBM Quantum real device
    service = QiskitRuntimeService(channel="ibm_quantum")
    backend = service.backend("ibm_brisbane")
    compiled_circuits = transpile(circuits, backend=backend)

    with Session(backend=backend) as session:
        sampler = SamplerV2(mode=session)
        result = sampler.run(compiled_circuits, shots=1024).result()

    bob_results = []
    for i in range(N_BITS):
        counts = result[i].join_data().get_counts()
        measured_bit = int(max(counts, key=counts.get)[-1])  # Take the last bit of the bitstring
        bob_results.append(measured_bit)


    # Sifted key creation
    sifted_key_alice = []
    sifted_key_bob = []
    matching_indices = []
    for i in range(N_BITS):
        if alice_bases[i] == bob_bases[i]:
            matching_indices.append(i)
            sifted_key_alice.append(alice_bits[i])
            sifted_key_bob.append(bob_results[i])

    # QBER Calculation
    errors = sum([a != b for a, b in zip(sifted_key_alice, sifted_key_bob)])
    qber = errors / len(sifted_key_alice) if sifted_key_alice else 0

    # Key Verification (simulated public check)
    VERIFICATION_SAMPLE = 5
    sample_indices = random.sample(range(len(sifted_key_alice)), min(VERIFICATION_SAMPLE, len(sifted_key_alice)))
    sample_matches = [sifted_key_alice[i] == sifted_key_bob[i] for i in sample_indices]

    verified = all(sample_matches)
    final_key = [sifted_key_alice[i] for i in range(len(sifted_key_alice)) if i not in sample_indices] if verified else []

    result_data = {
        "Eavesdropping Enabled": False,
        "Total bits sent": N_BITS,
        "Matching bases": len(matching_indices),
        "Errors in matching": errors,
        "QBER": round(qber * 100, 2),
        "Sample verified": "Passed" if verified else "Failed",
        "Final Key": final_key,
    }

    print("\n--- BB84 Quantum Key Distribution (Real Device) ---")
    for key, value in result_data.items():
        print(f"{key}: {value}")

    return result_data


#actual run_simulation
# def run_simulation(data):
#     # Step 1: Get data from frontend (via POST request body)
#     print("Received data:", data)

#     N_BITS = 3
#     EAVESDROP = data.get('EAVESDROP', False)
#     EVE_INTERCEPT_RATE = data.get('EVE_INTERCEPT_RATE', 1.0)
#     alice_bits = data.get('alice_bits', [random.randint(0, 1) for _ in range(N_BITS)])
#     alice_bases = data.get('alice_bases', [random.choice(['Z', 'X']) for _ in range(N_BITS)])

#     # Step 2: BOB chooses random bases
#     bob_bases = [random.choice(['Z', 'X']) for _ in range(N_BITS)]

#     # Optional: Eve intercepts and measures
#     eve_bases = [random.choice(['Z', 'X']) if random.random() < EVE_INTERCEPT_RATE else None for _ in range(N_BITS)]
#     eve_results = [None] * N_BITS

#     # Step 3: Quantum Circuit Creation
#     circuits = []
#     for i in range(N_BITS):
#         qc = QuantumCircuit(1, 1)

#         # Alice encodes her bit
#         if alice_bits[i] == 1:
#             qc.x(0)
#         if alice_bases[i] == 'X':
#             qc.h(0)

#         # Eve intercepts before Bob
#         if EAVESDROP and eve_bases[i] is not None:
#             if eve_bases[i] == 'X':
#                 qc.h(0)
#             qc.measure(0, 0)
#             qc.reset(0)
#             eve_results[i] = 'intercepted'

#             if alice_bits[i] == 1:
#                 qc.x(0)
#             if eve_bases[i] == 'X':
#                 qc.h(0)

#         # Bob's measurement
#         if bob_bases[i] == 'X':
#             qc.h(0)
#         qc.measure(0, 0)
#         circuits.append(qc)

#     # Step 4: Run simulation
#     simulator = AerSimulator()
#     compiled = transpile(circuits, simulator)
#     job = simulator.run(compiled, shots=1024)
#     result = job.result()

#     bob_results = []
#     for i in range(N_BITS):
#         counts = result.get_counts(circuits[i])
#         measured_bit = int(max(counts, key=counts.get))
#         bob_results.append(measured_bit)

#     # Step 5: Sifted key creation
#     sifted_key_alice = []
#     sifted_key_bob = []
#     matching_indices = []

#     for i in range(N_BITS):
#         if alice_bases[i] == bob_bases[i]:
#             matching_indices.append(i)
#             sifted_key_alice.append(alice_bits[i])
#             sifted_key_bob.append(bob_results[i])

#     # Step 6: QBER Calculation
#     errors = sum([a != b for a, b in zip(sifted_key_alice, sifted_key_bob)])
#     qber = errors / len(sifted_key_alice) if sifted_key_alice else 0

#     # Step 7: Key Verification
#     VERIFICATION_SAMPLE = 5
#     sample_indices = random.sample(range(len(sifted_key_alice)), min(VERIFICATION_SAMPLE, len(sifted_key_alice)))
#     sample_matches = [sifted_key_alice[i] == sifted_key_bob[i] for i in sample_indices]

#     verified = all(sample_matches)
#     final_key = [sifted_key_alice[i] for i in range(len(sifted_key_alice)) if i not in sample_indices] if verified else []

#     # Step 8: Bloch Sphere Visualization for Qubit 0


#     vis_qc = QuantumCircuit(1)
#     if alice_bits[0] == 1:
#         vis_qc.x(0)
#     if alice_bases[0] == 'X':
#         vis_qc.h(0)

#     state = Statevector.from_instruction(vis_qc)
#     bloch_coords = state.to_bloch_vector()

#     fig = plot_bloch_vector(bloch_coords, title="Bloch Sphere: Qubit 0 (Alice Encoded)")
#     fig.savefig("bloch_sphere_qubit0.png")

#     # Results display
#     result_data = {
#         "Eavesdropping Enabled": EAVESDROP,
#         "Total bits sent": N_BITS,
#         "Matching bases": len(matching_indices),
#         "Errors in matching": errors,
#         "QBER": round(qber * 100, 2),
#         "Sample verified": "Passed" if verified else "Failed",
#         "Final Key": final_key,
#         "Bloch Sphere Image": "bloch_sphere_qubit0.png"
#     }

#     return result_data

def run_simulation(data):
    print("Received data:", data)

    N_BITS = 6  # Hardcoded
    EAVESDROP = data.get('EAVESDROP', False)
    EVE_INTERCEPT_RATE = data.get('EVE_INTERCEPT_RATE', 1.0)

    alice_bits = data['alice_bits']
    alice_bases = data['alice_bases']
    print(f"alice bits : {alice_bits}")
    print(f"alice_bases : {alice_bases}")

    if not alice_bits or not alice_bases:
        raise ValueError("Missing 'alice_bits' or 'alice_bases' in input data")

    if len(alice_bits) != N_BITS or len(alice_bases) != N_BITS:
        raise ValueError(f"'alice_bits' and 'alice_bases' must be of length {N_BITS}")

    # Bob chooses random bases
    bob_bases = [random.choice(['Z', 'X']) for _ in range(N_BITS)]

    # Eve intercepts
    eve_bases = [random.choice(['Z', 'X']) if random.random() < EVE_INTERCEPT_RATE else None for _ in range(N_BITS)]
    eve_results = [None] * N_BITS

    # Quantum Circuit
    circuits = []
    for i in range(N_BITS):
        qc = QuantumCircuit(1, 1)

        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 'X':
            qc.h(0)

        if EAVESDROP and eve_bases[i] is not None:
            if eve_bases[i] == 'X':
                qc.h(0)
            qc.measure(0, 0)
            qc.reset(0)
            eve_results[i] = 'intercepted'

            if alice_bits[i] == 1:
                qc.x(0)
            if eve_bases[i] == 'X':
                qc.h(0)

        if bob_bases[i] == 'X':
            qc.h(0)
        qc.measure(0, 0)
        circuits.append(qc)

    simulator = AerSimulator()
    compiled = transpile(circuits, simulator)
    job = simulator.run(compiled, shots=1024)
    result = job.result()

    bob_results = []
    for i in range(N_BITS):
        counts = result.get_counts(circuits[i])
        measured_bit = int(max(counts, key=counts.get))
        bob_results.append(measured_bit)

    # Sifted Key
    sifted_key_alice = []
    sifted_key_bob = []
    matching_indices = []

    for i in range(N_BITS):
        if alice_bases[i] == bob_bases[i]:
            matching_indices.append(i)
            sifted_key_alice.append(alice_bits[i])
            sifted_key_bob.append(bob_results[i])

    errors = sum([a != b for a, b in zip(sifted_key_alice, sifted_key_bob)])
    qber = errors / len(sifted_key_alice) if sifted_key_alice else 0

    VERIFICATION_SAMPLE = min(5, len(sifted_key_alice))
    sample_indices = random.sample(range(len(sifted_key_alice)), VERIFICATION_SAMPLE)
    sample_matches = [sifted_key_alice[i] == sifted_key_bob[i] for i in sample_indices]

    verified = all(sample_matches)
    final_key = [sifted_key_alice[i] for i in range(len(sifted_key_alice)) if i not in sample_indices] if verified else []

    # vis_qc = QuantumCircuit(1)
    # if alice_bits[0] == 1:
    #     vis_qc.x(0)
    # if alice_bases[0] == 'X':
    #     vis_qc.h(0)

    # state = Statevector.from_instruction(vis_qc)
    # bloch_coords = state.to_bloch_vector()

    # fig = plot_bloch_vector(bloch_coords, title="Bloch Sphere: Qubit 0 (Alice Encoded)")
    # fig.savefig("bloch_sphere_qubit0.png")

    result_data = {
        "Eavesdropping Enabled": EAVESDROP,
        "Matching bases": len(matching_indices),
        "Errors in matching": errors,
        "QBER": round(qber * 100, 2),
        "Sample verified": "Passed" if verified else "Failed",
        "Final Key": final_key,
        # "Bloch Sphere Image": "bloch_sphere_qubit0.png"
    }

    return result_data


if __name__ == "__main__":
    choice = (input("Choose simulation type (1 for simulation, 2 for real device): "))
    if choice == "1":
        data = {
            'N_BITS': int(input("Enter number of bits (recommended : 32): ")),
            'EAVESDROP': input("Enable eavesdropping? (True/False): ").strip().lower() == 'true',
            'alice_bits': [random.randint(0, 1) for _ in range(6)],
            'alice_bases': [random.choice(['Z', 'X']) for _ in range(6)]
        }
        print(run_simulation(data))

    elif choice == "2":
        data = {
            'N_BITS': int(input("Enter number of bits (recommended : 32): ")),
            'EAVESDROP': input("Enable eavesdropping? (True/False): ").strip().lower() == 'true',
            'alice_bits': [random.randint(0, 1) for _ in range(50)],
            'alice_bases': [random.choice(['Z', 'X']) for _ in range(50)]
        }
        print(run_on_real_device(data))
    else:
        print("Invalid choice.")