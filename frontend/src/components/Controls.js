import React, { useState } from 'react';

const Controls = ({ onRunSimulation }) => {
  const [aliceBits, setAliceBits] = useState([0, 0, 0, 0]);
  const [aliceBases, setAliceBases] = useState(['Z', 'Z', 'Z', 'Z']);

  const handleBitChange = (index, value) => {
    const updatedBits = [...aliceBits];
    updatedBits[index] = parseInt(value);
    setAliceBits(updatedBits);
  };

  const handleBaseChange = (index, value) => {
    const updatedBases = [...aliceBases];
    updatedBases[index] = value;
    setAliceBases(updatedBases);
  };

  const handleRun = () => {
    // Log the payload before sending it
    const payload = { alice_bit: aliceBits, alice_base: aliceBases };
    console.log("Payload being sent to backend:", payload);

    onRunSimulation(payload);
  };

  return (
    <div>
      <h3>Controls</h3>
      {aliceBits.map((bit, index) => (
        <div key={index}>
          <label>
            Alice's Bit {index + 1}:{' '}
            <input
              type="number"
              value={bit}
              onChange={(e) => handleBitChange(index, e.target.value)}
              min="0"
              max="1"
            />
          </label>
          <label>
            Alice's Base {index + 1}:{' '}
            <select
              value={aliceBases[index]}
              onChange={(e) => handleBaseChange(index, e.target.value)}
            >
              <option value="Z">Z</option>
              <option value="X">X</option>
            </select>
          </label>
        </div>
      ))}
      <button onClick={handleRun}>Run Simulation</button>
    </div>
  );
};

export default Controls;
