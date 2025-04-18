import random
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.visualization import plot_histogram
from matplotlib import pyplot as plt 
from qiskit.providers.basic_provider import BasicProvider

# # Parameters
# n = 20  # Number of bits to exchange

# # Step 1: Alice generates random bits and random bases
# alice_bits = [random.randint(0, 1) for _ in range(n)]
# alice_bases = [random.choice(['Z', 'X']) for _ in range(n)]

# # Step 2: Bob chooses his random measurement bases
# bob_bases = [random.choice(['Z', 'X']) for _ in range(n)]

# # Step 3: Create quantum circuits
# circuits = []
# for i in range(n):
#     qc = QuantumCircuit(1, 1)

#     # Encode Alice's bit
#     if alice_bits[i] == 1:
#         qc.x(0)
#     if alice_bases[i] == 'X':
#         qc.h(0)

#     # Bob's measurement
#     if bob_bases[i] == 'X':
#         qc.h(0)
#     qc.measure(0, 0)
#     circuits.append(qc)

# # Step 4: Run the circuits on Qiskit simulator

# simulator = BasicProvider().get_backend("basic_simulator")
# compiled = transpile(circuits, simulator)
# job = simulator.run(compiled)
# result = job.result()

# # Step 5: Bob reads the results
# bob_results = []
# for i in range(n):
#     counts = result.get_counts(circuits[i])
#     bit = int(list(counts.keys())[0])
#     bob_results.append(bit)

# # Step 6: Publicly compare bases and create sifted key
# sifted_key = []
# matching_indices = []
# for i in range(n):
#     if alice_bases[i] == bob_bases[i]:
#         matching_indices.append(i)
#         if alice_bits[i] == bob_results[i]:
#             sifted_key.append(alice_bits[i])

# # Step 7: Display results
# print("\n--- BB84 Protocol Simulation ---")
# print("Alice's bits:    ", alice_bits)
# print("Alice's bases:   ", alice_bases)
# print("Bob's bases:     ", bob_bases)
# print("Bob's results:   ", bob_results)
# print("Matching indices:", matching_indices)
# print("Sifted key:      ", sifted_key)
# print("Key length:      ", len(sifted_key))


# import random
# from qiskit import QuantumCircuit, transpile
# from qiskit.visualization import plot_histogram
# from matplotlib import pyplot as plt
# from qiskit.providers.basic_provider import BasicProvider

# -------------------------------
# PARAMETERS
# -------------------------------
N_BITS = 50            # Number of bits to transmit
EAVESDROP = True       # Toggle Eve ON/OFF
EVE_INTERCEPT_RATE = 1.0  # Percentage of qubits Eve intercepts (0.0 to 1.0)

# -------------------------------
# STEP 1: ALICE generates bits and bases
# -------------------------------
alice_bits = [random.randint(0, 1) for _ in range(N_BITS)]
alice_bases = [random.choice(['Z', 'X']) for _ in range(N_BITS)]

# -------------------------------
# STEP 2: BOB chooses random bases
# -------------------------------
bob_bases = [random.choice(['Z', 'X']) for _ in range(N_BITS)]

# Optional: Eve intercepts and measures
eve_bases = [random.choice(['Z', 'X']) if random.random() < EVE_INTERCEPT_RATE else None for _ in range(N_BITS)]
eve_results = [None] * N_BITS

# -------------------------------
# STEP 3: Quantum Circuit Creation
# -------------------------------
circuits = []
for i in range(N_BITS):
    qc = QuantumCircuit(1, 1)

    # Alice encodes her bit
    if alice_bits[i] == 1:
        qc.x(0)
    if alice_bases[i] == 'X':
        qc.h(0)

    # Eve intercepts before Bob
    if EAVESDROP and eve_bases[i] is not None:
        if eve_bases[i] == 'X':
            qc.h(0)
        qc.measure(0, 0)
        qc.reset(0)
        eve_results[i] = 'intercepted'

        # Re-encode Eve's result
        if alice_bits[i] == 1:
            qc.x(0)
        if eve_bases[i] == 'X':
            qc.h(0)

    # Bob's measurement
    if bob_bases[i] == 'X':
        qc.h(0)
    qc.measure(0, 0)
    circuits.append(qc)

# -------------------------------
# STEP 4: Run simulation
# -------------------------------
simulator = BasicProvider().get_backend("basic_simulator")
compiled = transpile(circuits, simulator)
job = simulator.run(compiled)
result = job.result()

bob_results = []
for i in range(N_BITS):
    counts = result.get_counts(circuits[i])
    measured_bit = int(max(counts, key=counts.get))  # Get most likely bit
    bob_results.append(measured_bit)

# -------------------------------
# STEP 5: Sifted key creation
# -------------------------------
sifted_key_alice = []
sifted_key_bob = []
matching_indices = []

for i in range(N_BITS):
    if alice_bases[i] == bob_bases[i]:
        matching_indices.append(i)
        sifted_key_alice.append(alice_bits[i])
        sifted_key_bob.append(bob_results[i])

# -------------------------------
# STEP 6: QBER Calculation
# -------------------------------
errors = sum([a != b for a, b in zip(sifted_key_alice, sifted_key_bob)])
qber = errors / len(sifted_key_alice) if sifted_key_alice else 0

# -------------------------------
# STEP 7: Key Verification (simulated public check)
# -------------------------------
VERIFICATION_SAMPLE = 5
sample_indices = random.sample(range(len(sifted_key_alice)), min(VERIFICATION_SAMPLE, len(sifted_key_alice)))
sample_matches = [sifted_key_alice[i] == sifted_key_bob[i] for i in sample_indices]

verified = all(sample_matches)
final_key = [sifted_key_alice[i] for i in range(len(sifted_key_alice)) if i not in sample_indices] if verified else []

# -------------------------------
# RESULTS DISPLAY
# -------------------------------
print("\n--- BB84 Quantum Key Distribution ---")
print("Eavesdropping Enabled:", EAVESDROP)
print("Total bits sent:       ", N_BITS)
print("Matching bases:        ", len(matching_indices))
print("Errors in matching:    ", errors)
print("QBER:                  ", round(qber * 100, 2), "%")
print("Sample verified:", "Passed" if verified else "Failed")
print("Final Key (length = {}):".format(len(final_key)), final_key)

# Optional: Plot histogram of one measurement
plot_histogram(result.get_counts(circuits[0]))
plt.title("Measurement Histogram of First Qubit")
plt.show()
