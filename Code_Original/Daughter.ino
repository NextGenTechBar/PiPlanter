const char EOPmarker = '$'; //This is the end of packet marker
char serialbuf[32]; //This gives the incoming serial some room. Change it if you want a longer incoming.

#include <string.h> // we'll need this for subString
#define MAX_STRING_LEN 20 // like 3 lines above, change as needed.

// Hardware Pin Defenitions

//Pump pins
int Pump_pin = 2;
#define Num_of_Sols 2
int Sol0_pin = 3;
int Sol1_pin = 4;
int Sols[Num_of_Sols] = { Sol0_pin, Sol1_pin };

//LED pins
#define Num_of_LEDs 3
int RLED_pin = 5;
int GLED_pin = 6;
int BLED_pin = 9;
int LEDs[Num_of_LEDs] = { RLED_pin, GLED_pin, BLED_pin }; 

//Sensor input pins
#define Num_of_Sens 5
int P_MST0 = 0;
int P_MST1 = 1;
int A_LDR0 = 2;
int A_TMP0 = 3;
int P_TMP0 = 4;
int Sens[Num_of_Sens] = { P_MST0, P_MST1, A_LDR0, A_TMP0, P_TMP0 };

int SensorsEnable_pin = 7;

void setup(){
  Serial.begin(9600);

  pinMode(Pump_pin,OUTPUT);

  for (int i = 0; i < Num_of_Sols; i++)  {
    pinMode(Sols[i], OUTPUT);
  }
  
  for (int i = 0; i < Num_of_LEDs; i++)  {
    pinMode(LEDs[i], OUTPUT);
  }
  
  pinMode(SensorsEnable_pin, OUTPUT);
}
  
void loop() {
    if (Serial.available() > 0) { //makes sure something is ready to be read
      static int bufpos = 0; //starts the buffer back at the first position in the incoming serial.read
      char inchar = Serial.read(); //assigns one byte (as serial.read()'s only input one byte at a time
      if (inchar != EOPmarker) { //if the incoming character is not the byte that is the incoming package ender
        serialbuf[bufpos] = inchar; //the buffer position in the array get assigned to the current read
        bufpos++; //once that has happend the buffer advances, doing this over and over again until the end of package marker is read.
      }
      else { //once the end of package marker has been read
        serialbuf[bufpos] = 0; //restart the buff
        bufpos = 0; //restart the position of the buff

        Action( atoi(subStr(serialbuf, ",", 2)),atoi(subStr(serialbuf, ",", 3)),atof(subStr(serialbuf, ",", 4)),atoi(subStr(serialbuf, ",", 5)) );
         
      }
    }
}

void Action(int Command_Type, int Data0, float Data1, int Data2){
  if (Command_Type == 0){ 
    SampleSensors(Data0,(int)Data1);
  }
  if (Command_Type == 1){ 
    LEDWrite(Data0,(int)Data1,Data2);
  }
  if (Command_Type == 2){
    PumpLiquid(Data0,Data1);
  }
}

//start of plant functions

void SampleSensors(int Sensor, int Samples){
  float value;
  if (Sensor == 0 || Sensor == 1 || Sensor == 2 ){ //Moisture & Light Sensors
    float sum = 0;
    for (int i = 0; i < Samples; i++){
      digitalWrite(SensorsEnable_pin, OUTPUT);
      sum = sum + analogRead(Sens[Sensor]);
      digitalWrite(SensorsEnable_pin, LOW);
    }
    float val = sum/Samples;
    value = (val/1024)*100;
  }
  else if (Sensor == 3 || Sensor == 4) { //Temperature Sensors
    float sum = 0;
    for (int i = 0; i < Samples; i++){
      digitalWrite(SensorsEnable_pin, OUTPUT);
      sum = sum + analogRead(Sens[Sensor]);
      digitalWrite(SensorsEnable_pin, LOW);
    }
    float val = sum/Samples;
    int rawvoltage= val;
    float volts= rawvoltage/205.0;
    float celsiustemp= 100.0 * volts - 50;
    float fahrenheittemp= celsiustemp * 9.0/5.0 + 10.0;
    value = fahrenheittemp;
  }
  Serial.println(value); 
}

void LEDWrite(int R, int G, int B){
  int colors[] = {R,G,B}; 
  for (int i = 0; i < Num_of_LEDs; i++){
    analogWrite(LEDs[i],colors[i]);
  }
  Serial.println("1");
}

void PumpLiquid(int Sol_No, float Volume){
  float ontime = (Volume*15); 
  digitalWrite(Sols[Sol_No], HIGH);  
  digitalWrite(Pump_pin, HIGH);
  delay(ontime*1000);
  digitalWrite(Pump_pin, LOW);
  digitalWrite(Sols[Sol_No], LOW);
 
  Serial.println(ontime);
}

// end of plant functions
 
char* subStr (char* input_string, char *separator, int segment_number) {
  char *act, *sub, *ptr;
  static char copy[MAX_STRING_LEN];
  int i;
  strcpy(copy, input_string);
  for (i = 1, act = copy; i <= segment_number; i++, act = NULL) {
    sub = strtok_r(act, separator, &ptr);
    if (sub == NULL) break;
  }
 return sub;
}
