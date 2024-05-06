# ClimateControlPRJ2
Semesterprojekt 2, Software.

# Webserver
The Webserver is hosted locally using python3 extension Flask. This is essential for two reasons. 
One being the integration of python scripts for the website, such as buttons, input-boxes, and other interactions. 
Another being that the webserver needs to be hosted for it to be accessible for from other devices. Local hosting is not ideal, as we want to host it on a local area network (LAN), but it will do for now.
!!! Make sure to have the base.html in a templates folder, and the app.py in the parent folder of templates.

# Sensors 
The Sensor data is transmitted (with I2C) from the SCD30's every 3 seconds or so. 
The Arduino scans (I2C) for new information (SCD30.ino), and when this is registered, it prints the data through UART (USB-connection) to the          computer.  
The Computer is running main.py that is constantly scanning for input and this is dissected to identify the values of the parameters passed from the   Arduino UART print.

# Motor
