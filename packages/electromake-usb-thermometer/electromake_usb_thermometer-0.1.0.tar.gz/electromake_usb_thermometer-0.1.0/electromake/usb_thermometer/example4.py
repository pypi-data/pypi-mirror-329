import paho.mqtt.client as mqtt
import json
import time
import random
from .thermometer import *

# MQTT Configuration
MQTT_BROKER = "192.168.0.104"  # Replace with your MQTT broker IP
MQTT_PORT = 1883  # Default MQTT port
# MQTT_USER = "your_username"  # Change if authentication is required
# MQTT_PASSWORD = "your_password"
SENSOR_NAME = "USB_Temperature_Sensor"
DISCOVERY_TOPIC = f"homeassistant/sensor/{SENSOR_NAME}/config"
STATE_TOPIC = f"homeassistant/sensor/{SENSOR_NAME}/state"

# Connect to MQTT Broker
client = mqtt.Client()

# If authentication is required, set username and password
# client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Home Assistant MQTT Discovery Payload
sensor_config = {
    "name": "Temperature Sensor",
    "state_topic": STATE_TOPIC,
    "unit_of_measurement": "°C",
    "device_class": "temperature",
    "value_template": "{{ value_json.temperature }}",
    "unique_id": SENSOR_NAME,
    "device": {
        "identifiers": [SENSOR_NAME],
        "name": "USB Thermometer",
        "manufacturer": "Electromake",
        "model": "1.0",
    }
}

# Publish discovery message
client.publish(DISCOVERY_TOPIC, json.dumps(sensor_config), retain=True)

print(f"[INFO] Published MQTT discovery message for {SENSOR_NAME}")

def publish_temperature():
    usb_therm = USBThermometer("/dev/ttyUSB0")
    usb_therm.discover_ROMs(alarm=False)
    while True:
        T = usb_therm.read_temperature(0)
        payload = json.dumps({"temperature": f"{T:3.1f}"})
        client.publish(STATE_TOPIC, payload)
        print(f"[INFO] Published Temperature: {T:3.1f} °C")
        time.sleep(15)  # Publish every 15 seconds

# Start publishing temperature values
publish_temperature()
