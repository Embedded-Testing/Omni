import unittest
import pytest
from ..robotlibraries.salea import *
from unittest.mock import patch
from saleae.automation import *


class TestSalea(unittest.TestCase):

    def test_connect_raises_exception_if_connection_timeout(self):
        my_logic = LogicAnalyzer()
        with pytest.raises(SaleaConnectionTimeout, match=".*Unable to connect to Salea application. Verify connection on.*"):
            my_logic.connect_to_salea_application(timeout_seconds=1)

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
