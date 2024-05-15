import threading                                            # For multithread operation
import serial                                               # Serial communication to Arduino
import time                                                 # Sleep timers
from datetime import datetime, timedelta                    # Timestamps for plotting
import matplotlib.pyplot as plt                             # For data visualisation

# Initialize serial communication
serialInst = serial.Serial('/dev/tty.usbmodem1101', 115200)  # Port and baudrate. On mac terminal: ls /dev/tty.*
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
temperature_lower_threshold = 10.0
humidity_lower_threshold = 30.0
humidity_upper_threshold = 70.0
CO2_upper_threshold = 2000.0

# Initialize thresholds with initial values
initial_temperature_lower_threshold = temperature_lower_threshold
initial_humidity_lower_threshold = humidity_lower_threshold
initial_humidity_upper_threshold = humidity_upper_threshold
initial_CO2_upper_threshold = CO2_upper_threshold

# Initialize threshold triggers
CO2_beyond = False
hum_below = False
hum_beyond = False
temp_below = False

# Initialize window boolean
WindowIsOpen = False

# Initialize threshold colors
color_hum_low = 'gray'
color_hum_high = 'gray'
color_CO2 = 'gray'
color_temp = 'gray' 

# Methods
def save_plot(time_log, temp_log, hum_log, CO2_log, output_path): # Converts plots to PNG. Used in update_plots
    global temperature_lower_threshold, color_temp, humidity_lower_threshold, humidity_upper_threshold, color_hum_low, color_hum_high, CO2_upper_threshold, color_CO2
    
    # Create a new plot
    plt.figure(figsize=(15, 13))
    
    # Temperature plot
    plt.subplot(3, 1, 1)
    plt.plot([t.strftime('%H:%M:%S') for t in time_log], temp_log, color='red')  # Format time to display hour, minute, and second
    plt.axhline(y=temperature_lower_threshold, color=color_temp, linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.title('Temperature Plot')
    plt.xticks(rotation=0)  # Rotate x-axis labels if needed
    
    # Dynamically adjust the number of ticks on the x-axis for temperature plot
    num_ticks_temp = min(len(time_log), 10)  # Maximum of 10 ticks
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(num_ticks_temp))
    
    # Humidity plot
    plt.subplot(3, 1, 2)
    plt.plot([t.strftime('%H:%M:%S') for t in time_log], hum_log, color='blue')  # Format time to display hour, minute, and second
    plt.axhline(y=humidity_lower_threshold, color=color_hum_low, linestyle='--')
    plt.axhline(y=humidity_upper_threshold, color=color_hum_high, linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('Humidity (%)')
    plt.ylim(0, 100)
    plt.grid(True)
    plt.title('Humidity Plot')
    plt.xticks(rotation=0)  # Rotate x-axis labels if needed
    
    # Dynamically adjust the number of ticks on the x-axis for humidity plot
    num_ticks_hum = min(len(time_log), 10)  # Maximum of 10 ticks
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(num_ticks_hum))
    
    # CO2 plot
    plt.subplot(3, 1, 3)
    plt.plot([t.strftime('%H:%M:%S') for t in time_log], CO2_log, color='green')  # Format time to display hour, minute, and second
    plt.axhline(y=CO2_upper_threshold, color=color_CO2, linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('CO2 (ppm)')
    plt.grid(True)
    plt.title('CO2 Plot')
    plt.xticks(rotation=0)  # Rotate x-axis labels if needed
    
    # Dynamically adjust the number of ticks on the x-axis for CO2 plot
    num_ticks_CO2 = min(len(time_log), 10)  # Maximum of 10 ticks
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(num_ticks_CO2))
    
    plt.subplots_adjust(hspace=0.5)  # Adjust the vertical spacing between subplots
    
    plt.tight_layout()
    
    # Save the plot as a PNG file
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)
    
    # Close the current plot to release memory
    plt.close()


def log_data_thread(): #Function to log data in a seperate thread
    global temperature, humidity, CO2, time_log, temp_log, hum_log, CO2_log
    while True:
        # Read data from Arduino
        data = serialInst.readline().decode().strip()  # Read a line of data
        if data:  # Check for data
            current_time = datetime.now()
            lines = data.split('\n')
            for line in lines:
                if "Temperature" in line:
                    temperature = float(line.split(":")[1].split(",")[0])  # Extract the value between ':' and ','
                elif "Relative Humidity" in line:
                    humidity = float(line.split(":")[1].split(",")[0])  # Extract the value between ':' and ','
                elif "CO2" in line:
                    CO2 = float(line.split(":")[1].split(",")[0])  # Extract the value between ':' and ','

            # Log received data to lists
            time_log.append(current_time)  # Append current time as datetime object
            temp_log.append(temperature)
            hum_log.append(humidity)
            CO2_log.append(CO2)
            
def update_plots(): # Update plots with new data
    # Calculate the current time
    current_time = datetime.now()
    
    # Plot for the last minute
    last_minute_time = current_time - timedelta(minutes=1)
    mask_minute = [t >= last_minute_time for t in time_log]
    time_minute = [t for t, mask in zip(time_log, mask_minute) if mask]
    temp_minute = [temp for temp, mask in zip(temp_log, mask_minute) if mask]
    hum_minute = [hum for hum, mask in zip(hum_log, mask_minute) if mask]
    CO2_minute = [CO2 for CO2, mask in zip(CO2_log, mask_minute) if mask]
    if CO2_minute:  # Check if CO2_minute list is not empty
        save_plot(time_minute, temp_minute, hum_minute, CO2_minute, 'static/images/minute.png')
    
    # Plot for the last hour
    last_hour_time = current_time - timedelta(hours=1)
    mask_hourly = [t >= last_hour_time for t in time_log]
    time_hourly = [t for t, mask in zip(time_log, mask_hourly) if mask]
    temp_hourly = [temp for temp, mask in zip(temp_log, mask_hourly) if mask]
    hum_hourly = [hum for hum, mask in zip(hum_log, mask_hourly) if mask]
    CO2_hourly = [CO2 for CO2, mask in zip(CO2_log, mask_hourly) if mask]
    if CO2_hourly:  # Check if CO2_hourly list is not empty
        save_plot(time_hourly, temp_hourly, hum_hourly, CO2_hourly, 'static/images/hourly.png')
    
    # Plot for the last 24 hours
    last_24_hours_time = current_time - timedelta(days=1)
    mask_daily = [t >= last_24_hours_time for t in time_log]
    time_daily = [t for t, mask in zip(time_log, mask_daily) if mask]
    temp_daily = [temp for temp, mask in zip(temp_log, mask_daily) if mask]
    hum_daily = [hum for hum, mask in zip(hum_log, mask_daily) if mask]
    CO2_daily = [CO2 for CO2, mask in zip(CO2_log, mask_daily) if mask]
    if CO2_daily:  # Check if CO2_daily list is not empty
        save_plot(time_daily, temp_daily, hum_daily, CO2_daily, 'static/images/daily.png')

    time.sleep(2)  # Adjust the sleep time as needed

def check_triggers(): # Compare data to thresholds
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

def actuator_activator(): # Controller for open and closing window
    global WindowIsOpen,CO2_beyond
    # Open or close window?
    if CO2_beyond and not WindowIsOpen: # OPEN WINDOW! 
        open_window()
    elif not CO2_beyond and WindowIsOpen: # CLOSE WINDOW
        close_window()

def open_window():
    global WindowIsOpen
    print("UPDATE: Opening window!")
    # CODE HERE
    message = "open\n"
    serialInst.write(message.encode())

    time.sleep(5)  # Allow time for Window to close
    WindowIsOpen = True

def close_window():
    global WindowIsOpen
    print("UPDATE: Closing window!")
    # CODE HERE
    message = "close\n"
    serialInst.write(message.encode())

    time.sleep(5)  # Allow time for Window to close
    WindowIsOpen = False

# Start a thread to run the update_plots_thread function
log_thread = threading.Thread(target=log_data_thread)
log_thread.start()

try:
    while True:
        update_plots() # Has two second sleep

        check_triggers()

        actuator_activator()

except KeyboardInterrupt: # Close program on Ctrl+C
    print("Ctrl+C detected. Exiting...")
    raise SystemExit # Exit the program

