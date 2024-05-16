from flask import Flask, render_template, request, redirect, jsonify
import requests  # Import requests library for sending POST requests

# Other imports and initialization...

app = Flask(__name__)

# Existing routes...

# Route to save threshold values
@app.route('/save-threshold-values', methods=['POST'])
def save_threshold_values():
    global temperature_lower_threshold, humidity_lower_threshold, humidity_upper_threshold, CO2_upper_threshold
    
    # Get the threshold values from the POST request
    temperature_lower_threshold = float(request.form['temperature_lower_threshold'])
    humidity_lower_threshold = float(request.form['humidity_lower_threshold'])
    humidity_upper_threshold = float(request.form['humidity_upper_threshold'])
    CO2_upper_threshold = float(request.form['CO2_upper_threshold'])
    
    # Send the threshold values to the function in the other Python file
    send_threshold_values_to_other_file(temperature_lower_threshold, humidity_lower_threshold, humidity_upper_threshold, CO2_upper_threshold)
    
    # Redirect or respond as needed
    return redirect('/')  # Redirect to the homepage or respond with a success message

# Method to send threshold values to the other Python file
def send_threshold_values_to_other_file(temperature_lower_threshold, humidity_lower_threshold, humidity_upper_threshold, CO2_upper_threshold):
    # Define the URL of the endpoint in the other Python file
    url = 'http://localhost:5003/update-threshold-values'
    
    # Prepare the data to send in the POST request
    data = {
        'temperature_lower_threshold': temperature_lower_threshold,
        'humidity_lower_threshold': humidity_lower_threshold,
        'humidity_upper_threshold': humidity_upper_threshold,
        'CO2_upper_threshold': CO2_upper_threshold
    }
    
    # Send a POST request to the other Python file
    response = requests.post(url, data=data)
    
    # Handle the response as needed (e.g., check for success)
    if response.status_code == 200:
        print('Threshold values successfully sent to the other Python file')
    else:
        print('Failed to send threshold values to the other Python file')

# Existing routes and Flask initialization...
