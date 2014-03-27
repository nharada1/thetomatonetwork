#include <Ethernet.h>
#include <SPI.h>

#define serverCycle 50U
#define plantcareCycle 5U

// Server connection fields
String nutrient_string_buffer;
String nutrient_string;
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
boolean waterCycleStarted [] = {false,false,false,false};
unsigned long waterCycleLastMillis = 0;
unsigned long lightCycleLastMillis = 0;

boolean water_state = 0;
boolean light_state = 0;

void updatePlantCare(){
  int i=0;
  unsigned long currentMillis = millis();
  // Water
  if(currentMillis-waterCycleLastMillis >= WATER_CYCLE_PERIOD){
        for(i; i<NUM_PLANTS; i++){
          digitalWrite(PLANT_PINS[i],HIGH);
        }
    Serial.println("Started new water cycle.");
    waterCycleLastMillis = currentMillis;
    waterCycleStarted[i] = true;
  } else {
    for(i; i<NUM_PLANTS; i++){
      if(waterCycleStarted[i] && currentMillis-waterCycleLastMillis >= waterDutyCycles[i]*WATER_CYCLE_PERIOD){
        digitalWrite(PLANT_PINS[i],LOW);
        Serial.print("Stopped water cycle for plant ");
        Serial.println(i);
        waterCycleStarted[i] = false;
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

unsigned long lastConnectionTime = 0;          // last time you connected to the server, in milliseconds
boolean lastConnected = false;                 // state of the connection last time through the main loop
const unsigned long postingInterval = 10*1000;  // delay between updates, in milliseconds

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0F, 0x3B, 0xE2 };
char server[] = "http://seed-hydroponics.herokuapp.com";

// nutrient values
float nutrient_val_1 = 0;
float nutrient_val_2 = 0;
float nutrient_val_3 = 0;
float nutrient_val_4 = 0;


void setup()
{
  // Init nutrient_string buffer to empty
  nutrient_string_buffer = "";
  nutrient_string        = nutrient_string_buffer;
  
  // Begin serial comm
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("Initializing seed hydroponics server");
  // start the Ethernet connection and the server:
  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
  }
  // give the Ethernet shield a second to initialize:
  delay(1000);
    
  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
  }
  
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
      if(!client.connected() && (millis() - lastConnectionTime > postingInterval)) {
        Serial.println("requesting!!!");
        httpRequest();
      }
      
      nutrient_string = get_stream_value();

      // Parse nutrient_string
      int first_delim  = nutrient_string.indexOf(',');
      int second_delim = nutrient_string.indexOf(',', first_delim + 1);
      int third_delim  = nutrient_string.indexOf(',', second_delim + 1);
      int fourth_delim = nutrient_string.indexOf(',', third_delim + 1);

      String val_1 = nutrient_string.substring(0, first_delim);
      String val_2 = nutrient_string.substring(first_delim+1, second_delim);
      String val_3 = nutrient_string.substring(second_delim+1, third_delim);
      String val_4 = nutrient_string.substring(third_delim+1, fourth_delim);

      char buf[val_1.length()];
      val_1.toCharArray(buf,val_1.length());
      nutrient_val_1 = atof(buf);
      
      char buf2[val_2.length()];
      val_2.toCharArray(buf2,val_2.length());
      nutrient_val_2 = atof(buf2);

      char buf3[val_3.length()];
      val_3.toCharArray(buf3,val_3.length());
      nutrient_val_3 = atof(buf3); 
      
      char buf4[val_4.length()];
      val_4.toCharArray(buf4,val_4.length());
      nutrient_val_4 = atof(buf4);
      
      // update connected status
      lastConnected = client.connected();
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
    while(client.available()) {
        char c = client.read();
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (incoming)
        {
          if(c == '$')
          {
            String temp_buffer = nutrient_string_buffer;
            nutrient_string_buffer     = "";
            incoming           = 0;
            return temp_buffer;
          }
          nutrient_string_buffer += c; 
        }
        if(c == '$'){ 
          incoming = 1;
        }
 
   }
  }
  
  // if there's no net connection, but there was one last time
  // through the loop, then stop the client:
  if (!client.connected() && lastConnected) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
  
  return nutrient_string;
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

// this method makes a HTTP connection to the server:
void httpRequest() {
  // if there's a successful connection:
  if (client.connect(server, 80)) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    client.println("GET /sync HTTP/1.0");
    client.println("Host: seed-hydroponics.herokuapp.com");
    client.println("User-Agent: arduino-ethernet");
    client.println("Connection: close");
    client.println();

    // note the time that the connection was made:
    lastConnectionTime = millis();
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
    Serial.println("disconnecting.");
    client.stop();
  }
}

  

  

