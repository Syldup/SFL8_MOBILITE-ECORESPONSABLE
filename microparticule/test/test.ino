
#include "MQ135.h" 
// The load resistance on the board
#define RLOAD 22.0
// Calibration resistance at atmospheric CO2 level
#define RZERO 879.13 
MQ135 gasSensor = MQ135(A6); 
int val; 
int sensorPin = A6; 
int sensorValue = 0; 
void setup() { 
  Serial.begin(9600);
  pinMode(sensorPin, INPUT); 
} 
 
void loop() { 
  delay(5000); 
  float ppm = gasSensor.getPPM(); 
  Serial.print ("ppm: "); 
  Serial.println (ppm); 
} 
