#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = '0.tcp.ap.ngrok.io'
MQTT_PORT = 10016
MQTT_TOPIC = '/chacharin/servo'

class ServoPublisherGUI:
    def __init__(self):
        # Set up MQTT client and connect
        self.client = mqtt.Client()
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print("Connected to MQTT broker")
        except Exception as e:
            print(f"Could not connect to MQTT broker: {e}")

        # Set up GUI
        self.root = tk.Tk()
        self.root.title("Servo Publisher")

        self.label = tk.Label(self.root, text="Enter Servo Value:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_value)
        self.send_button.pack(pady=10)

    def send_value(self):
        value = self.entry.get()
        if value:
            self.client.publish(MQTT_TOPIC, str(value))
            print(f"Sent: {value}")
            messagebox.showinfo("MQTT", f"Sent: {value}")
        else:
            messagebox.showwarning("Input Error", "Please enter a value.")

    def run(self):
        self.root.mainloop()

def main():
    app = ServoPublisherGUI()
    app.run()

if __name__ == '__main__':
    main()

