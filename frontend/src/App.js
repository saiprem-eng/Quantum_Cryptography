// import React, { useState } from 'react';
// import QuantumCircuit from './components/QuantumCircuit';
// import BlochSphere from './components/BlochSphere';
// import ResultsGraph from './components/ResultsGraph';
// import Controls from './components/Controls';
// import axios from 'axios';


// const App = () => {
//   const [simulationData, setSimulationData] = useState(null);

//   const runSimulation = async (params) => {
//     const response = await axios.post('http://localhost:5000/run_simulation', params);
//     setSimulationData(response.data);
//   };

//   return (
//     <div>
//       <h1>Quantum Key Distribution Simulation</h1>
//       <Controls onRunSimulation={runSimulation} />
//       {simulationData && (
//         <>
//           <QuantumCircuit data={simulationData.circuitData} />
//           <BlochSphere qubitState={simulationData.qubitState} />
//           <ResultsGraph results={simulationData.results} />
//         </>
//       )}
//     </div>
//   );
// };

// export default App;


import React, { useState } from 'react';
import QuantumCircuit from './components/QuantumCircuit';
import BlochSphere from './components/BlochSphere';
import ResultsGraph from './components/ResultsGraph';
import BB84Form from './components/run_simulation'; // Import your new component
import Controls from './components/Controls';

const App = () => {
  const [simulationData, setSimulationData] = useState(null);
  const [show,setShow] = useState('');

  // This function will receive the data and trigger the simulation
  // const handleRunSimulation = async (params) => {
  //   try {
  //     const response = await run_simulation(params); // Call your RunSimulation component here
  //     setSimulationData(response.data);
  //   } catch (error) {
  //     console.error('Simulation error:', error);
  //   }
  // };

  const handleSimulationClick = () => {setShow('Simulation')};
  const handleRealTimeClick = () => {setShow('Realtime')};

  return (
    <div>
      <h1>Quantum Key Distribution Simulation</h1>
      {/* You can pass the handleRunSimulation function to Controls */}
      {/* <Controls onRunSimulation={handleRunSimulation} /> */}
      <div>Choose one</div>
      <button onClick={handleSimulationClick}>Simulation</button>
      <button onClick={handleRealTimeClick}>Real Time</button>
      {show === 'Simulation' && <div>{show}<BB84Form  /></div>}
      {show === 'Realtime' && <div>{show}<Controls  /> </div>}
      {/* <BB84Form/> */}
      {simulationData && (
        <>
          <QuantumCircuit data={simulationData.circuitData} />
          <BlochSphere qubitState={simulationData.qubitState} />
          <ResultsGraph results={simulationData.results} />
        </>
      )}
    </div>
  );
};

export default App;
