import json
import pytest
from unittest.mock import MagicMock, patch
from rfxtrx.mqtt_handler import MQTTHandler

@pytest.fixture
def mqtt_handler():
    return MQTTHandler(host="localhost", port=1883, topic_prefix="test")

def test_mqtt_handler_init(mqtt_handler):
    assert mqtt_handler.host == "localhost"
    assert mqtt_handler.port == 1883
    assert mqtt_handler.topic_prefix == "test"

def test_mqtt_handler_publish(mqtt_handler):
    mqtt_handler.client = MagicMock()
    data = {"packet_type": "0x10", "data": "test"}
    mqtt_handler.publish(data)
    mqtt_handler.client.publish.assert_called_once_with("test/0x10", json.dumps(data))

def test_mqtt_handler_subscribe(mqtt_handler):
    mqtt_handler.client = MagicMock()
    mqtt_handler.subscribe("test/topic")
    mqtt_handler.client.subscribe.assert_called_once_with("test/topic")

def test_mqtt_handler_on_message(mqtt_handler):
    mqtt_handler.on_message_callback = MagicMock()
    msg = MagicMock()
    msg.payload.decode.return_value = json.dumps({"data": "test"})
    mqtt_handler._on_message(None, None, msg)
    mqtt_handler.on_message_callback.assert_called_once_with({"data": "test"})
