# from flask import Flask, request, jsonify, send_file
# import os, sys
# from flask_cors import CORS  # Import CORS
# # Adding the parent folder to the system path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from quantum_simulation import run_simulation, run_on_real_device
# from bloch_sphere import plot_sphere

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# @app.route('/')
# def index():
#     return "Welcome to the Quantum Simulation API!"

# @app.route('/run_simulation', methods=['POST'])
# def run_simulation_route():
#     try:
#         data = request.json

#         # Validate required keys
#         if 'alice_bit' not in data or 'alice_base' not in data:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'Missing required fields: alice_bit and/or alice_base'
#             }), 400

#         # Run simulation with validated input
#         result = run_simulation(data)
#         return jsonify({
#             'status': 'success',
#             'message': 'Simulation completed successfully',
#             'data': result
#         }), 200

#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': f'An error occurred while processing the simulation: {str(e)}'
#         }), 500


# @app.route('/bloch_visualization', methods=['POST'])
# def plot_bloch_from_data():
#     try:
#         # Get data from the request
#         data = request.json
#         alice_bits = data.get('alice_bits')
#         alice_bases = data.get('alice_bases')

#         # Check if both 'alice_bits' and 'alice_bases' are provided
#         if not alice_bits or not alice_bases:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'Missing required fields: alice_bits and/or alice_bases'
#             }), 400

#         # Call the function from bloch_sphere.py to generate the Bloch sphere plot
#         img_io = plot_sphere(alice_bits, alice_bases)

#         # Return the image as a response to the frontend
#         return send_file(img_io, mimetype='image/png', as_attachment=False, download_name="bloch_spheres.png")

#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': f'Error generating Bloch sphere: {str(e)}'
#         }), 500


# @app.route('/run_on_real_device', methods=['POST'])
# def run_on_real_device_route():
#     data = request.json
#     result = run_on_real_device(data)
#     return jsonify(result)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001, debug=True)


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import os, sys
from typing import List, Optional

# Adding the parent folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantum_simulation import run_simulation, run_on_real_device
from bloch_sphere import plot_sphere

# Create FastAPI app
app = FastAPI()

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:8501"],  # Allow all origins, adjust as necessary
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models for validation
class SimulationRequest(BaseModel):
    alice_bits: list[int]
    alice_bases: list[str]
    EAVESDROP: Optional[bool] = False
    EVE_INTERCEPT_RATE: Optional[float] = 1.0

class BlochVisualizationRequest(BaseModel):
    alice_bits: list[int]
    alice_bases: list[str]

@app.get('/')
async def index():
    return {"message": "Welcome to the Quantum Simulation API!"}

@app.post('/run_simulation')
async def run_simulation_route(data: SimulationRequest):
    try:
        print(f"data is :{data}")
        # Run simulation with validated input
        result = run_simulation(data.model_dump())
        
        print(f"result : {result}")
        return JSONResponse({
            'status': 'success',
            'message': 'Simulation completed successfully',
            'data': result
        }, status_code=200)

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f'An error occurred while processing the simulation: {str(e)}'
    #     )
    
    except Exception as e:
        import traceback
        traceback.print_exc()  # This prints the full error to console
        raise HTTPException(
            status_code=500,
            detail=f'An error occurred: {str(e)}'
        )


@app.post('/bloch_visualization')
async def plot_bloch_from_data(data: BlochVisualizationRequest):
    try:
        print(f"The data here {data}")
        # If data is a Pydantic model, access attributes like this
        img_io = plot_sphere(data.alice_bits, data.alice_bases)

        return StreamingResponse(img_io, media_type='image/png')

    except Exception as e:
        import traceback
        traceback.print_exc()  # This prints the full error traceback to the console
        raise HTTPException(
            status_code=500,
            detail=f'Error generating Bloch sphere: {str(e)}'
        )
    
@app.post('/run_on_real_device')
async def run_on_real_device_route(data: dict):
    try:
        result = run_on_real_device(data)
        
        return JSONResponse(result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error interacting with real device: {str(e)}'
        )

@app.get("/test_bloch")
async def test_bloch():
    alice_bits = [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0]
    alice_bases = ['X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z', 'X', 'Z']
    
    try:
        # Generate the Bloch sphere image
        img_io = plot_sphere(alice_bits, alice_bases)
        
        # Return the image as a response using StreamingResponse
        return StreamingResponse(img_io, media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))