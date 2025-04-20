// src/BlochSphere.js
import React, { useState } from "react";
import axios from "axios";

function BlochSphere() {
    const [imageSrc, setImageSrc] = useState(null); // Store image src in state

    const handleGenerateBlochSphere = async () => {
        try {
            // Make a GET request to the FastAPI endpoint
            const response = await axios.get("http://127.0.0.1:8000/test_bloch", {
                responseType: "blob", // Important to specify responseType as blob
            });

            // Create an object URL from the response
            const imageBlob = response.data;
            const imageUrl = URL.createObjectURL(imageBlob);

            // Set the image URL to be displayed in the state
            setImageSrc(imageUrl);
        } catch (error) {
            console.error("Error generating Bloch sphere:", error);
        }
    };

    return (
        <div>
            <h1>Generate Bloch Sphere</h1>
            <button onClick={handleGenerateBlochSphere}>Generate Bloch Sphere</button>

            {/* Display the Bloch Sphere image if it exists */}
            {imageSrc && <img src={imageSrc} alt="Bloch Sphere" style={{ marginTop: "20px" }} />}
        </div>
    );
}

export default BlochSphere;
