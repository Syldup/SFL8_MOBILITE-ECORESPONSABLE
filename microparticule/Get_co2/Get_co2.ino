int pin = 8;
unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 30000;//sampe 2s ;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float concentration = 0;
int sensorValue;
int digitalValue;
void setup()
{

Serial.begin(9600); // sets the serial port to 9600
pinMode(13, OUTPUT);
pinMode( 3, INPUT);
pinMode(pin,INPUT);
starttime = millis();//get the current time;

}

void loop()
{

 duration = pulseIn(pin, LOW);
    lowpulseoccupancy = lowpulseoccupancy+duration;

    if ((millis()-starttime) > sampletime_ms)//if the sampel time == 30s
    {
        ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // Integer percentage 0=>100
        concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
        Serial.println(concentration);
        lowpulseoccupancy = 0;
        starttime = millis();

        sensorValue = analogRead(0); // read analog input pin 0

        digitalValue = digitalRead(2); 
        if(sensorValue>400){
          digitalWrite(13, HIGH);
        }
        else
        digitalWrite(13, LOW);
        Serial.print("CO2 : ");
        Serial.println(sensorValue, DEC); // prints the value read
    }
}
