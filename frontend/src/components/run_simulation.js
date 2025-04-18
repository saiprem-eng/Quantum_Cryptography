import React, { useState } from 'react';

function BB84Form() {
  const [aliceBit, setAliceBit] = useState(null);
  const [aliceBase, setAliceBase] = useState('');
  const [eveBase, setEveBase] = useState(false); // Added Eve's base state

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent the default form submission

    // Create the data object
    const data = {
      alice_bit: aliceBit,
      alice_base: aliceBase,
    };

    try {
      const response = await fetch('http://localhost:5000/run_simulation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      const result = await response.json();
  
      if (response.ok) {
        console.log('✅ Simulation Success:', result);
        // alert(`Simulation Success: ${JSON.stringify(result.data)}`);
        // Optionally set state to render on UI
        // setSimulationData(result.data);
      } else {
        console.error('❌ API Error:', result.message);
        // alert(`API Error: ${result.message}`);
      }
    } catch (error) {
      console.error('❌ Network or Server Error:', error);
      // alert('Network or Server Error. Please try again later.');
    }
  };

  const handleChange = (e) => {
    setEveBase(e.target.value === 'true');
  };

  return (
    <div>
      <h2>BB84 Protocol</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Alice Bit (0 or 1):
          <input
            type="number"
            value={aliceBit}
            onChange={(e) => setAliceBit(Number(e.target.value))}
            min="0"
            max="1"
          />
        </label>
        <br />
        <label>
          Alice Base (Z or X):
          <input
            type="text"
            value={aliceBase}
            onChange={(e) => setAliceBase(e.target.value)}
            placeholder="Z or X"
          />
        </label>
        <br />
        <label>
        <span>Enable Eve Base: </span>
        <input
          type="radio"
          value="true"
          checked={eveBase === true}
          onChange={handleChange}
        />
        True
      </label>

      <label style={{ marginLeft: '1rem' }}>
      <span>Disable Eve Base: </span>
        <input
          type="radio"
          value="false"
          checked={eveBase === false}
          onChange={handleChange}
        />
        False
      </label>
        <br />
        <button type="submit">Run Simulation</button>
      </form>
    </div>
  );
}

export default BB84Form;

// i want same this code 
// import random
// from qiskit import QuantumCircuit, transpile
// from qiskit.visualization import plot_histogram
// from matplotlib import pyplot as plt
// from qiskit_aer import AerSimulator  # Updated import for Qiskit 2.0

// # Parameters
// N_BITS = 50            # Number of bits to transmit
// EAVESDROP = False       # Toggle Eve ON/OFF
// EVE_INTERCEPT_RATE = 1.0  # Percentage of qubits Eve intercepts (0.0 to 1.0)

// # -------------------------------
// # STEP 1: ALICE generates bits and bases
// # -------------------------------
// alice_bits = [random.randint(0, 1) for _ in range(N_BITS)]
// alice_bases = [random.choice(['Z', 'X']) for _ in range(N_BITS)]

// # -------------------------------
// # STEP 2: BOB chooses random bases
// # -------------------------------
// bob_bases = [random.choice(['Z', 'X']) for _ in range(N_BITS)]

// # Optional: Eve intercepts and measures
// eve_bases = [random.choice(['Z', 'X']) if random.random() < EVE_INTERCEPT_RATE else None for _ in range(N_BITS)]
// eve_results = [None] * N_BITS

// # -------------------------------
// # STEP 3: Quantum Circuit Creation
// # -------------------------------
// circuits = []
// for i in range(N_BITS):
//     qc = QuantumCircuit(1, 1)

//     # Alice encodes her bit
//     if alice_bits[i] == 1:
//         qc.x(0)
//     if alice_bases[i] == 'X':
//         qc.h(0)

//     # Eve intercepts before Bob
//     if EAVESDROP and eve_bases[i] is not None:
//         if eve_bases[i] == 'X':
//             qc.h(0)
//         qc.measure(0, 0)
//         qc.reset(0)
//         eve_results[i] = 'intercepted'

//         # Re-encode Eve's result
//         if alice_bits[i] == 1:
//             qc.x(0)
//         if eve_bases[i] == 'X':
//             qc.h(0)

//     # Bob's measurement
//     if bob_bases[i] == 'X':
//         qc.h(0)
//     qc.measure(0, 0)
//     circuits.append(qc)

// # -------------------------------
// # STEP 4: Run simulation
// # -------------------------------
// # Use AerSimulator for simulation in Qiskit 2.0
// simulator = AerSimulator()
// compiled = transpile(circuits, simulator)
// job = simulator.run(compiled, shots=1024)
// result = job.result()

// bob_results = []
// for i in range(N_BITS):
//     counts = result.get_counts(circuits[i])
//     measured_bit = int(max(counts, key=counts.get))  # Get most likely bit
//     bob_results.append(measured_bit)

// # -------------------------------
// # STEP 5: Sifted key creation
// # -------------------------------
// sifted_key_alice = []
// sifted_key_bob = []
// matching_indices = []

// for i in range(N_BITS):
//     if alice_bases[i] == bob_bases[i]:
//         matching_indices.append(i)
//         sifted_key_alice.append(alice_bits[i])
//         sifted_key_bob.append(bob_results[i])

// # -------------------------------
// # STEP 6: QBER Calculation
// # -------------------------------
// errors = sum([a != b for a, b in zip(sifted_key_alice, sifted_key_bob)])
// qber = errors / len(sifted_key_alice) if sifted_key_alice else 0

// # -------------------------------
// # STEP 7: Key Verification (simulated public check)
// # -------------------------------
// VERIFICATION_SAMPLE = 5
// sample_indices = random.sample(range(len(sifted_key_alice)), min(VERIFICATION_SAMPLE, len(sifted_key_alice)))
// sample_matches = [sifted_key_alice[i] == sifted_key_bob[i] for i in sample_indices]

// verified = all(sample_matches)
// final_key = [sifted_key_alice[i] for i in range(len(sifted_key_alice)) if i not in sample_indices] if verified else []

// # -------------------------------
// # RESULTS DISPLAY
// # -------------------------------
// print("\n--- BB84 Quantum Key Distribution ---")
// print("Eavesdropping Enabled:", EAVESDROP)
// print("Total bits sent:       ", N_BITS)
// print("Matching bases:        ", len(matching_indices))
// print("Errors in matching:    ", errors)
// print("QBER:                  ", round(qber * 100, 2), "%")
// print("Sample verified:", "Passed" if verified else "Failed")
// print("Final Key (length = {}):".format(len(final_key)), final_key)

// # Optional: Plot histogram of one measurement
// plot_histogram(result.get_counts(circuits[0]))
// plt.title("Measurement Histogram of First Qubit")
// plt.show()


// # --- BB84 Quantum Key Distribution ---
// # Eavesdropping Enabled: False
// # Total bits sent:        50
// # Matching bases:         28
// # Errors in matching:     0
// # QBER:                   0.0 %
// # Sample verified: Passed
// # Final Key (length = 23): [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]

// i want this to run and show output where this fuction is in a file which is routed through app.py in a specfic endpoint from frontend where the 