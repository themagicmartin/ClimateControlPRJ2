// Basic demo for readings from Adafruit SCD30
#include <Adafruit_SCD30.h>

Adafruit_SCD30  scd30;

const int directionPin = 2;
const int stepPin = 3; 


void setup(void) {
  Serial.begin(115200);
  while (!Serial) delay(10);     // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit SCD30 test!");

  // Try to initialize!
  if (!scd30.begin()) {
    Serial.println("Failed to find SCD30 chip");
    while (1) { delay(10); }
  }
  Serial.println("SCD30 Found!");


  // if (!scd30.setMeasurementInterval(10)){
  //   Serial.println("Failed to set measurement interval");
  //   while(1){ delay(10);}
  // }
  Serial.print("Measurement Interval: "); 
  Serial.print(scd30.getMeasurementInterval()); 
  Serial.println(" seconds");
  
  //Motor pin setup
  pinMode(directionPin, OUTPUT);
  pinMode(stepPin, OUTPUT);
  digitalWrite(directionPin, LOW);
  digitalWrite(stepPin, LOW);
}

void loop() {
  if (scd30.dataReady()){
    Serial.println("Data available!");

    if (!scd30.read()){ Serial.println("Error reading sensor data"); return; }

    Serial.print("Temperature: ");
    Serial.print(scd30.temperature);
    Serial.print("\n");
    
    Serial.print("Relative Humidity: ");
    Serial.print(scd30.relative_humidity);
    Serial.print("\n");
    
    Serial.print("CO2: ");
    Serial.print(scd30.CO2, 3);
    Serial.print("\n");
    
  } else {
    //Serial.println("No data");
  }
  //Read the string sent from terminal, do what it tells.
  if(Serial.available() > 0){
    String data = Serial.readString();
  
    if(data.equals("open"))
    {
    open();
    }
    else if(data.equals("close"))
    {
    close();
    }
    else{
    standby();
   }
  }
  standby();

  delay(100);
}
//The standby / do nothing call
void standby()
{
 digitalWrite(stepPin, LOW);
 delayMicroseconds(600);
 digitalWrite(stepPin, LOW);
 delayMicroseconds(600);
 test = 2;
}
void run()
{
 digitalWrite(stepPin, HIGH);
 delayMicroseconds(200);
 digitalWrite(stepPin, LOW);
 delayMicroseconds(200);
}
void open()
{
  //Towards metal end
  int i = 0;
  int u = 0;
  digitalWrite(directionPin, HIGH);
  for(uint16_t i; i<64000; i++)
  {
    run();
  }
  standby();
}

void close()
{
  //Towards stepper motor
  int i = 0;
  digitalWrite(directionPin, LOW);
    for(uint16_t i; i<64000; i++){
      run();
  }
  standby();
}


