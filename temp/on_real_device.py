from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2
import random

def run_on_real_device(data):
    print("Received data:", data)

    # Decode the data into parameters
    N_BITS = data.get('N_BITS', 50)  # Default to 50 if not provided
    EAVESDROP = data.get('EAVESDROP', False)  # Default to False
    EVE_INTERCEPT_RATE = data.get('EVE_INTERCEPT_RATE', 1.0)  # Default to 1.0
    alice_bits = data.get('alice_bits', [random.randint(0, 1) for _ in range(N_BITS)])
    alice_bases = data.get('alice_bases', [random.choice(['Z', 'X']) for _ in range(N_BITS)])

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

    print(result_data)
    return result_data

if __name__ == "__main__":
        run_on_real_device({
        'N_BITS': 3,
        'alice_bits': [1, 0, 1],
        'alice_bases': ['Z', 'X', 'Z']
        })