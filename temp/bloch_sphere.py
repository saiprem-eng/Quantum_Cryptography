    # Optional: Bloch sphere visualization for the first qubit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
import numpy as np
import matplotlib.pyplot as plt

# Recreate the statevector before measurement (after Alice's encoding)
qc_vis = QuantumCircuit(1)
if alice_bits[0] == 1:
    qc_vis.x(0)
if alice_bases[0] == 'X':
    qc_vis.h(0)

state = Statevector.from_instruction(qc_vis)
bloch_vector = state.data BlochVector = state.to_instruction().to_matrix()  # You can use state.to_operator() too
bloch_coords = state.to_bloch_vector()

# Plot Bloch sphere
fig = plot_bloch_vector(bloch_coords, title="Bloch Sphere: Qubit 0 After Alice Encoding")
fig.savefig("bloch_sphere_qubit0.png")
