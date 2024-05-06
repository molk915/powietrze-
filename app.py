from flask import Flask, request, jsonify
from datetime import datetime
import os
from typing import Dict, Any
from airvisual_client import AirVisualClient

app = Flask(__name__)
data_store: Dict[str, Dict[str, Any]] = {}
api_key = os.environ.get('AIRVISUAL_API_KEY')
client = AirVisualClient(api_key)
@app.route('/weather-pollution', methods=['POST'])
def add_weather_pollution_data():
    data = request.json
    if 'temperature' not in data or 'pressure' not in data or 'pollution_level' not in data:
        return jsonify({'error': 'Missing data fields'}), 400
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_store[timestamp] = data
    return jsonify({'message': 'Data added successfully'}), 201
@app.route('/weather-pollution/<date_time>', methods=['GET'])
def get_weather_pollution_data(date_time):
    closest_timestamp = min(data_store.keys(), key=lambda x: abs(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(x, '%Y-%m-%d %H:%M:%S')))
    return jsonify(data_store[closest_timestamp])

@app.route('/city-pollution/<city>', methods=['GET'])
def get_city_pollution(city):
    city_pollution_data = client.get_city_pollution(city)
    return jsonify(city_pollution_data)

if __name__ == '__main__':
    app.run(debug=True)
