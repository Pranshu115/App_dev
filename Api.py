from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

from flask import Flask, request, jsonify
import App_code  # Import the existing code file as a module

app = Flask(__name__)

# Load existing data when the API starts
App_code.load_data()

@app.route('/add_race_result', methods=['POST'])
def add_race_result():
    data = request.get_json()
    name = data.get('name')
    timing = data.get('timing')

    if not name or timing is None:
        return jsonify({"error": "Name and timing are required."}), 400

    try:
        timing = float(timing)
        App_code.add_race_result(name, timing)
        return jsonify({"message": "Race result added successfully."}), 200
    except ValueError:
        return jsonify({"error": "Invalid timing. It must be a number."}), 400

@app.route('/view_performance/<string:name>', methods=['GET'])
def view_performance(name):
    user_results = [entry for entry in App_code.race_data if entry['name'].lower() == name.lower()]

    if not user_results:
        return jsonify({"error": f"No data found for {name}."}), 404

    total_races = len(user_results)
    below_threshold = sum(1 for result in user_results if result["status"] == "Below Threshold")
    above_threshold = total_races - below_threshold
    average_timing = sum(result["timing"] for result in user_results) / total_races

    response = {
        "name": name,
        "total_races": total_races,
        "average_timing": average_timing,
        "below_threshold": below_threshold,
        "above_threshold": above_threshold,
        "details": user_results
    }
    return jsonify(response), 200

@app.route('/get_all_race_data', methods=['GET'])
def get_all_race_data():
    return jsonify(App_code.race_data), 200

@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running."}), 200

if __name__ == '__main__':
    app.run(debug=True)
