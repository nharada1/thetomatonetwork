#include <Ethernet.h>
#include <SPI.h>

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
unsigned long lastConnectionTime = 0;          // last time you connected to the server, in milliseconds
boolean lastConnected = false;                 // state of the connection last time through the main loop
const unsigned long postingInterval = 10*1000;  // delay between updates, in milliseconds

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0F, 0x3B, 0xE2 };
char server[] = "http://seed-hydroponics.herokuapp.com";


void setup()
{
  // Init command buffer to empty
  command_buffer = "";
  command        = command_buffer;
  
  // Begin serial comm
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("Initializing seed hydroponics server");
  // start the Ethernet connection and the server:
  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    while(true);
  }
  // give the Ethernet shield a second to initialize:
  delay(1000);

    
  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
  }
  // print your local IP address:
  Serial.println(Ethernet.localIP());
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
      
      if (client.available()) {
        char c = client.read();
        Serial.print(c);
      }

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
      
      // update connected status
      lastConnected = client.connected();
    }
    
    // Check if this is a cycle dedicated for handling plantcare
    if(cycleCheck(&plantcareLastMillis, plantcareCycle))
    {
      //if(command)
      //Serial.println(command);
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
       return command_buffer;
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

  

  

