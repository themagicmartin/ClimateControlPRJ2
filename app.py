from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Default thresholds (can be stored in a database)
thresholds = {
    'temperature_min': '10',    # Default temperature threshold
    'humidity_min': '30',   # Default minimum humidity threshold
    'humidity_max': '70',   # Default maximum humidity threshold
    'co2_max': '1000'       # Default maximum CO2 threshold
}

# Flask initiation
@app.route('/')
def index():
    # Default image path
    image_path = 'static/images/plot.png'
    return render_template('base.html', image_path=image_path, thresholds=thresholds)


# Graph handler !! Notice path of images, and naming of these
@app.route('/change-image', methods=['POST'])
def change_image():
    action = request.form['action']
    if action == 'daily':
        image_path = 'static/images/Daily.png'
    elif action == 'weekly':
        image_path = 'static/images/Weekly.png'
    elif action == 'monthly':
        image_path = 'static/images/Monthly.png'
    else:
        image_path = 'static/images/plot.png'  # Default image path
    return render_template('base.html', image_path=image_path, thresholds=thresholds)


# Save threshold handler
@app.route('/save-threshold', methods=['POST'])
def save_threshold():
    threshold_type = request.form['thresholdType']
    threshold_value = request.form['thresholdValue']
    
    # Update the thresholds dictionary with the new value
    thresholds[threshold_type] = threshold_value
    
    # Redirect to the homepage after processing
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True,port=5001)
