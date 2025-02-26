#!/usr/bin/env python3
import argparse
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    unused_client = client
    unused_userdata = userdata
    print(f"📥 Received message on {msg.topic}: {msg.payload.decode()}")

def main():
    parser = argparse.ArgumentParser(description="MQTT subscriber for RFXtrx messages.")
    parser.add_argument("--mqtt-host", type=str, default="localhost", help="MQTT broker hostname or IP")
    parser.add_argument("--mqtt-port", type=int, default=1883, help="MQTT broker port (default: 1883)")
    parser.add_argument("--mqtt-user", type=str, help="MQTT username (optional)")
    parser.add_argument("--mqtt-password", type=str, help="MQTT password (optional)")
    parser.add_argument("--mqtt-topic", type=str, default="rfxtrx/#", help="MQTT topic to subscribe to (default: 'rfxtrx/#')")

    args = parser.parse_args()

    # Setup MQTT client
    client = mqtt.Client()
    if args.mqtt_user and args.mqtt_password:
        client.username_pw_set(args.mqtt_user, args.mqtt_password)

    client.on_message = on_message
    client.connect(args.mqtt_host, args.mqtt_port, 60)
    client.subscribe(args.mqtt_topic)

    print(f"🔎 Listening for MQTT messages on topic '{args.mqtt_topic}'...")
    client.loop_forever()

if __name__ == "__main__":
    main()
