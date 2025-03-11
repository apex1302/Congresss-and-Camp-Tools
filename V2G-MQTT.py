import paho.mqtt.client as mqtt
import ssl
import json
from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.routing import on
import asyncio

# MQTT Broker details
MQTT_BROKER = "your-mqtt-broker.com"
MQTT_PORT = 8883  # Secure MQTT port
MQTT_TOPIC_SUB = "v2g/input"
MQTT_TOPIC_PUB = "v2g/output"
MQTT_USERNAME = "your_username"
MQTT_PASSWORD = "your_password"

# OCPP ChargePoint class
class ChargePoint(cp):
    @on("SetChargingProfile")
    async def on_set_charging_profile(self, charging_profile):
        print(f"Received charging profile: {charging_profile}")
        return call.SetChargingProfilePayload(status="Accepted")
    
    @on("Authorize")
    async def on_authorize(self, id_tag):
        # Simulating getting the car make via authorization
        car_make = "Tesla" if "TESLA" in id_tag.upper() else "Unknown"
        if car_make == "Tesla":
            print("Error: Tesla detected. Stopping operation.")
            self.stop_charging()
            return call.AuthorizePayload(id_tag_info={"status": "Rejected"})
        return call.AuthorizePayload(id_tag_info={"status": "Accepted"})
    
    def stop_charging(self):
        print("Stopping all charging operations due to Tesla detection.")
        # Logic to stop charging via OCPP
        self.send(call.RemoteStopTransactionPayload(transaction_id="1234"))

# Simulated ISO 15118 V2G message processing using OCPP
def process_v2g_message(message):
    try:
        data = json.loads(message)
        charging_power = data.get("charging_power", 10)  # Default to 10kW
        print(f"Received charging power request: {charging_power} kW")
        
        # Example control logic: Adjust the charging current
        charging_current = charging_power / 230  # Assuming 230V AC supply
        response = json.dumps({
            "charging_current": round(charging_current, 2),
            "status": "Accepted"
        })
        return response
    except Exception as e:
        print(f"Error processing V2G message: {e}")
        return json.dumps({"error": "Invalid message format"})

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
