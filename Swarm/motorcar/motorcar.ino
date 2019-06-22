#include <SPI.h>
#include <ESP8266WiFi.h>

//byte ledPin = 2;
//char ssid[] = "Electronics Club";           // SSID of your home WiFi
//char pass[] = "RandomShit";            // password of your home WiFi
//
//unsigned long askTimer = 0;
//
//IPAddress server(192,168,0,112);       // the fix IP address of the server
//WiFiClient client;

const int  EnA = 4;     //D2
const int  EnB = 14;    //D5
const int  In1 = 16;    //D0
const int  In2 = 5;     //D1
const int  In3 = 0;     //D3
const int In4 = 2;      //D4

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
//  WiFi.begin(ssid, pass);             // connects to the WiFi router
//  while (WiFi.status() != WL_CONNECTED) {
//    Serial.print(".");
//    delay(500);

  pinMode(EnA, OUTPUT);
  pinMode(EnB, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  analogWrite(EnB, 300);
  analogWrite(EnA, 300);
  
}

void forward(){
  digitalWrite(In2, LOW);
  digitalWrite(In1,HIGH);
  digitalWrite(In4, LOW);
  digitalWrite(In3, HIGH);
}

void back(){
  digitalWrite(In2, HIGH);
  digitalWrite(In1,LOW);
  digitalWrite(In4, HIGH);
  digitalWrite(In3, LOW);
}

void right(){
  analogWrite(EnB, 200);
  analogWrite(EnA, 200);
  digitalWrite(In2, LOW);
  digitalWrite(In1,HIGH);
  digitalWrite(In4, HIGH);
  digitalWrite(In3, LOW);
}

void left(){
  analogWrite(EnB, 255);
  analogWrite(EnA, 500);
  digitalWrite(In2, HIGH);
  digitalWrite(In1,LOW);
  digitalWrite(In4, HIGH);
  digitalWrite(In3, LOW);
}

void stop_motion(){
  digitalWrite(In2, LOW);
  digitalWrite(In1,LOW);
  digitalWrite(In4, LOW);
  digitalWrite(In3, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  //client.connect(server, 80);   // Connection to the server
  //digitalWrite(ledPin, LOW);    // to show the communication only (inverted logic)
  //Serial.println(".");
  //client.println("Hello server! Are you sleeping?\r");  // sends the message to the server
  //String x = client.readStringUntil('\r');
  
  //client.println("Hii\r");
  char x = Serial.read();
  
  if(x == '0'){
    back();
  }
  else if(x == '1'){
    forward();
  }
  else if(x == '2'){
    right();
  }
  else if(x == '3'){
    left();
  }
  else if(x == '4'){
    stop_motion();
  }
  //client.flush();
  delay(500); 

}
