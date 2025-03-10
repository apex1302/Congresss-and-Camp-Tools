import paho.mqtt.client as mqtt
import ssl
import json
import open_v2g  

# MQTT Broker details
MQTT_BROKER = "your-mqtt-broker.com"
MQTT_PORT = 8883  # Secure MQTT port
MQTT_TOPIC_SUB = "v2g/input"
MQTT_TOPIC_PUB = "v2g/output"
MQTT_USERNAME = "your_username"
MQTT_PASSWORD = "your_password"

# Simulated ISO 15118 V2G message processing using open_v2g
def process_v2g_message(message):
    try:
        v2g_session = open_v2g.parse_message(message)
        charging_power = v2g_session.get_requested_power()
        print(f"Received charging power request: {charging_power} kW")
        
        # Example control logic: Adjust the charging current
        charging_current = charging_power / 230  # Assuming 230V AC supply
        response = open_v2g.create_response(charging_current)
        return response
    except Exception as e:
        print(f"Error processing V2G message: {e}")
        return json.dumps({"error": "Invalid ISO 15118 message format"})

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!" if rc == 0 else f"Failed to connect, return code {rc}")
    client.subscribe(MQTT_TOPIC_SUB)

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    response = process_v2g_message(msg.payload.decode())
    client.publish(MQTT_TOPIC_PUB, response)

# MQTT Client Setup
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()

