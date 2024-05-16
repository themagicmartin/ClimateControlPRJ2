import threading                                            
import serial                                               
import time                                                 
from datetime import datetime, timedelta                    
import matplotlib.pyplot as plt                             
from flask import Flask, render_template, request, redirect, jsonify

serialInst = serial.Serial('/dev/tty.usbmodem1101', 115200)  # Port and baudrate. On mac terminal: ls /dev/tty.*
time.sleep(2)  # Allow time for Arduino to initialize

app = Flask(__name__)

# Initialize threshold values
temperature_lower_threshold = 10.0
humidity_lower_threshold = 30.0
humidity_upper_threshold = 70.0
CO2_upper_threshold = 2000.0

# Initialize thresholds with initial values
initial_temperature_lower_threshold = temperature_lower_threshold
initial_humidity_lower_threshold = humidity_lower_threshold
initial_humidity_upper_threshold = humidity_upper_threshold
initial_CO2_upper_threshold = CO2_upper_threshold

# Flask initiation
@app.route('/')
def index():
    # Default image path
    image_path = 'static/images/minute.png'
    with open('/Users/Martin/Desktop/Webserver/static/averages.txt', 'r') as file:
        averages_text = file.read()
    return render_template('base.html', image_path=image_path, averages_text=averages_text, temperature_lower_threshold=temperature_lower_threshold,humidity_lower_threshold=humidity_lower_threshold,humidity_upper_threshold=humidity_upper_threshold,CO2_upper_threshold=CO2_upper_threshold)

# Graph handler !! Notice path of images, and naming of these
@app.route('/change-image', methods=['POST'])
def change_image():
    action = request.form['action']
    if action == 'minute':
        image_path = 'static/images/minute.png'
    elif action == 'hourly':
        image_path = 'static/images/hourly.png'
    elif action == 'daily':
        image_path = 'static/images/daily.png'
    else:
        image_path = 'static/images/minute.png'  # Default image path
    with open('/Users/Martin/Desktop/Webserver/static/averages.txt', 'r') as file:
        averages_text = file.read()
    return render_template('base.html', image_path=image_path, averages_text=averages_text, temperature_lower_threshold=temperature_lower_threshold,humidity_lower_threshold=humidity_lower_threshold,humidity_upper_threshold=humidity_upper_threshold,CO2_upper_threshold=CO2_upper_threshold)

# Save/reset threshold handler
@app.route('/save-reset-threshold', methods=['POST'])
def save_reset_threshold():
    global temperature_lower_threshold, humidity_lower_threshold, humidity_upper_threshold, CO2_upper_threshold
    
    # Get the threshold type selected in the form
    threshold_type = request.form['thresholdType']
    
    # Get the action type (save or reset)
    action = request.form['action']
    
    if action == 'save':
        # Assign the threshold value based on the selected threshold type
        if threshold_type == 'temperature_lower_threshold':
            temperature_lower_threshold = float(request.form['thresholdValue'])
        elif threshold_type == 'humidity_upper_threshold':
            humidity_upper_threshold = float(request.form['thresholdValue'])
        elif threshold_type == 'humidity_lower_threshold':
            humidity_lower_threshold = float(request.form['thresholdValue'])
        elif threshold_type == 'CO2_upper_threshold':
            CO2_upper_threshold = float(request.form['thresholdValue'])
    elif action == 'reset':
        # Reset thresholds to their initial values
        temperature_lower_threshold = initial_temperature_lower_threshold
        humidity_lower_threshold = initial_humidity_lower_threshold
        humidity_upper_threshold = initial_humidity_upper_threshold
        CO2_upper_threshold = initial_CO2_upper_threshold

    # Redirect to the homepage after processing
    return redirect('/')

# Endpoint to get the averages text
@app.route('/get_averages')
def get_averages():
    with open('/Users/Martin/Desktop/Webserver/static/averages.txt', 'r') as file:
        averages_text = file.read()
    return jsonify({'averages_text': averages_text})

# Run webserver on specified port (can be changed to any port not in use)
app.run(debug=True, port=5002)
