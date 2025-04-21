// import React, { useState } from 'react';

// function BB84Form() {
//   const [aliceBit, setAliceBit] = useState(null);
//   const [aliceBase, setAliceBase] = useState('');
//   const [eveBase, setEveBase] = useState(false); // Added Eve's base state

//   // Handle form submission
//   const handleSubmit = async (e) => {
//     e.preventDefault();  // Prevent the default form submission

//     // Create the data object
//     const data = {
//       alice_bit: aliceBit,
//       alice_base: aliceBase,
//     };

//     try {
//       const response = await fetch('http://localhost:8000/run_simulation', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//       });
  
//       const result = await response.json();
  
//       if (response.ok) {
//         console.log('✅ Simulation Success:', result);
//         // alert(`Simulation Success: ${JSON.stringify(result.data)}`);
//         // Optionally set state to render on UI
//         // setSimulationData(result.data);
//       } else {
//         console.error('❌ API Error:', result.message);
//         // alert(`API Error: ${result.message}`);
//       }
//     } catch (error) {
//       console.error('❌ Network or Server Error:', error);
//       // alert('Network or Server Error. Please try again later.');
//     }
//   };

//   const handleChange = (e) => {
//     setEveBase(e.target.value === 'true');
//   };

//   return (
//     <div>
//       <h2>BB84 Protocol</h2>
//       <form onSubmit={handleSubmit}>
//         <label>
//           Alice Bit (0 or 1):
//           <input
//             type="number"
//             value={aliceBit}
//             onChange={(e) => setAliceBit(Number(e.target.value))}
//             min="0"
//             max="1"
//           />
//         </label>
//         <label>
//           Alice Bit (0 or 1):
//           <input
//             type="number"
//             value={aliceBit}
//             onChange={(e) => setAliceBit(Number(e.target.value))}
//             min="0"
//             max="1"
//           />
//         </label>
//         <label>
//           Alice Bit (0 or 1):
//           <input
//             type="number"
//             value={aliceBit}
//             onChange={(e) => setAliceBit(Number(e.target.value))}
//             min="0"
//             max="1"
//           />
//         </label>
//         <label>
//           Alice Bit (0 or 1):
//           <input
//             type="number"
//             value={aliceBit}
//             onChange={(e) => setAliceBit(Number(e.target.value))}
//             min="0"
//             max="1"
//           />
//         </label>
//         <br />
//         <label>
//           Alice Base (Z or X):
//           <input
//             type="text"
//             value={aliceBase}
//             onChange={(e) => setAliceBase(e.target.value)}
//             placeholder="Z or X"
//           />
//         </label>
//         <label>
//           Alice Base (Z or X):
//           <input
//             type="text"
//             value={aliceBase}
//             onChange={(e) => setAliceBase(e.target.value)}
//             placeholder="Z or X"
//           />
//         </label>
//         <label>
//           Alice Base (Z or X):
//           <input
//             type="text"
//             value={aliceBase}
//             onChange={(e) => setAliceBase(e.target.value)}
//             placeholder="Z or X"
//           />
//         </label>
//         <label>
//           Alice Base (Z or X):
//           <input
//             type="text"
//             value={aliceBase}
//             onChange={(e) => setAliceBase(e.target.value)}
//             placeholder="Z or X"
//           />
//         </label>
//         <br />
//         <label>
//         <span>Enable Eve Base: </span>
//         <input
//           type="radio"
//           value="true"
//           checked={eveBase === true}
//           onChange={handleChange}
//         />
//         True
//       </label>

//       <label style={{ marginLeft: '1rem' }}>
//       <span>Disable Eve Base: </span>
//         <input
//           type="radio"
//           value="false"
//           checked={eveBase === false}
//           onChange={handleChange}
//         />
//         False
//       </label>
//         <br />
//         <button type="submit">Run Simulation</button>
//       </form>
//     </div>
//   );
// }

// export default BB84Form;

import React, { useState } from 'react';

function BB84Form() {
  const [aliceBits, setAliceBits] = useState([0, 0, 0, 0]);
  const [aliceBases, setAliceBases] = useState(['Z', 'Z', 'Z', 'Z']);
  const [eveBase, setEveBase] = useState(false); // Added Eve's base state

  // Handle form submission
const handleRunSimulation = async (payload) => {
  try {
    // Select the URL based on the flag in the payload
    const url = payload.isRealDevice
      ? 'http://localhost:8000/run_on_real_device' // For real device
      : 'http://localhost:8000/run_simulation'; // For simulation

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        alice_bit: payload.alice_bit,
        alice_base: payload.alice_base,
      }),
    });

    const result = await response.json();
    console.log('Simulation result:', result);
  } catch (error) {
    console.error('Error running simulation:', error);
  }
};);

      const result = await response.json();

      if (response.ok) {
        console.log('✅ Simulation Success:', result);
      } else {
        console.error('❌ API Error:', result.message);
      }
    } catch (error) {
      console.error('❌ Network or Server Error:', error);
    }
  };

  const handleChange = (e) => {
    setEveBase(e.target.value === 'true');
  };

  const handleBitChange = (index, value) => {
    const updatedBits = [...aliceBits];
    updatedBits[index] = parseInt(value, 10);
    setAliceBits(updatedBits);
  };

  const handleBaseChange = (index, value) => {
    const updatedBases = [...aliceBases];
    updatedBases[index] = value;
    setAliceBases(updatedBases);
  };

  return (
    <div>
      <h2>BB84 Protocol</h2>
      <form onSubmit={handleSubmit}>
        {aliceBits.map((bit, index) => (
          <label key={`bit-${index}`}>
            Alice Bit {index + 1} (0 or 1):
            <select
              value={bit}
              onChange={(e) => handleBitChange(index, e.target.value)}
            >
              <option value="0">0</option>
              <option value="1">1</option>
            </select>
          </label>
        ))}

        <br />

        {aliceBases.map((base, index) => (
          <label key={`base-${index}`}>
            Alice Base {index + 1} (Z or X):
            <input
              type="text"
              value={base}
              onChange={(e) => handleBaseChange(index, e.target.value)}
              placeholder="Z or X"
            />
          </label>
        ))}

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
