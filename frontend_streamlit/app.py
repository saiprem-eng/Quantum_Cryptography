import streamlit as st
import requests

# Title of the app
st.title("Quantum Simulation Input")

# Selection between two options (e.g., Simulation vs Real-time)
box_choice = st.selectbox("Choose Box", ["Select a Box", "Box 1 (Simulation)", "Box 2 (Real-Time)"])

# Only show the input fields after a box is selected
if box_choice != "Select a Box":
    # Input fields for Alice's bits and bases
    alice_bits = []
    alice_bases = []

    # Collecting 6 bits as text input
    st.write("Enter 6 Alice's Bits (0 or 1):")
    for i in range(6):
        bit = st.text_input(f"Bit {i+1}", key=f"bit_{i}")
        alice_bits.append(bit)

    # Collecting 6 bases as text input
    st.write("Enter 6 Alice's Bases (X or Z):")
    for i in range(6):
        base = st.text_input(f"Base {i+1}", key=f"base_{i}")
        alice_bases.append(base)

    # Eve Intercept option
    eve_intercept = st.radio("Does Eve intercept?", ["True", "False"])

    # Define backend API endpoint based on the box selection
    if box_choice == "Box 1 (Simulation)":
        endpoint = "http://localhost:8000/run_simulation"
        plot_endpoint = "http://localhost:8000/bloch_visualization"
    elif box_choice == "Box 2 (Real-Time)":
        endpoint = "http://localhost:8000/run_on_real_device"
        plot_endpoint = "http://localhost:8000/bloch_visualization"

    # When the button is pressed, send the data to the backend
    if st.button("Submit"):
        # Prepare the data to send to the backend
        data = {
            "alice_bits": alice_bits,
            "alice_bases": alice_bases,
            "eve_intercept": eve_intercept
        }
        print(f"data: {data}")

        # Send the data to the backend API via POST request
        try:
            response = requests.post(endpoint, json=data)
            if response.status_code == 200:
                st.success("Data successfully sent to the backend!")
                st.write(response.json())  # Display response from backend
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to send data: {str(e)}")

     # Generate Bloch Sphere plot button
    if st.button("Generate Bloch Sphere"):
        # Send the same data to the plot endpoint to generate the Bloch Sphere
        try:
            data = {
            "alice_bits": alice_bits,
            "alice_bases": alice_bases,
            "eve_intercept": eve_intercept
            }
            plot_response = requests.post(plot_endpoint, json=data)
            if plot_response.status_code == 200:
                # Display the Bloch Sphere plot
                st.success("Bloch Sphere Generated!")
                # Assuming the backend sends the plot as an image URL or base64 data
                st.image(plot_response.content)  # Display the image received from the backend
            else:
                st.error(f"Error generating Bloch Sphere: {plot_response.status_code}")
        except Exception as e:
            st.error(f"Failed to generate Bloch Sphere: {str(e)}")

else:
    st.write("Please select either Box 1 or Box 2 to begin.")
