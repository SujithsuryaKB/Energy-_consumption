import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample energy consumption data
# In practice, this could be replaced with data from a database or sensors
data = pd.DataFrame({
    'device': ['AC', 'Heater', 'Lights', 'Refrigerator', 'Washing Machine'],
    'power_rating_kw': [1.5, 2.0, 0.5, 0.8, 1.2],
    'hours_used': [8, 4, 12, 24, 2]
})

def calculate_energy_consumption():
    """
    Calculate energy consumption for each device.
    Energy consumption (kWh) = Power Rating (kW) * Hours Used
    """
    data['energy_consumed_kwh'] = data['power_rating_kw'] * data['hours_used']
    return data

@app.route('/energy-data', methods=['GET'])
def get_energy_data():
    """
    API endpoint to fetch energy consumption data.
    """
    try:
        energy_data = calculate_energy_consumption()
        return jsonify(energy_data.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add-device', methods=['POST'])
def add_device():
    """
    Add a new device to the energy tracking system.
    """
    try:
        new_device = request.json
        data.loc[len(data)] = [
            new_device['device'],
            new_device['power_rating_kw'],
            new_device['hours_used'],
            0  # Placeholder for energy consumed, recalculated dynamically
        ]
        return jsonify({'message': 'Device added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
