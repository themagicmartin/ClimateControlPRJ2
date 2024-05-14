//arduino 2
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX for SoftwareSerial
float temperature1;
float humidity1;
float CO21;
bool limit = false;

void setup() {
  Serial.begin(115200);
  mySerial.begin(115200); // Initialize SoftwareSerial
}

void loop() 
{
  if (mySerial.available() > 0) 
  {
    String receivedData = mySerial.readStringUntil('\n');
    if (receivedData.startsWith("sensor1data:")) 
    {
        parseSensorData(receivedData);
        checkLimit();
    }
  }

  float temperature2 = 23;  // Sensor 2 temperature
  float humidity2 = 40;     // Sensor 2 humidity
  float CO22 = 800;         // Sensor 2 CO2 level

  // Displaying combined sensor data
  Serial.print("Temperature1: ");
  Serial.print(temperature1);
  Serial.print(" °C, ");
  Serial.print("Humidity1: ");
  Serial.print(humidity1);
  Serial.print(" %, ");
  Serial.print("CO21: ");
  Serial.print(CO21);
  Serial.println(" ppm ");
  
  Serial.print("Temperature2: ");
  Serial.print(temperature2);
  Serial.print(" °C, ");
  Serial.print("Humidity2: ");
  Serial.print(humidity2);
  Serial.print(" %, ");
  Serial.print("CO22: ");
  Serial.print(CO22);
  Serial.println(" ppm");
  
  delay(1000); // Delay to avoid flooding the Serial output
}

void parseSensorData(String data) 
{
  data.remove(0, 12); // Remove "sensor1data:" from the beginning
  int commaIndex1 = data.indexOf(',');
  int commaIndex2 = data.lastIndexOf(',');
  temperature1 = data.substring(0, commaIndex1).toFloat();
  humidity1 = data.substring(commaIndex1 + 1, commaIndex2).toFloat();
  CO21 = data.substring(commaIndex2 + 1).toFloat();
}

void checkLimit() 
{
  if (temperature1 > 30) 
  {
    Serial.println("Temperature limit reached");
    limit = true;
  } 
  else if (humidity1 > 80) 
  {
    Serial.println("Humidity limit reached");
    limit = true;
  } 
  else if (CO21 > 1500) 
  {
    Serial.println("CO2 limit reached");
    limit = true;
  } 
  else 
  {
    limit = false;
  }
  
  delay(2000);
} 

