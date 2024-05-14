#include <AccelStepper.h>
const int directionPin = 2;
const int stepPin = 3; 
const int MSIPin = 4;
const int MSI2Pin = 5;
int test = 0;

void setup() 
{
  Serial.begin(115200);
  while (!Serial) delay(10);
  pinMode(directionPin, OUTPUT);
  pinMode(stepPin, OUTPUT);
  digitalWrite(directionPin, LOW);
  digitalWrite(stepPin, LOW);
}

void loop() 
{
  if(test == 1)
  {
    open();
  }
  else if(test == 0)
  {
    close();
  }
  else{
  standby();
  }
}

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
 delayMicroseconds(100);
 digitalWrite(stepPin, LOW);
 delayMicroseconds(100);
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



