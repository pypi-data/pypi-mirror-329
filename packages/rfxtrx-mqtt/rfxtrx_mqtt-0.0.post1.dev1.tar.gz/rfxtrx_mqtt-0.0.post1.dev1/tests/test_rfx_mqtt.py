import pytest
from unittest.mock import MagicMock, patch
from rfxtrx.rfx_mqtt import main

@patch("rfxtrx.rfx_mqtt.RFXtrx")
@patch("rfxtrx.rfx_mqtt.MQTTHandler")
@patch("rfxtrx.rfx_mqtt.argparse.ArgumentParser.parse_args")
def test_main(mock_parse_args, mock_mqtt_handler, mock_rfxtrx):
    mock_parse_args.return_value = MagicMock(
        device="/dev/ttyUSB0",
        baudrate=38400,
        timeout=1,
        readsize=16,
        mqtt_host="localhost",
        mqtt_port=1883,
        mqtt_user=None,
        mqtt_password=None,
        mqtt_topic="rfxtrx"
    )
    main()
    mock_mqtt_handler.assert_called_once()
    mock_rfxtrx.assert_called_once()
