import React, { useState } from 'react';

const Controls = ({ onRunSimulation }) => {
  const [aliceBit, setAliceBit] = useState(0);
  const [aliceBase, setAliceBase] = useState('Z');

  const handleRun = () => {
    onRunSimulation({ aliceBit, aliceBase });
  };

  return (
    <div>
      <h3>Controls</h3>
      <label>
        Alice's Bit: 
        <input type="number" value={aliceBit} onChange={(e) => setAliceBit(e.target.value)} />
      </label>
      <label>
        Alice's Base:
        <select value={aliceBase} onChange={(e) => setAliceBase(e.target.value)}>
          <option value="Z">Z</option>
          <option value="X">X</option>
        </select>
      </label>
      <button onClick={handleRun}>Run Simulation</button>
    </div>
  );
};

export default Controls;
