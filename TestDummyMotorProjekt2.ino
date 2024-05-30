#include <AccelStepper.h>
#include <Wire.h>
#define buzzerPin 5
const int directionPin = 2;
const int stepPin = 3; 
char test = 'x';

void setup() 
{
  Serial.begin(115200);
  while (!Serial) delay(10);
  pinMode(directionPin, OUTPUT);
  pinMode(stepPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(directionPin, LOW);
  digitalWrite(stepPin, LOW);
}

void loop() 
{
  if(Serial.available() > 0){
    char data = Serial.read();
    Serial.println("kom ind i motor loop");
    Serial.println(data);
    if(data == 'j')
    {
      beep();
      delay(1000);
      beep();
      open();
    }
    else if(data == 'n')
    {
      beep();
      delay(1000);
      beep();
      close();
    }
    else{
      standby();
   }
  }
}

void beep()
{
  int u;
  for(u=0; u<80; u++)
  digitalWrite(buzzerPin, HIGH);
  delay(500);
  digitalWrite(buzzerPin, LOW);
  delay(500);
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
  digitalWrite(directionPin, HIGH);
  for(uint16_t i=0; i<64000; i++)
  {
    run();
  }
  standby();
}

void close()
{
  //Towards stepper motor
  digitalWrite(directionPin, LOW);
    for(uint16_t i=0; i<64000; i++){
      run();
  }
  standby();
}



