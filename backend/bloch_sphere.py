# from qiskit import QuantumCircuit
# from qiskit.quantum_info import Statevector, SparsePauliOp
# from qiskit.visualization.bloch import Bloch
# import numpy as np
# import matplotlib.pyplot as plt
# from flask import Flask, jsonify

# # Example 16-bit inputs
# alice_bits = [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1]
# alice_bases = ['Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X']

# def plot_bloch_sphere(alice_bits, alice_bases):
#     # Initialize a Bloch sphere
#     bloch = Bloch()
#     bloch.font_size = 12
#     bloch.title = "All 16 Qubits - Bloch Vectors"
#     vectors = []

#     for i in range(16):
#         qc = QuantumCircuit(1)
#         if alice_bits[i] == 1:
#             qc.x(0)
#         if alice_bases[i] == 'X':
#             qc.h(0)

#         state = Statevector.from_instruction(qc)
#         bloch_vector = [
#             np.real(state.expectation_value(SparsePauliOp.from_list([("X", 1)]))),
#             np.real(state.expectation_value(SparsePauliOp.from_list([("Y", 1)]))),
#             np.real(state.expectation_value(SparsePauliOp.from_list([("Z", 1)])))
#         ]

#         vectors.append({"x": bloch_vector[0], "y": bloch_vector[1], "z": bloch_vector[2]})

#     return jsonify(vectors)
    


# This code plots Bloch spheres for 16 qubits using Alice's bit and basis choices
# import matplotlib
# matplotlib.use("Agg")  # Use non-interactive backend
# from qiskit import QuantumCircuit
# from qiskit.quantum_info import Statevector, SparsePauliOp
# from qiskit.visualization import plot_bloch_vector
# import matplotlib.pyplot as plt
# import numpy as np

# Example inputs (16 random bits and bases)
# alice_bits = [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1]
# alice_bases = ['Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X']

# Create figure with 4x4 subplots
# fig = plt.figure(figsize=(16, 10), dpi=100)
# axs = [fig.add_subplot(4, 4, i + 1, projection='3d') for i in range(16)]
# fig.suptitle("Bloch Spheres: Alice's Encoded 16 Qubits", fontsize=18)

import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend for saving images
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.visualization import plot_bloch_vector
import numpy as np
from io import BytesIO
import os, datetime

def plot_sphere(alice_bits, alice_bases):
    try:
        # Create a folder to save images if it doesn't exist (optional, as you're returning image in memory)
        save_folder = 'images'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        # Generate the filename based on the current date and time (optional for saving to disk)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(save_folder, f"bloch_spheres_{timestamp}.png")

        # Create figure with subplots for the number of qubits (16)
        fig = plt.figure(figsize=(16, 10), dpi=100)
        axs = [fig.add_subplot(4, 4, i + 1, projection='3d') for i in range(len(alice_bits))]
        fig.suptitle("Bloch Spheres: Alice's Encoded 16 Qubits", fontsize=18)

        for i in range(len(alice_bits)):
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

        # Save the plot to a BytesIO object instead of saving to disk
        img_io = BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)  # Seek to the beginning of the BytesIO object
        plt.close()

        return img_io  # Return the image as a BytesIO object

    except Exception as e:
        raise Exception(f"Error generating Bloch sphere: {str(e)}")
