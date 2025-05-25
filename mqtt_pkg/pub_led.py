#!/usr/bin/env python3

import tkinter as tk
import paho.mqtt.client as mqtt

MQTT_BROKER = '0.tcp.ap.ngrok.io'
MQTT_PORT = 10016
MQTT_TOPIC = '/chacharin/led'

class MqttGui:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)

        self.root = tk.Tk()
        self.root.title("MQTT LED Controller")

        self.button_on = tk.Button(self.root, text="ON", command=self.publish_on)
        self.button_on.pack(pady=10)

        self.button_off = tk.Button(self.root, text="OFF", command=self.publish_off)
        self.button_off.pack(pady=10)

    def publish_on(self):
        self.client.publish(MQTT_TOPIC, "on")
        print("Sent MQTT message: on")

    def publish_off(self):
        self.client.publish(MQTT_TOPIC, "off")
        print("Sent MQTT message: off")

    def run(self):
        self.root.mainloop()

def main():
    gui = MqttGui()
    gui.run()

if __name__ == '__main__':
    main()

