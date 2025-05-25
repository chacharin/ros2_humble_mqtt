#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "MARA1";
const char* password = "MARAMARA1";

// MQTT broker details
const char* mqtt_server = "0.tcp.ap.ngrok.io";
const int mqtt_port = 11882;
const char* mqtt_topic = "/chacharin/button";

// Button setup
const int BUTTON_PIN = 27;
int lastButtonState = HIGH;  // default not pressed (INPUT_PULLUP)

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected. IP: " + WiFi.localIP().toString());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    String clientId = "ESP32Client-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed (rc=");
      Serial.print(client.state());
      Serial.println("), retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int currentState = digitalRead(BUTTON_PIN);

  // Detect bump: HIGH -> LOW transition (button press)
  if (lastButtonState == HIGH && currentState == LOW) {
    Serial.println("Button bumped! Sending message...");
    client.publish(mqtt_topic, "1");
    delay(50);  // Short debounce
  }

  lastButtonState = currentState;
}
