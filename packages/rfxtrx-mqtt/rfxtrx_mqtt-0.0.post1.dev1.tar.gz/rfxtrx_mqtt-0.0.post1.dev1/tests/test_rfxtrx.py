import pytest
from unittest.mock import MagicMock, patch
from rfxtrx.rfxtrx import RFXtrx

@pytest.fixture
def rfxtrx():
    return RFXtrx(device="/dev/ttyUSB0", baudrate=38400, timeout=1, readsize=16)

def test_rfxtrx_init(rfxtrx):
    assert rfxtrx.device == "/dev/ttyUSB0"
    assert rfxtrx.baudrate == 38400
    assert rfxtrx.timeout == 1
    assert rfxtrx.readsize == 16

#def test_rfxtrx_parse_data(rfxtrx):
#    data = b'\x0a\x14\x00\x00\x00\x00\x00\x00\x00\x00'
#    parsed_data = rfxtrx.parse_data(data)
#    assert parsed_data["packet_type"] == "Unknown"

#@patch("rfxtrx.rfxtrx.serial.Serial")
#def test_rfxtrx_start(mock_serial, rfxtrx):
#    mock_serial_instance = mock_serial.return_value
#    mock_serial_instance.read.return_value = b'\x0a\x14\x00\x00\x00\x00\x00\x00\x00\x00'
#    rfxtrx.callback = MagicMock()
#    rfxtrx.start()
#    rfxtrx.callback.assert_called_once()
