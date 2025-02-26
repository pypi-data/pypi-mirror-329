import json
import paho.mqtt.client as mqtt

class MQTTHandler:
    """
    A class to manage MQTT connections and message publishing for RFXtrx data.
    """

    def __init__(self, host="localhost", port=1883, username=None, password=None, topic_prefix="rfxtrx", on_message_callback=None):
        """
        Initializes the MQTT client.
        :param host: MQTT broker address (default: "localhost")
        :param port: MQTT broker port (default: 1883)
        :param username: Optional MQTT username
        :param password: Optional MQTT password
        :param topic_prefix: MQTT topic prefix (default: "rfxtrx")
        :param on_message_callback: Function to handle incoming messages
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.topic_prefix = topic_prefix
        self.on_message_callback = on_message_callback

        self.client = mqtt.Client(protocol=mqtt.MQTTv5)

        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

        # Set message callback
        self.client.on_message = self._on_message

        try:
            self.client.connect(self.host, self.port, 60)
            print(f"✅ Connected to MQTT broker at {self.host}:{self.port}")
        except Exception as e:
            print(f"❌ Error connecting to MQTT broker: {e}")
            self.client = None

    def _on_message(self, client, userdata, msg):
        """
        Internal MQTT message handler.
        """
        try:
            unused_client = client
            unused_userdata = userdata
            data = json.loads(msg.payload.decode())
            print(f"📥 MQTT Received: {msg.topic} -> {data}")

            if self.on_message_callback:
                self.on_message_callback(data)
        except Exception as e:
            print(f"❌ Error processing MQTT message: {e}")

    def publish(self, data):
        """
        Publishes RFXtrx data to an MQTT topic.
        :param data: Dictionary containing RFXtrx JSON data
        """
        if self.client:
            topic = f"{self.topic_prefix}/{data['packet_type']}"
            payload = json.dumps(data)
            try:
                self.client.publish(topic, payload)
                print(f"📡 MQTT Published: {topic} -> {payload}")
            except Exception as e:
                print(f"❌ MQTT Error: {e}")

    def subscribe(self, topic=None):
        """
        Subscribes to MQTT topics.
        :param topic: The MQTT topic to listen to (default: 'rfxtrx/#')
        """
        if self.client:
            topic = topic or f"{self.topic_prefix}/#"
            self.client.subscribe(topic)
            print(f"🔎 Subscribed to MQTT topic: {topic}")
            self.client.loop_start()

    def disconnect(self):
        """
        Disconnects the MQTT client.
        """
        if self.client:
            self.client.disconnect()
            print("🔌 Disconnected from MQTT broker")
