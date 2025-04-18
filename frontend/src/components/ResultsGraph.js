import React from 'react';
import Plot from 'react-plotly.js';

const ResultsGraph = ({ results }) => {
  return (
    <div>
      <h3>Measurement Results</h3>
      <Plot
        data={results}
        layout={{ title: 'Measurement Results' }}
      />
    </div>
  );
};

export default ResultsGraph;
