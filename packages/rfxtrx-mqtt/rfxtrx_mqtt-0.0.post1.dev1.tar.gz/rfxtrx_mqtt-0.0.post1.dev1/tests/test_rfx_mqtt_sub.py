import pytest
from unittest.mock import MagicMock, patch
from rfxtrx.rfx_mqtt_sub import main

@patch("rfxtrx.rfx_mqtt_sub.mqtt.Client")
@patch("rfxtrx.rfx_mqtt_sub.argparse.ArgumentParser.parse_args")
def test_main(mock_parse_args, mock_mqtt_client):
    mock_parse_args.return_value = MagicMock(
        mqtt_host="localhost",
        mqtt_port=1883,
        mqtt_user=None,
        mqtt_password=None,
        mqtt_topic="rfxtrx/#"
    )
    main()
    mock_mqtt_client.assert_called_once()
