import React, { useEffect } from 'react';

const BlochSphere = ({ qubitState }) => {
  useEffect(() => {
    const bloch = new Bloch();
    bloch.add_states(qubitState);
    bloch.show();
  }, [qubitState]);

  return <div id="bloch-sphere"></div>;
};

export default BlochSphere;
