
#define triacPulse 26  // pin goes to moc3021
#include <WiFi.h>
#define ZVC 18// pin comes from 4n257
int led = 0;
int y,z ;
int red = 25, blue = 27, green = 14, relay = 33;
int c = 150;
const char* ssid     = "Galaxy ash";    //wifi name
const char* password = "ashwin77";   //wifi password
WiFiServer server(80);

void setup() {
 
     pinMode(ZVC, INPUT_PULLUP);
     pinMode(33,OUTPUT);
    
  pinMode(triacPulse, OUTPUT);
  
  
 
  ledcSetup(0, 5000, 8);
  ledcAttachPin(blue, 0);
  
  ledcSetup(1, 5000, 8);
  ledcAttachPin(red, 1);
  
  ledcSetup(2, 5000, 8);
  ledcAttachPin(green, 2);
  

    Serial.begin(115200);
    

    delay(10);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected.");
    
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
  attachInterrupt(ZVC, acon, RISING);  
    server.begin();
digitalWrite(33,HIGH);
 pinMode(2,OUTPUT);

}

void loop()  {  
     WiFiClient client = server.available();   // listen for incoming clients
     if (WiFi.status() == WL_CONNECTED)
     {
      digitalWrite(2,HIGH);
     }
  if (client) {                             // if you get a client,
    Serial.println("New Client.");           // print a message out the serial port
                   // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {  

       y = client.parseInt();//

       if (y==1)
{      led = 1;}
else if(y==2)
{
  led = 0;
}
   else if(y==3)
{
  ledcWrite(0, 255);                 ///////////blue
  ledcWrite(1, 0);
  ledcWrite(2, 0);
}

 else if(y==4)
{
   ledcWrite(1, 255);           ////red
  ledcWrite(2, 0);
  ledcWrite(0, 0);
}

else if(y==5)
{
   ledcWrite(2, 255);
  ledcWrite(1, 0);                //green
  ledcWrite(0, 0);
}
       
else if(y==6)
{
   ledcWrite(0, 255);
  ledcWrite(1, 255);                //pink
  ledcWrite(2, 0);
}
 else if(y == 7)
 {
  ledcWrite(0,0);                   //orange
  ledcWrite(1,255);
  ledcWrite(2,140);
 }
else if(y == 8)
 {
  ledcWrite(0,255);                   //orange
  ledcWrite(1,255);
  ledcWrite(2,255);
 }
           
       else
       {
        if (y != 0)
        {
          c = y;
        }
       
        if (c<150)
        {
          c = 150;
        }
        if (c > 700)
        {
          c = 700;
        }
        z = ((c-150) * 3400)/550;
        z += 1300;
        z = 4700-z;
        z += 1300; 
         
               }
// Serial.println(z); 
      if (led == 1)
      {
        digitalWrite(33,LOW);         
      }
      else
      {
        digitalWrite(33,HIGH);
      }
         
               
               
               }
    // close the connection:
   
  }
}
        

           
  }



void acon()
{ 
  delayMicroseconds(z);
   digitalWrite(triacPulse, HIGH);
   delayMicroseconds(10);
   
  // Serial.println("hiohg");
   digitalWrite(triacPulse, LOW);
 
   
  
   
}
