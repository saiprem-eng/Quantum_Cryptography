# This code plots Bloch spheres for 16 qubits using Alice's bit and basis choices
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
import numpy as np

# Example inputs (16 random bits and bases)
alice_bits = [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1]
alice_bases = ['Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X']

# Create figure with 4x4 subplots
fig = plt.figure(figsize=(16, 10), dpi=100)
axs = [fig.add_subplot(4, 4, i + 1, projection='3d') for i in range(16)]
fig.suptitle("Bloch Spheres: Alice's Encoded 16 Qubits", fontsize=18)

for i in range(16):
    qc_vis = QuantumCircuit(1)
    if alice_bits[i] == 1:
        qc_vis.x(0)
    if alice_bases[i] == 'X':
        qc_vis.h(0)

    state = Statevector.from_instruction(qc_vis)
    bloch_vector = [
        np.real(state.expectation_value(SparsePauliOp.from_list([("X", 1)]))),
        np.real(state.expectation_value(SparsePauliOp.from_list([("Y", 1)]))),
        np.real(state.expectation_value(SparsePauliOp.from_list([("Z", 1)])))
    ]

    plot_bloch_vector(bloch_vector, title=f"Qubit {i}", ax=axs[i])

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig("bloch_spheres_16qubits.png")
print("✅ Saved Bloch spheres to 'bloch_spheres_16qubits.png'")
