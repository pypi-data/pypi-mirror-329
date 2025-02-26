#!/usr/bin/env python3
import argparse
import json
from rfxtrx.mqtt_handler import MQTTHandler

def main():
    parser = argparse.ArgumentParser(description="Standalone MQTT publisher for RFXtrx data.")
    parser.add_argument("--mqtt-host", type=str, default="localhost", help="MQTT broker hostname or IP")
    parser.add_argument("--mqtt-port", type=int, default=1883, help="MQTT broker port (default: 1883)")
    parser.add_argument("--mqtt-user", type=str, help="MQTT username (optional)")
    parser.add_argument("--mqtt-password", type=str, help="MQTT password (optional)")
    parser.add_argument("--mqtt-topic", type=str, default="rfxtrx", help="MQTT topic prefix (default: 'rfxtrx')")
    parser.add_argument("--data", type=str, required=True, help="JSON string of the data to publish")

    args = parser.parse_args()

    # Setup MQTT client
    mqtt_client = MQTTHandler(
        host=args.mqtt_host,
        port=args.mqtt_port,
        username=args.mqtt_user,
        password=args.mqtt_password,
        topic_prefix=args.mqtt_topic
    )

    try:
        data = json.loads(args.data)
        mqtt_client.publish(data)
        print(f"✅ Published to {args.mqtt_topic}: {data}")
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format.")

if __name__ == "__main__":
    main()
