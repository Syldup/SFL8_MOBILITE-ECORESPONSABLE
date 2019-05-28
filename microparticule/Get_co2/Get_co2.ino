#include "MQ135.h" 
// The load resistance on the board
#define RLOAD 22.0
// Calibration resistance at atmospheric CO2 level
#define RZERO 879.13 
MQ135 gasSensor = MQ135(A6); 
unsigned long duration, starttime, lowpulseoccupancy = 0;
unsigned long sampletime_ms = 30000;//attente de 30s
int val, sensorPin = A6, sensorValue = 0; 
float ratio = 0, concentration = 0;

void setup(){

Serial.begin(9600); // initialise le serial port a 9600
pinMode(13, OUTPUT);
pinMode( 3, INPUT);
pinMode(sensorPin, INPUT); 
starttime = millis();//récupère le temps réel;
}

void loop(){
//***Capteur de microparticule***
 duration = pulseIn(8, LOW);
    lowpulseoccupancy = lowpulseoccupancy+duration;

    if ((millis()-starttime) > sampletime_ms)//si sampletime_ms == 30s
    {
        ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // intégration du pourcentage 0=>100
        // Calcule de la concentration avec une fonction trigonométrique du 3ème degrès
        concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62;
        Serial.print(concentration);// affichage concentration
        lowpulseoccupancy = 0;
        starttime = millis();
        
        //***Capteur de CO2***
        
        float ppm = gasSensor.getPPM(); 
        Serial.print (","); 
        Serial.println (ppm); 

    }
}


