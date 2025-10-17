#include <Servo.h>
#define sensor A0 
#define maxAngle 80 // set servo max angle 
#define minAngle 0 // set servo min angle 
Servo myservo; // create servo object to control a servo 
// twelve servo objects can be created on most boards 
int pos = 0; // variable to store the servo position 
float volts; 
int distance; 
void PID(); 
void setup() { 
  Serial.begin(9600); 
  myservo.attach(9); // attaches the servo on pin 9 to the servo object 
} 
void loop() { 
  char command = Serial.read(); 
  switch (command){ 
    case 'a': //automatic control 
      while (Serial.available() == 0){ 
        PID(); 
        } 
      break; 
    case 'b': 
      //servo setup 
      ServoSetup(); 
      break; 
    case 'c': 
      //Stop System 
      Stop(); 
      break; 
  } 
} 

void PID() {
  //Automatic Control
  Serial.println("Starting Manual Control!"); 
  for(int i = minAngle+1; i < maxAngle; i ++){  
    Serial.print("Servo Angle: "); 
    Serial.println(i); 
    delay(15);
    } 
  for(int i = maxAngle-1; i > minAngle; i --){ 
    Serial.print("Servo Angle: "); 
    Serial.println(i); 
    delay(15); 
  } 
} 

void ServoSetup(){ 
  Serial.println("Starting Servo Setup!"); 
} 

void Stop(){ 
  Serial.println("Stopping System!"); 
  myservo.detach(); 
}