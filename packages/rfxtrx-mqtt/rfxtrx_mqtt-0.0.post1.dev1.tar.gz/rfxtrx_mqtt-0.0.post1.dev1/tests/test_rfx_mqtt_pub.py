import pytest
from unittest.mock import MagicMock, patch
from rfxtrx.rfx_mqtt_pub import main

@patch("rfxtrx.rfx_mqtt_pub.MQTTHandler")
@patch("rfxtrx.rfx_mqtt_pub.argparse.ArgumentParser.parse_args")
def test_main(mock_parse_args, mock_mqtt_handler):
    mock_parse_args.return_value = MagicMock(
        mqtt_host="localhost",
        mqtt_port=1883,
        mqtt_user=None,
        mqtt_password=None,
        mqtt_topic="rfxtrx",
        data='{"packet_type": "0x10", "data": "test"}'
    )
    main()
    mock_mqtt_handler.assert_called_once()
