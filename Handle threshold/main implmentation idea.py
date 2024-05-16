from flask import jsonify

@app.route('/get-threshold-values', methods=['GET'])
def get_threshold_values():
    # Retrieve the threshold values from wherever they are stored
    threshold_values = {
        'temperature_lower_threshold': temperature_lower_threshold,
        'humidity_lower_threshold': humidity_lower_threshold,
        'humidity_upper_threshold': humidity_upper_threshold,
        'CO2_upper_threshold': CO2_upper_threshold
    }
    # Return the threshold values as a JSON response
    return jsonify(threshold_values)
