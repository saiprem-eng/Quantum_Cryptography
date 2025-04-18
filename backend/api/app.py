from flask import Flask, request, jsonify
import os, sys
from flask_cors import CORS  # Import CORS
# Adding the parent folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantum_simulation import run_simulation, run_on_real_device

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return "Welcome to the Quantum Simulation API!"

@app.route('/run_simulation', methods=['POST'])
def run_simulation_route():
    try:
        data = request.json

        # Validate required keys
        if 'alice_bit' not in data or 'alice_base' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: alice_bit and/or alice_base'
            }), 400

        # Run simulation with validated input
        result = run_simulation(data)
        return jsonify({
            'status': 'success',
            'message': 'Simulation completed successfully',
            'data': result
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while processing the simulation: {str(e)}'
        }), 500


@app.route('/run_on_real_device', methods=['POST'])
def run_on_real_device_route():
    data = request.json
    result = run_on_real_device(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
