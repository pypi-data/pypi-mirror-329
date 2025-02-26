#!/usr/bin/env python3
import argparse
from rfxtrx.rfxtrx import RFXtrx
from rfxtrx.mqtt_handler import MQTTHandler

def handle_mqtt_command(data):
    """
    Function to handle incoming MQTT messages and process RFXtrx commands.
    """
    print(f"🔄 Processing MQTT command: {data}")

def main():
    parser = argparse.ArgumentParser(description="RFXtrx to MQTT bridge.")
    parser.add_argument("-d", "--device", type=str, default="/dev/ttyUSB0", help="Serial device path (default: /dev/ttyUSB0)")
    parser.add_argument("-b", "--baudrate", type=int, default=38400, help="Baud rate (default: 38400)")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout in seconds (default: 1)")
    parser.add_argument("-r", "--readsize", type=int, default=16, help="Number of bytes to read at a time (default: 16)")

    # MQTT Parameters
    parser.add_argument("--mqtt-host", type=str, default="localhost", help="MQTT broker hostname or IP")
    parser.add_argument("--mqtt-port", type=int, default=1883, help="MQTT broker port (default: 1883)")
    parser.add_argument("--mqtt-user", type=str, help="MQTT username (optional)")
    parser.add_argument("--mqtt-password", type=str, help="MQTT password (optional)")
    parser.add_argument("--mqtt-topic", type=str, default="rfxtrx", help="MQTT topic prefix (default: 'rfxtrx')")

    args = parser.parse_args()

    # Setup MQTT client
    mqtt_client = MQTTHandler(
        host=args.mqtt_host,
        port=args.mqtt_port,
        username=args.mqtt_user,
        password=args.mqtt_password,
        topic_prefix=args.mqtt_topic,
        on_message_callback=handle_mqtt_command
    )

    # Subscribe to MQTT topic
    mqtt_client.subscribe(f"{args.mqtt_topic}/#")

    # Define callback function
    def mqtt_callback(data):
        mqtt_client.publish(data)

    # Start listening for RFXtrx messages and forward to MQTT
    rfxtrx = RFXtrx(
        device=args.device,
        baudrate=args.baudrate,
        timeout=args.timeout,
        readsize=args.readsize,
        callback=mqtt_callback
    )

    print(f"🔄 RFXtrx to MQTT bridge started on {args.device}, publishing to {args.mqtt_topic}/<packet_type>")
    rfxtrx.start()

if __name__ == "__main__":
    main()
