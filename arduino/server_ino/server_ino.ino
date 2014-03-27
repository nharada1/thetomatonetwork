#include <LPD8806.h>
#include <SPI.h>
#include <Dhcp.h>
#include <Dns.h>
#include <Ethernet.h>
#include <EthernetClient.h>
#include <EthernetServer.h>
#include <EthernetUdp.h>
#include <util.h>

#define serverCycle 50U
#define plantcareCycle 5U


// Server connection fields
String command_buffer;
String command;
EthernetClient client;

// Arduino Cycle counters
unsigned long serverLastMillis = 0;
unsigned long plantcareLastMillis = 0;
boolean serverState = false;
boolean plantcareState = false;

// BEGIN CONTROL CODE

// Control constants
const int NUM_PLANTS = 4;
const int LIGHT_PIN = 13;
const int AIR_PIN = 12;
const int PLANT_PINS [] = {11,10,9,8}; 
const unsigned long WATER_CYCLE_PERIOD = 20000; //7200000; // 2 hours
const unsigned long LIGHT_CYCLE_PERIOD = 10000; //43200000; // 12 hours
// 5 minute difference between duty cycles of each plant
// i.e. water_duty_cycle[0] = water_duty_cycle[1]-0.042
const double WATER_DUTY_CYCLE_GRADIENT = 0.042;

// Control variables
// Run for approx. hour on, hour off at the start
// double waterDutyCycles[4];
double waterDutyCycles [] = {0.5-1.5*WATER_DUTY_CYCLE_GRADIENT,
                          0.5-0.5*WATER_DUTY_CYCLE_GRADIENT,
                          0.5+0.5*WATER_DUTY_CYCLE_GRADIENT,
                          0.5+1.5*WATER_DUTY_CYCLE_GRADIENT};
unsigned long waterCycleLastMillis = 0;
unsigned long lightCycleLastMillis = 0;
void updatePlantCare(){
  int i=0;
  unsigned long currentMillis = millis();
  // Water
  if(currentMillis-waterCycleLastMillis >= WATER_CYCLE_PERIOD){
    if(0){ //Server is available to overrwrite duty cycles      
    }
    for(i; i<NUM_PLANTS; i++){
      digitalWrite(PLANT_PINS[i],HIGH);
    }
    Serial.println("Started new water cycle.");
    waterCycleLastMillis = currentMillis;
  } else {
    for(i; i<NUM_PLANTS; i++){
      if(currentMillis-waterCycleLastMillis >= waterDutyCycles[i]*WATER_CYCLE_PERIOD){
        digitalWrite(PLANT_PINS[i],LOW);
        Serial.print("Stopped water cycle for plant ");
        Serial.println(i);
      }
    }
  }
  // Light
  if(currentMillis-lightCycleLastMillis >= LIGHT_CYCLE_PERIOD){
    if(digitalRead(LIGHT_PIN)==HIGH){
      digitalWrite(LIGHT_PIN,LOW);
    } else {
      digitalWrite(LIGHT_PIN,HIGH);
    }
    Serial.println("Toggled light");
    lightCycleLastMillis = currentMillis;
  }
}

// END CONTROL CODE

/*
  Web Server for Hydroponics
 
 Based almost entirely upon Web Server by Tom Igoe and David Mellis

 */

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0F, 0x3B, 0xE2 };

IPAddress ip(192,168,1,147); //<<< ENTER DESIRED LOCAL IP ADDRESS HERE!!!

// Initialize the Ethernet server library
// with the IP address and port you want to use 
// (port 80 is default for HTTP):
EthernetServer server(80);

void setup()
{
   command_buffer = "";
   command        = command_buffer;

  // start the Ethernet connection and the server:
  Ethernet.begin(mac, ip);
  server.begin();
  Serial.begin(9600);
  Serial.println("let's do it !!!!!");
    
  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
  }
  // print your local IP address:
  Serial.println(Ethernet.localIP());
  client = server.available();
  
  pinMode(LIGHT_PIN,OUTPUT);
  digitalWrite(LIGHT_PIN,HIGH);
  pinMode(AIR_PIN,OUTPUT);
  digitalWrite(AIR_PIN,HIGH);
  int i=0;
  for(i; i<NUM_PLANTS; i++){
    pinMode(PLANT_PINS[i],OUTPUT);
    digitalWrite(PLANT_PINS[i],HIGH);
  }
  
}

void loop()
{   
    // Check if this is a cycle dedicated for handling requests
    if(cycleCheck(&serverLastMillis, serverCycle))
    {
      client = server.available();
      command = get_stream_value();
      command = "1.26f,2.34f,1.34f";

      // Parse command
      int first_delim  = command.indexOf(',');
      int second_delim = command.indexOf(',', first_delim + 1);
      int third_delim  = command.indexOf(',', second_delim + 1);

      String val_1 = command.substring(0, first_delim);
      String val_2 = command.substring(first_delim+1, second_delim);
      String val_3 = command.substring(second_delim+1, third_delim);

      char buf[val_1.length()];
      val_1.toCharArray(buf,val_1.length());
      float val_1_f = atof(buf);
      
      char buf2[val_2.length()];
      val_2.toCharArray(buf2,val_2.length());
      float val_2_f = atof(buf2);

      char buf3[val_3.length()];
      val_3.toCharArray(buf3,val_3.length());
      float val_3_f = atof(buf3); 
 
      Serial.println("The numbers are: ");
      Serial.print(val_1_f);
      Serial.print(", ");
      Serial.print(val_2_f);
      Serial.print(", ");
      Serial.print(val_3_f);     

    }
    
    // Check if this is a cycle dedicated for handling plantcare
    if(cycleCheck(&plantcareLastMillis, plantcareCycle))
    {
      updatePlantCare();
    }
}

// Ethernet character stream get character
String get_stream_value()
{ 
  boolean incoming = 0;
  
  // listen for incoming clients
  if (client) {
    while(client.connected()) {
      if (client.available()) {
        char c = client.read();
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (incoming)
        {
          if(c == ' ')
          {
            String temp_buffer = command_buffer;
            command_buffer     = "";
            incoming           = 0;
            return temp_buffer;
          }
          command_buffer += c; 
          Serial.println(command_buffer);
        }
        
        if(c == '$'){ 
          incoming = 1;
        }
      }
     else{
       client.stop();
       client = server.available();
     }
   }
  }
  return command;
}

// Determine how many cycles each process gets
boolean cycleCheck(unsigned long *lastMillis, unsigned int cycle) 
{
  unsigned long currentMillis = millis();
  if(currentMillis - *lastMillis >= cycle)
  {
    *lastMillis = currentMillis;
    return true;
  }
  else
    return false;
}


  

  

