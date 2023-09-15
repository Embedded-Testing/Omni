import unittest
import pytest
from Omini.robotlibraries.salea import LogicAnalyzer, SaleaConfigurationError, SaleaConnectionTimeout
from unittest.mock import patch, Mock, MagicMock
from saleae.automation import *


class TestSalea(unittest.TestCase):

    def test_connect_raises_exception_if_connection_timeout(self):
        my_logic = LogicAnalyzer()
        with pytest.raises(SaleaConnectionTimeout, match=".*Unable to connect to Salea application. Verify connection on.*"):
            my_logic.connect_to_salea_application(timeout_seconds=0.1)

    @patch('saleae.automation.Manager.connect')
    def test_connect(self, mock_mgr_connect):
        my_logic = LogicAnalyzer()
        my_logic.connect_to_salea_application(timeout_seconds=1)
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
            my_logic.start_salea_capture()

    @patch('saleae.automation.Manager.start_capture')
    @patch('saleae.automation.LogicDeviceConfiguration', return_value=["mocked_configuration"])
    def test_set_start_capture_raise_exp_if_capture_not_configured(self, mock_dev_cfg, mock_cfg):
        my_logic = LogicAnalyzer()
        my_logic.set_device_configuration(
            analog_sample_rate=30000, enabled_analog_channels=[1, 2])
        with pytest.raises(SaleaConfigurationError, match=r".*Capture Configuration Error.*"):
            my_logic.start_salea_capture()

    @patch("Omini.robotlibraries.salea.SaleaLogicAnalyzer.automation.Manager")
    def test_set_start_captureX(self, mock_connect):
        my_logic = LogicAnalyzer()
        mock_manager_instance = mock_connect.connect.return_value
        mock_start_capture = MagicMock()
        mock_manager_instance.start_capture = mock_start_capture
        my_logic.connect_to_salea_application(timeout_seconds=1)
        my_logic.set_device_configuration(
            analog_sample_rate=30000, enabled_analog_channels=[1, 2])
        my_logic.set_timed_capture(3)
        my_logic.start_salea_capture()
        print(dir(my_logic))
        mock_manager_instance.start_capture.assert_called_once_with(
            device_id=None,
            device_configuration=my_logic._LogicAnalyzer__device_configuration,
            capture_configuration=my_logic._LogicAnalyzer__capture_configuration
        )
