/*
  UDPSendReceive.pde:
  This sketch receives UDP message strings, prints them to the serial port
  and sends an "acknowledge" string back to the sender

  A Processing sketch is included at the end of file that can be used to send
  and received messages for testing with a computer.

  created 21 Aug 2010
  by Michael Margolis

  This code is in the public domain.

  adapted from Ethernet library examples
*/


#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#ifndef STASSID
#define STASSID "Electronics Club"
#define STAPSK  "RandomShit"
#endif

const int  EnA = 4;     //D2
const int  EnB = 14;    //D5
const int  In1 = 16;    //D0
const int  In2 = 5;     //D1
const int  In3 = 0;     //D3
const int In4 = 2;      //D4


unsigned int localPort = 5007;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE + 1]; //buffer to hold incoming packet,
char  ReplyBuffer[] = "acknowledged\r\n";       // a string to send back

WiFiUDP Udp;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", localPort);
  Udp.begin(localPort);
  pinMode(EnA, OUTPUT);
  pinMode(EnB, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  analogWrite(EnB, 500);
  analogWrite(EnA, 500);
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
  analogWrite(EnB, 500);
  analogWrite(EnA, 255);
  digitalWrite(In2, HIGH);
  digitalWrite(In1,LOW);
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
  int x = 0;
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.printf("Received packet of size %d from %s:%d\n    (to %s:%d, free heap = %d B)\n",
                  packetSize,
                  Udp.remoteIP().toString().c_str(), Udp.remotePort(),
                  Udp.destinationIP().toString().c_str(), Udp.localPort(),
                  ESP.getFreeHeap());

    // read the packet into packetBufffer
    //String x = client.readStringUntil('\r');
    int n = Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    packetBuffer[n] = 0;
    Serial.println("Contents:");
    Serial.println(packetBuffer);

    // send a reply, to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(ReplyBuffer);
    x = (int)packetBuffer;
    Udp.endPacket();
  }
 if(x == 0){
    back();
  }
  else if(x == 1){
    forward();
  }
  else if(x == 2){
    right();
  }
  else if(x == 3){
    left();
  }
  else if(x == 4){
    stop_motion();
  }
  
  Serial.println(x);
   
  

}

/*
  test (shell/netcat):
  --------------------
    nc -u 192.168.esp.address 8888
*/
