#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import tkinter as tk
from tkinter import ttk
import threading
import paho.mqtt.client as mqtt
import time

from geometry_msgs.msg import Twist  # ✅ Import Twist message

# MQTT Configuration
MQTT_BROKER = '0.tcp.ap.ngrok.io'
MQTT_PORT = 11882
MQTT_TOPIC = '/chacharin/button'

class MQTTButtonListener(Node):
    def __init__(self):
        super().__init__('mqtt_button_listener')
        self.counter = 0
        self.last_msg_time = time.time()

        # ✅ Create publisher for /turtle1/cmd_vel
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Start GUI in a separate thread
        self.gui_thread = threading.Thread(target=self.init_gui, daemon=True)
        self.gui_thread.start()

        # Set up MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

        # Start MQTT loop in a thread
        self.mqtt_thread = threading.Thread(target=self.mqtt_client.loop_forever, daemon=True)
        self.mqtt_thread.start()

        # Watchdog loop to turn off light after 1 second
        self.watchdog_thread = threading.Thread(target=self.watchdog_loop, daemon=True)
        self.watchdog_thread.start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.get_logger().info("Connected to MQTT broker")
            client.subscribe(MQTT_TOPIC)
        else:
            self.get_logger().error(f"MQTT connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        if message == "1":
            self.counter += 1
            self.last_msg_time = time.time()
            self.update_gui()
            self.publish_cmd_vel()  # ✅ Publish to turtle1/cmd_vel

    def publish_cmd_vel(self):
        # ✅ Create and publish Twist message
        twist_msg = Twist()
        twist_msg.linear.x = 1.0
        twist_msg.angular.z = 1.0
        self.cmd_vel_publisher.publish(twist_msg)
        self.get_logger().info("Published cmd_vel: linear.x=1.0, angular.z=1.0")

    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("MQTT Button Counter")
        self.root.geometry("500x350")
        self.root.configure(bg="#2c3e50")

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", background="#2c3e50", foreground="white", font=("Helvetica", 18, "bold"))

        self.counter_label = ttk.Label(self.root, text="Count: 0")
        self.counter_label.pack(pady=30)

        self.light_canvas = tk.Canvas(self.root, width=150, height=150, bg="#2c3e50", highlightthickness=0)
        self.light_id = self.light_canvas.create_oval(10, 10, 140, 140, fill="gray")
        self.light_canvas.pack(pady=20)

        self.root.mainloop()

    def update_gui(self):
        if hasattr(self, 'counter_label'):
            self.counter_label.config(text=f"Count: {self.counter}")
        self.set_light_color("green")

    def set_light_color(self, color):
        if hasattr(self, 'light_canvas') and hasattr(self, 'light_id'):
            self.light_canvas.itemconfig(self.light_id, fill=color)

    def watchdog_loop(self):
        while True:
            current_time = time.time()
            if current_time - self.last_msg_time > 1.0:
                self.set_light_color("gray")
            time.sleep(0.1)

def main(args=None):
    rclpy.init(args=args)
    node = MQTTButtonListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

