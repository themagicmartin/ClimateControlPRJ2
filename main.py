import serial
import time
import matplotlib.pyplot as plt

# Initialize serial communication
serialInst = serial.Serial('/dev/tty.usbmodem1101', 115200)  # On mac terminal: ls /dev/tty.*
time.sleep(2)  # Allow time for Arduino to initialize

# Initialize lists for logging data
time_log = []
temp_log = []
hum_log = []
CO2_log = []

# Initialize variables
temperature = 0
humidity = 0
CO2 = 0
start_time = time.time()

# Initialize threshold values
temperature_lower_threshold = float(10)
humidity_lower_threshold = float(20)
humidity_upper_threshold = float(80)
CO2_upper_threshold = float(1500)

# Initialize threshold triggers
CO2_beyond = False
hum_below = False
hum_beyond = False
temp_below = False

# Initialize threshold colors
color_hum_low = 'gray'
color_hum_high = 'gray'
color_CO2 = 'gray'
color_temp = 'gray' 

# Initialize plot
plt.figure(figsize=(15, 10))

# Methods
def update_plots():
    global temperature, humidity, CO2  # Declare variables as global to modify them
    # Update the plots
    plt.clf()  # Clear previous plot

    # Temperature plot
    plt.subplot(3, 1, 1)
    plt.plot(time_log, temp_log, color='red')
    plt.axhline(y=temperature_lower_threshold, color=color_temp, linestyle='--')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.text(max(time_log), temperature, f'{temperature:.2f}', va='center', ha='left', color='red')

    # Humidity plot
    plt.subplot(3, 1, 2)
    plt.plot(time_log, hum_log, color='blue')
    plt.axhline(y=humidity_lower_threshold, color=color_hum_low, linestyle='--')
    plt.axhline(y=humidity_upper_threshold, color=color_hum_high, linestyle='--')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Humidity (%)')
    plt.ylim(0, 100)
    plt.grid(True)
    plt.text(max(time_log), humidity, f'{humidity_lower_threshold:.2f}', va='center', ha='left', color='blue')

    # CO2 plot
    plt.subplot(3, 1, 3)
    plt.plot(time_log, CO2_log, color='green')
    plt.axhline(y=CO2_upper_threshold, color=color_CO2, linestyle='--')
    plt.xlabel('Time (minutes)')
    plt.ylabel('CO2 (ppm)')
    plt.grid(True)
    plt.text(max(time_log), CO2, f'{CO2:.2f}', va='center', ha='left', color='green')

    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)  # Pause to allow the plot to update

def log_data(data):
    global temperature, humidity, CO2  # Declare variables as global to modify them
    elapsed_time = (time.time() - start_time) / 60  # Minutes passed
    lines = data.split('\n')                        # Split lines of data
    for line in lines:                              # Scan for information
        if "Temperature" in line:
            temperature = float(line.split(":")[1].strip())
        elif "Relative Humidity" in line:
            humidity = float(line.split(":")[1].strip())
        elif "CO2" in line:
            CO2 = float(line.split(":")[1].strip()) 

    # Log received data to lists
    time_log.append(elapsed_time)
    temp_log.append(temperature)
    hum_log.append(humidity)
    CO2_log.append(CO2)

def check_triggers():
    global temperature, humidity, CO2, CO2_beyond, hum_below, hum_beyond, temp_below, color_CO2, color_hum_low, color_hum_high, color_temp
    # Threshold triggers
    # CO2 trigger
    if CO2 > CO2_upper_threshold and not CO2_beyond:
        # CO2 is high
        color_CO2 = 'red'
        CO2_beyond = True
        print("UPDATE: CO2 is above threshold!")
    elif CO2 < CO2_upper_threshold:
        # CO2 is good
        color_CO2 = 'gray'
        CO2_beyond = False

    # Humidity trigger
    if humidity < humidity_lower_threshold and not hum_below:             
        # Humidity is low  
        hum_below = True
        color_hum_low = 'red'
        print("UPDATE: Humidity is below the lower threshold!")
    elif humidity > humidity_upper_threshold and not hum_beyond:              
        # Humidity is high
        hum_beyond = True 
        color_hum_high = 'red'
        print("UPDATE: Humidity is above the upper threshold!")
    elif humidity < humidity_upper_threshold and humidity > humidity_lower_threshold:
        # Humidity is within thresholds
        hum_below = False
        hum_beyond = False  
        color_hum_low = 'gray'
        color_hum_high = 'gray'

    # Temperature trigger
    if temperature < temperature_lower_threshold and not temp_below: 
        # Temperature is low
        temp_below = True
        color_temp = 'red'
        print("UPDATE: Temperature is below the threshold!")
    elif temperature > temperature_lower_threshold:
        # Temperature is good
        temp_below = False 
        color_temp = 'gray' 

# Main loop
try:
    while True:
        # Read data from Arduino
        data = serialInst.readline().decode().strip()  # Read a line of data
        if data:  # Check for data
            log_data(data)  # Log new data

            update_plots()  # Update the plots

            check_triggers()    # Checking data against thresholds
            
except KeyboardInterrupt: # Close serial connection on Ctrl+C
    serialInst.close()
