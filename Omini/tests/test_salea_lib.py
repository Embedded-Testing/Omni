import unittest
import pytest
from Omini.robotlibraries.SaleaLogicAnalyzer import (LogicAnalyzer,
                                                     SaleaConfigurationError,
                                                     SaleaConnectionTimeout,
                                                     config_spi_channels,
                                                     config_spi_protocol)

from unittest.mock import patch, Mock, MagicMock, ANY
from saleae.automation import *


class TestSalea(unittest.TestCase):

    def test_connect_raises_exception_if_connection_timeout(self):
        my_logic = LogicAnalyzer()
        with pytest.raises(SaleaConnectionTimeout, match=".*Unable to connect to Salea application. Verify connection on.*"):
            my_logic.connect_to_backend(timeout_seconds=0.1)

    @patch('saleae.automation.Manager.connect')
    def test_connect(self, mock_mgr_connect):
        my_logic = LogicAnalyzer()
        my_logic.connect_to_backend(timeout_seconds=1)
        mock_mgr_connect.assert_called_once_with(
            port=10430,
            address='127.0.0.1',
            connect_timeout_seconds=1
        )

    @patch('saleae.automation.LogicDeviceConfiguration')
    def test_set_device_configuration_configures_digital_channels_str(self, mock_device_cfg):
        my_logic = LogicAnalyzer()
        my_logic.set_device_configuration(
            digital_sample_rate="50000", enabled_digital_chanels=["1", "2"])
        mock_device_cfg.assert_called_once_with(
            enabled_digital_channels=[1, 2],
            digital_sample_rate=50000,
            enabled_analog_channels=None,
            analog_sample_rate=None,
            digital_threshold_volts=None
        )

    @patch('saleae.automation.LogicDeviceConfiguration')
    def test_set_device_configuration_configures_digital_channels_int(self, mock_device_cfg):
        my_logic = LogicAnalyzer()
        my_logic.set_device_configuration(
            digital_sample_rate=20000, enabled_digital_chanels=[1, 2], digital_threshold_volts=1.2)
        mock_device_cfg.assert_called_once_with(
            enabled_digital_channels=[1, 2],
            digital_sample_rate=20000,
            enabled_analog_channels=None,
            analog_sample_rate=None,
            digital_threshold_volts=1.2
        )

    @patch('saleae.automation.LogicDeviceConfiguration')
    def test_set_device_configuration_configures_analog_channels_str(self, mock_device_cfg):
        my_logic = LogicAnalyzer()
        my_logic.set_device_configuration(
            analog_sample_rate="30000", enabled_analog_channels=["1", "2"])
        mock_device_cfg.assert_called_once_with(
            enabled_digital_channels=None,
            digital_sample_rate=None,
            enabled_analog_channels=[1, 2],
            analog_sample_rate=30000,
            digital_threshold_volts=None
        )

    @patch('saleae.automation.LogicDeviceConfiguration')
    def test_set_device_configuration_configures_analog_channels_int(self, mock_device_cfg):
        my_logic = LogicAnalyzer()
        my_logic.set_device_configuration(
            analog_sample_rate=30000, enabled_analog_channels=[1, 2])
        mock_device_cfg.assert_called_once_with(
            enabled_analog_channels=[1, 2],
            analog_sample_rate=30000,
            enabled_digital_channels=None,
            digital_sample_rate=None,
            digital_threshold_volts=None
        )

    @patch('saleae.automation.CaptureConfiguration')
    def test_set_capture_mode_to_manual(self, mock_capture_cfg):
        my_logic = LogicAnalyzer()
        my_logic.set_manual_capture()
        mock_capture_cfg.assert_called_once_with(
            capture_mode=saleae.automation.ManualCaptureMode()
        )

    @patch('saleae.automation.CaptureConfiguration')
    def test_set_capture_mode_to_timmed(self, mock_capture_cfg):
        my_logic = LogicAnalyzer()
        my_logic.set_timed_capture(3)
        mock_capture_cfg.assert_called_once_with(
            capture_mode=saleae.automation.TimedCaptureMode(3)
        )

    @patch('saleae.automation.Manager.start_capture')
    @patch('saleae.automation.CaptureConfiguration', return_value=["mocked_capture"])
    def test_set_start_capture_raise_exp_if_device_not_configured(self, mock_start_capture, mock_capture):
        my_logic = LogicAnalyzer()
        my_logic.set_timed_capture(3)
        with pytest.raises(SaleaConfigurationError, match=r".*Device Configuration Error.*"):
            my_logic.start_capture()

    @patch('saleae.automation.Manager.start_capture')
    @patch('saleae.automation.LogicDeviceConfiguration', return_value=["mocked_configuration"])
    def test_set_start_capture_raise_exp_if_capture_not_configured(self, mock_dev_cfg, mock_cfg):
        my_logic = LogicAnalyzer()
        my_logic.set_device_configuration(
            analog_sample_rate=30000, enabled_analog_channels=[1, 2])
        with pytest.raises(SaleaConfigurationError, match=r".*Capture Configuration Error.*"):
            my_logic.start_capture()

    @patch("Omini.robotlibraries.SaleaLogicAnalyzer.SaleaLogicAnalyzer.automation.Manager")
    def test_set_start_capture(self, mock_connect):
        my_logic = LogicAnalyzer()
        mock_manager_instance = mock_connect.connect.return_value
        mock_start_capture = MagicMock()
        mock_manager_instance.start_capture = mock_start_capture
        my_logic.connect_to_backend(timeout_seconds=1)
        my_logic.set_device_configuration(
            analog_sample_rate=30000, enabled_analog_channels=[1, 2])
        my_logic.set_timed_capture(3)
        my_logic.start_capture()
        print(dir(my_logic))
        mock_manager_instance.start_capture.assert_called_once_with(
            device_id=None,
            device_configuration=my_logic._LogicAnalyzer__device_configuration,
            capture_configuration=my_logic._LogicAnalyzer__capture_configuration
        )

    def test_wait_capture_end_calls_api(self):
        my_logic = LogicAnalyzer()
        mock_wait = Mock()
        my_logic.capture = mock_wait
        my_logic.wait_capture_end()
        mock_wait.wait.assert_called_once()

    def test_disconnect_from_backend_calls_close(self):
        my_logic = LogicAnalyzer()
        mock_disconnect = Mock()
        my_logic.manager = mock_disconnect
        my_logic.disconnect_from_backend()
        mock_disconnect.close.assert_called_once()

    def test_add_spi_analyser_adds_analyser_with_protocol_and_cfg(self):
        expected_dict = {'MISO': 1,
                         'MOSI': 2,
                         'Enable': 3,
                         'Clock': 4,
                         'Bits per Transfer': '8 Bits per Transfer (Standard)',
                         'Significant Bit': 'Most Significant Bit First (Standard)',
                         'Clock State': 'Clock is Low when inactive (CPOL = 0)',
                         'Clock Phase': 'Data is Valid on Clock Leading Edge (CPHA = 0)',
                         'Enable Line': 'Enable line is Active Low (Standard)'}
        my_logic = LogicAnalyzer()
        mock_spi_analyzer = Mock()
        my_logic.capture = mock_spi_analyzer
        spi_channels_cfg = config_spi_channels(
            MISO=1, MOSI=2, Enable=3, Clock=4)
        spi_protocol_cfg = config_spi_protocol(
            DATA_FRAME_SIZE=8, FIRST_BIT='MSB', CPHA=0, CPOL=0, EnableLineActiveOn=0)
        my_logic.add_spi_analyser(
            spi_channels_cfg, spi_protocol_cfg, "TEST_SPI")
        mock_spi_analyzer.add_analyzer.assert_called_with(
            'SPI', label='TEST_SPI', settings=expected_dict)

    @patch("Omini.robotlibraries.SaleaLogicAnalyzer.SaleaLogicAnalyzer.automation.capture.DataTableExportConfiguration",
           return_value="mocked_ExportConfiguration")
    def test_export_to_csv_calls_api_hex(self, mock_export_cfg):
        my_logic = LogicAnalyzer()
        mock_spi_analyzer = Mock()
        my_logic.capture = mock_spi_analyzer
        spi_channels_cfg = config_spi_channels(
            MISO=1, MOSI=2, Enable=3, Clock=4)
        spi_protocol_cfg = config_spi_protocol(
            DATA_FRAME_SIZE=8, FIRST_BIT='MSB', CPHA=0, CPOL=0, EnableLineActiveOn=0)
        my_logic.add_spi_analyser(
            spi_channels_cfg, spi_protocol_cfg, "TEST_SPI")
        my_logic.export_to_csv("/folder/to/csv/capture",
                               "capture_name.txt", "HEXADECIMAL")
        mock_export_cfg.assert_called_with(
            ANY, saleae.automation.capture.RadixType.HEXADECIMAL)
        mock_spi_analyzer.export_data_table.assert_called_with(
            filepath='/folder/to/csv/capture/capture_name.txt', analyzers=ANY)

    @patch("Omini.robotlibraries.SaleaLogicAnalyzer.SaleaLogicAnalyzer.automation.capture.DataTableExportConfiguration",
           return_value="mocked_ExportConfiguration")
    def test_export_to_csv_calls_api_bin(self, mock_export_cfg):
        my_logic = LogicAnalyzer()
        mock_spi_analyzer = Mock()
        my_logic.capture = mock_spi_analyzer
        spi_channels_cfg = config_spi_channels(
            MISO=1, MOSI=2, Enable=3, Clock=4)
        spi_protocol_cfg = config_spi_protocol(
            DATA_FRAME_SIZE=8, FIRST_BIT='MSB', CPHA=0, CPOL=0, EnableLineActiveOn=0)
        my_logic.add_spi_analyser(
            spi_channels_cfg, spi_protocol_cfg, "TEST_SPI")
        my_logic.export_to_csv("/folder/to/csv/capture",
                               "capture_name.txt", "BINARY")
        mock_export_cfg.assert_called_with(
            ANY, saleae.automation.capture.RadixType.BINARY)
        mock_spi_analyzer.export_data_table.assert_called_with(
            filepath='/folder/to/csv/capture/capture_name.txt', analyzers=ANY)

    @patch("Omini.robotlibraries.SaleaLogicAnalyzer.SaleaLogicAnalyzer.automation.capture.DataTableExportConfiguration",
           return_value="mocked_ExportConfiguration")
    def test_export_to_csv_calls_api_dec(self, mock_export_cfg):
        my_logic = LogicAnalyzer()
        mock_spi_analyzer = Mock()
        my_logic.capture = mock_spi_analyzer
        spi_channels_cfg = config_spi_channels(
            MISO=1, MOSI=2, Enable=3, Clock=4)
        spi_protocol_cfg = config_spi_protocol(
            DATA_FRAME_SIZE=8, FIRST_BIT='MSB', CPHA=0, CPOL=0, EnableLineActiveOn=0)
        my_logic.add_spi_analyser(
            spi_channels_cfg, spi_protocol_cfg, "TEST_SPI")
        my_logic.export_to_csv("/folder/to/csv/capture",
                               "capture_name.txt", "DECIMAL")
        mock_export_cfg.assert_called_with(
            ANY, saleae.automation.capture.RadixType.DECIMAL)
        mock_spi_analyzer.export_data_table.assert_called_with(
            filepath='/folder/to/csv/capture/capture_name.txt', analyzers=ANY)

    @patch("Omini.robotlibraries.SaleaLogicAnalyzer.SaleaLogicAnalyzer.automation.capture.DataTableExportConfiguration",
           return_value="mocked_ExportConfiguration")
    def test_export_to_csv_calls_api_ascii(self, mock_export_cfg):
        my_logic = LogicAnalyzer()
        mock_spi_analyzer = Mock()
        my_logic.capture = mock_spi_analyzer
        spi_channels_cfg = config_spi_channels(
            MISO=1, MOSI=2, Enable=3, Clock=4)
        spi_protocol_cfg = config_spi_protocol(
            DATA_FRAME_SIZE=8, FIRST_BIT='MSB', CPHA=0, CPOL=0, EnableLineActiveOn=0)
        my_logic.add_spi_analyser(
            spi_channels_cfg, spi_protocol_cfg, "TEST_SPI")
        my_logic.export_to_csv("/folder/to/csv/capture",
                               "capture_name.txt", "ASCII")
        mock_export_cfg.assert_called_with(
            ANY, saleae.automation.capture.RadixType.ASCII)
        mock_spi_analyzer.export_data_table.assert_called_with(
            filepath='/folder/to/csv/capture/capture_name.txt', analyzers=ANY)

    @patch("Omini.robotlibraries.SaleaLogicAnalyzer.SaleaLogicAnalyzer.automation.capture.DataTableExportConfiguration",
           return_value="mocked_ExportConfiguration")
    def test_export_to_csv_calls_api_invalid(self, mock_export_cfg):
        my_logic = LogicAnalyzer()
        mock_spi_analyzer = Mock()
        my_logic.capture = mock_spi_analyzer
        spi_channels_cfg = config_spi_channels(
            MISO=1, MOSI=2, Enable=3, Clock=4)
        spi_protocol_cfg = config_spi_protocol(
            DATA_FRAME_SIZE=8, FIRST_BIT='MSB', CPHA=0, CPOL=0, EnableLineActiveOn=0)
        my_logic.add_spi_analyser(
            spi_channels_cfg, spi_protocol_cfg, "TEST_SPI")
        with pytest.raises(ValueError, match=r".*Invalid value for radix.*"):
            my_logic.export_to_csv("/folder/to/csv/capture",
                                   "capture_name.txt", "INVALID")

    def test_sae_raw(self):
        my_logic = LogicAnalyzer()
        mock_capture = Mock()
        my_logic.capture = mock_capture
        my_logic.save_raw("/path/to/folder", "filename")
        mock_capture.save_capture.assert_called_once_with(
            filepath='/path/to/folder/filename')
