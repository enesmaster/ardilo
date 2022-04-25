#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>

//enesislam [https://github.com/enesislam/get_from_api.ino]
const char* ssid     = "ENES";
const char* password = "PASSWORD_ISN_T_DEFINED";
const String url = "http://enesenes222.pythonanywhere.com/api/signal/";


void setup() {
  Serial.begin(115200);
  Serial.println("");
  Serial.print("Connecting to " + String(ssid) + " ...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
}


void loop() {
  if (WiFi.status() == WL_CONNECTED) {
   WiFiClient client;
    HTTPClient http;
    http.begin(client, url);
    int id = http.GET();
     if (id > 0) {
      String payload = http.getString();
      if(payload.indexOf("true") > 0)
        {
          const int relay = 5;
          pinMode(relay, OUTPUT);
          digitalWrite(relay, HIGH);
          Serial.println(payload);
        }
        else
        {
          const int relay = 5;
          pinMode(relay, OUTPUT);
          digitalWrite(relay, HIGH);
        }
     }
    http.end();
  }
  delay(2000);
}