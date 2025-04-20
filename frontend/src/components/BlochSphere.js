import React, { useState } from "react";

function BlochVisualization() {
    const [aliceBits, setAliceBits] = useState([0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1]); // Example bits
    const [aliceBases, setAliceBases] = useState(['Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X']); // Example bases
    const [imageUrl, setImageUrl] = useState(null); // State to store image URL

    const fetchBlochImage = async () => {
        try {
            const response = await fetch('/bloch_visualization', {
                method: 'POST',
                body: JSON.stringify({ alice_bits: aliceBits, alice_bases: aliceBases }),
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) {
                throw new Error("Failed to fetch the image");
            }

            const blob = await response.blob(); // Convert response to Blob (image)
            const imageUrl = URL.createObjectURL(blob); // Create URL for the image Blob
            setImageUrl(imageUrl); // Set the image URL in state
        } catch (error) {
            console.error("Error fetching Bloch image:", error);
        }
    };

    return (
        <div>
            <h1>Bloch Sphere Visualization</h1>
            <button onClick={fetchBlochImage}>Generate Bloch Sphere</button>
            {imageUrl && <img src={imageUrl} alt="Bloch Sphere" style={{ width: "100%", height: "auto" }} />}
        </div>
    );
}

export default BlochVisualization;
