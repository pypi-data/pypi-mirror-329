import pytest
from unittest.mock import MagicMock, patch
from rfxtrx.rfx_dump import main

@patch("rfxtrx.rfx_dump.RFXtrx")
@patch("rfxtrx.rfx_dump.argparse.ArgumentParser.parse_args")
def test_main(mock_parse_args, mock_rfxtrx):
    mock_parse_args.return_value = MagicMock(
        device="/dev/ttyUSB0",
        baudrate=38400,
        timeout=1,
        readsize=16
    )
    main()
    mock_rfxtrx.assert_called_once()
