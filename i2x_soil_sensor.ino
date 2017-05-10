#include <Wire.h>

#define SLAVE_ADDRESS 0x04

#define voltageFlipPin1 6
#define voltageFlipPin2 7
#define sensorPin 1

int flipTimer = 1000;

void setup() {
  Serial.begin(9600);
  pinMode(voltageFlipPin1, OUTPUT);
  pinMode(voltageFlipPin2, OUTPUT);
  pinMode(sensorPin, INPUT);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  

  Serial.println("Ready!");
}

void loop() {
  delay(100);
}

void setSensorPolarity(boolean flip){
  if(flip){
    digitalWrite(voltageFlipPin1, HIGH);
    digitalWrite(voltageFlipPin2, LOW);
  }else{
    digitalWrite(voltageFlipPin1, LOW);
    digitalWrite(voltageFlipPin2, HIGH);
  }
}

void reportLevels(int val1,int val2){
  
  int avg = (val1 + val2) / 2;
  
  String msg = "avg: ";
  msg += avg;
  //Serial.print("read 1 is ");
  //Serial.println(val1);

  //Serial.print("read 2 is ");
  //Serial.println(val2);
  
  Serial.println(msg);

}

void sendData(){
  setSensorPolarity(true);
  delay(flipTimer);
  int val1 = analogRead(sensorPin);
  delay(flipTimer);
  setSensorPolarity(false);
  delay(flipTimer);
  int val2 = 1023 - analogRead(sensorPin);
  
  int avg = (val1 + val2) / 2;

  String msg = "avg: ";
  msg += avg;
  Serial.println(msg);

  uint8_t data;

  data = avg &0xff; //lsbs
  Wire.write(data);
  Serial.println(data);
  /*data = avg > 8; //msbs
  delay(1);
  #Wire.write(data);
  #Serial.println(data);
 */
}

void receiveData(int byteCount){
  delay(100);
}

