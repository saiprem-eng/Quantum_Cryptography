
// import React, { useState } from 'react';
// import QuantumCircuit from './components/QuantumCircuit';
// import BlochSphere from './components/BlochSphere';
// import ResultsGraph from './components/ResultsGraph';
// import BB84Form from './components/run_simulation'; // Import your new component
// import Controls from './components/Controls';

// const App = () => {
//   const [simulationData, setSimulationData] = useState(null);
//   const [show,setShow] = useState('');

//   // This function will receive the data and trigger the simulation
//   // const handleRunSimulation = async (params) => {
//   //   try {
//   //     const response = await run_simulation(params); // Call your RunSimulation component here
//   //     setSimulationData(response.data);
//   //   } catch (error) {
//   //     console.error('Simulation error:', error);
//   //   }
//   // };

//   const handleSimulationClick = () => {setShow('Simulation')};
//   const handleRealTimeClick = () => {setShow('Realtime')};

//   return (
//     <div>
//       <h1>Quantum Key Distribution Simulation</h1>
//       {/* You can pass the handleRunSimulation function to Controls */}
//       {/* <Controls onRunSimulation={handleRunSimulation} /> */}
//       <div>Choose one</div>
//       <button onClick={handleSimulationClick}>Simulation</button>
//       <button onClick={handleRealTimeClick}>Real Time</button>
//       {show === 'Simulation' && <div>{show}<BB84Form  /></div>}
//       {show === 'Realtime' && <div>{show}<Controls  /> </div>}
//       {/* <BB84Form/> */}
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

//working
// src/App.js
// import React, { useState } from 'react';
// import QuantumCircuit from './components/QuantumCircuit';
// // import BlochSphere from './components/BlochSphere';
// import ResultsGraph from './components/ResultsGraph';
// import BB84Form from './components/run_simulation';
// import Controls from './components/Controls';
// import BlochVectorsPlot from './components/BlochSphere'; // ✅ Import your Plotly component

// const App = () => {
//   const [simulationData, setSimulationData] = useState(null);
//   const [show, setShow] = useState('');

//   const handleSimulationClick = () => setShow('Simulation');
//   const handleRealTimeClick = () => setShow('Realtime');

//   return (
//     <div>
//       <h1>Quantum Key Distribution Simulation</h1>

//       <div>Choose one</div>
//       <button onClick={handleSimulationClick}>Simulation</button>
//       <button onClick={handleRealTimeClick}>Real Time</button>

//       {/* Show Simulation Components */}
//       {show === 'Simulation' && (
//         <div>
//           <h2>Simulation Mode</h2>
//           <BB84Form />
//         </div>
//       )}

//       {/* Show Realtime Components */}
//       {show === 'Realtime' && (
//         <div>
//           <h2>Real-Time Mode</h2>
//           <Controls />
//           <BlochVectorsPlot /> {/* ✅ Add your Plotly component here */}
//         </div>
//       )}

//       {/* Show circuit + bloch + result graph if simulationData exists */}
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

//working
// import React, { useState } from 'react';
// import QuantumCircuit from './components/QuantumCircuit';
// import ResultsGraph from './components/ResultsGraph';
// import BB84Form from './components/run_simulation';
// import Controls from './components/Controls';
// import BlochVisualization from './components/BlochSphere'; // Import BlochVisualization component

// const App = () => {
//   const [simulationData, setSimulationData] = useState(null);
//   const [show, setShow] = useState('');

//   const handleSimulationClick = () => setShow('Simulation');
//   const handleRealTimeClick = () => setShow('Realtime');

//   return (
//     <div>
//       <h1>Quantum Key Distribution Simulation</h1>

//       <div>Choose one</div>
//       <button onClick={handleSimulationClick}>Simulation</button>
//       <button onClick={handleRealTimeClick}>Real Time</button>

//       {/* Show Simulation Components */}
//       {show === 'Simulation' && (
//         <div>
//           <h2>Simulation Mode</h2>
//           <BB84Form />
//         </div>
//       )}

//       {/* Show Realtime Components */}
//       {show === 'Realtime' && (
//         <div>
//           <h2>Real-Time Mode</h2>
//           <Controls />
//           <BlochVisualization /> {/* Add BlochVisualization to show the image */}
//         </div>
//       )}

//       {/* Show circuit + bloch + result graph if simulationData exists */}
//       {simulationData && (
//         <>
//           <QuantumCircuit data={simulationData.circuitData} />
//           <ResultsGraph results={simulationData.results} />
//         </>
//       )}
//     </div>
//   );
// };

// export default App;


import React, { useState } from 'react';
import QuantumCircuit from './components/QuantumCircuit';
import ResultsGraph from './components/ResultsGraph';
import BB84Form from './components/run_simulation';
import Controls from './components/Controls';
import BlochVisualization from './components/BlochSphere';
import axios from "axios";

const App = () => {
  const [simulationData, setSimulationData] = useState(null);
  const [show, setShow] = useState('');
  const [imageSrc, setImageSrc] = useState(null);

  const handleSimulationClick = () => setShow('Simulation');
  const handleRealTimeClick = () => setShow('Realtime');

  const handleRunSimulation = async (data) => {
    try {
      const response = await fetch('http://localhost:8000/run_simulation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        console.log('✅ Simulation Success:', result);
        setSimulationData(result);  // Store result to show in visualizations
      } else {
        console.error('❌ API Error:', result.message);
      }
    } catch (error) {
      console.error('❌ Network or Server Error:', error);
    }
  };

  const handleGenerateBlochSphere = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/test_bloch", {
        responseType: "blob",
      });

      const imageBlob = response.data;
      const imageUrl = URL.createObjectURL(imageBlob);
      setImageSrc(imageUrl);
    } catch (error) {
      console.error("Error generating Bloch sphere:", error);
    }
  };

  return (
    <div>
      <h1>Quantum Key Distribution Simulation</h1>

      <div>Choose one</div>
      <button onClick={handleSimulationClick}>Simulation</button>
      <button onClick={handleRealTimeClick}>Real Time</button>

      {show === 'Simulation' && (
        <div>
          <h2>Simulation Mode</h2>
          <BB84Form />
          <button onClick={handleGenerateBlochSphere}>Generate Bloch Sphere</button>
          {imageSrc && <img src={imageSrc} alt="Bloch Sphere" style={{ marginTop: "20px" }} />}
        </div>
      )}

      {show === 'Realtime' && (
        <div>
          <h2>Real-Time Mode</h2>
          <Controls onRunSimulation={handleRunSimulation} />
          <button onClick={handleGenerateBlochSphere}>Generate Bloch Sphere</button>
          {imageSrc && <img src={imageSrc} alt="Bloch Sphere" style={{ marginTop: "20px" }} />}
        </div>
      )}

      {simulationData && (
        <>
          <QuantumCircuit data={simulationData.circuitData} />
          <ResultsGraph results={simulationData.results} />
        </>
      )}
    </div>
  );
};

export default App;

