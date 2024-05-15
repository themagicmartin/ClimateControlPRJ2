#include <Adafruit_SCD30.h>
#include <SoftwareSerial.h>

Adafruit_SCD30 scd30;

SoftwareSerial mySerial(10, 11); // RX, TX for SoftwareSerial

float temperature1;
float humidity1;
float CO21;

void setup() {
  Serial.begin(115200);
  mySerial.begin(115200); // Initialize SoftwareSerial
  if (!scd30.begin()) {
    Serial.println("Failed to find SCD30 chip");
    while (1) { delay(10); }
  }
  Serial.println("SCD30 Found!");
}

void readSensorData() 
{
  if (scd30.dataReady()) 
  {
    if (!scd30.read()) 
    {
      Serial.println("Error reading sensor data");
      return;
    }

    temperature1 = scd30.temperature;
    humidity1 = scd30.relative_humidity;
    CO21 = scd30.CO2;
  } 
  else 
  {
    Serial.println("No data available from Sensor");
  }
}

void transmitSensorData() 
{
  mySerial.print("sensor1data:");
  mySerial.print(temperature1);
  mySerial.print(",");
  mySerial.print(humidity1);
  mySerial.print(",");
  mySerial.println(CO21);
}

void loop() 
{
  readSensorData();
  transmitSensorData();
  delay(1000);
}
