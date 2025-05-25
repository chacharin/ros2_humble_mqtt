#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

// WiFi credentials
const char* ssid = "MARA1";
const char* password = "MARAMARA1";

// MQTT broker details
const char* mqtt_server = "0.tcp.ap.ngrok.io";
const int mqtt_port = 11882;
const char* mqtt_topic = "/chacharin/servo";

// Servo configuration
Servo myservo;
const int SERVO_PIN = 14;

// WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

// Connect to WiFi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

// Handle incoming MQTT messages
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  String msg;
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  Serial.println(msg);

  // Convert message to int and move servo
  int angle = msg.toInt();
  if (angle >= 0 && angle <= 180) {
    myservo.write(angle);
    Serial.print("Servo moved to: ");
    Serial.println(angle);
  } else {
    Serial.println("Invalid angle received.");
  }
}

// Ensure MQTT connection stays alive
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.subscribe(mqtt_topic);
      Serial.print("Subscribed to topic: ");
      Serial.println(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  myservo.attach(SERVO_PIN);
  setup_wifi();

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
