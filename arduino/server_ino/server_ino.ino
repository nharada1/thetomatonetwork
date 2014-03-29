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
const int LIGHT_PIN = 3;
const int PLANT_PINS [] = {4,5,6,7}; 
const unsigned long WATER_CYCLE_PERIOD = 7200000; // 2 hours
const unsigned long LIGHT_CYCLE_PERIOD = 43200000; // 12 hours

// Control variables
// Run for approx. hour on, hour off at the start
double pumpState[] = {.5,.5,.5,.5};
boolean waterCycleStarted [] = {false,false,false,false};
float lightState = 0;


/*
  Web Communication for Hydroponics
    - Uses about 5% of computation time to communicate with home server
    - parses nutrient data from server's sync view

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

  }
  // give the Ethernet shield a second to initialize:
  delay(1000);
  
  pinMode(LIGHT_PIN,OUTPUT);
  digitalWrite(LIGHT_PIN,LOW);
  int i=0;
  for(i; i<NUM_PLANTS; i++){
    pinMode(PLANT_PINS[i],OUTPUT);
    digitalWrite(PLANT_PINS[i],LOW);
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
      
      if (!nutrient_string.equals(""))
      {
      // Parse nutrient_string
      int first_delim  = nutrient_string.indexOf(',');
      int second_delim = nutrient_string.indexOf(',', first_delim + 1);
      int third_delim  = nutrient_string.indexOf(',', second_delim + 1);
      int fourth_delim = nutrient_string.indexOf(',', third_delim + 1);
      int fifth_delim = nutrient_string.indexOf(',', fourth_delim + 1)

      String val_1 = nutrient_string.substring(0, first_delim);
      String val_2 = nutrient_string.substring(first_delim+1, second_delim);
      String val_3 = nutrient_string.substring(second_delim+1, third_delim);
      String val_4 = nutrient_string.substring(third_delim+1, fourth_delim);
      String val_5 = nutrient_string.substring(fourth_delim+1, fifth_delim);

      char buf[val_1.length()];
      val_1.toCharArray(buf,val_1.length());
      pumpState[0] = atof(buf);
      
      char buf2[val_2.length()];
      val_2.toCharArray(buf2,val_2.length());
      pumpState[1] = atof(buf2);

      char buf3[val_3.length()];
      val_3.toCharArray(buf3,val_3.length());
      pumpState[2] = atof(buf3); 
      
      char buf4[val_4.length()];
      val_4.toCharArray(buf4,val_4.length());
      pumpState[3] = atof(buf4);
      
      char buf5[val_5.length()];
      val_5.toCharArray(buf5,val_5.length());
      lightState = atof(buf5);

      // update connected status
      lastConnected = client.connected();
      }
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
            Serial.println("The recieved nute values: ");
            Serial.println(temp_buffer);
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

/*******************************
 *** Plant care control code ***
 ***                         ***
 *** Author: John Pothier    ***
 *** Date: 3/26/14           ***
 *******************************/

void updatePlantCare(){
  int i=0;
  unsigned long currentMillis = millis();
  // Water

   for(i; i<NUM_PLANTS; i++){
      if(!waterCycleStarted[i] && int(pumpState[i])){
        digitalWrite(PLANT_PINS[i],HIGH);
        waterCycleStarted[i] = true;
        Serial.print("Started new water cycle for plant ");
        Serial.println(i);
      }
      else if(waterCycleStarted[i] && !int(pumpState[i])){
          digitalWrite(PLANT_PINS[i],LOW);
          Serial.print("Stopped water cycle for plant ");
          Serial.println(i);
          waterCycleStarted[i] = false;
        }   
    } 

  // Light
  if(lightState && digitalRead(LIGHT_PIN) == LOW)
  {
      digitalWrite(LIGHT_PIN,HIGH);
      Serial.println("Toggled light on");
  }
  else if(!lightState && digitalRead(LIGHT_PIN) == HIGH) 
     {
       digitalWrite(LIGHT_PIN,LOW);
       Serial.println("Toggled light OFF");
     }
  }
}


  

