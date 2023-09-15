from saleae import automation
import __main__


class SaleaConnectionTimeout(Exception):
    pass


class SaleaConfigurationError(Exception):
    pass


class LogicAnalyzer:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.__device_configuration = None
        self.__capture_configuration = None
        self.manager = None
        return

    def connect_to_salea_application(self, port=10430, address='127.0.0.1', timeout_seconds=3.0):
        try:
            self.manager = automation.Manager.connect(
                port=port, address=address, connect_timeout_seconds=timeout_seconds)
        except:
            raise SaleaConnectionTimeout(
                f"Unable to connect to Salea application. Verify connection on {address}:{port}")

    def set_device_configuration(self, enabled_digital_chanels=None,
                                 digital_sample_rate=None,
                                 enabled_analog_channels=None,
                                 analog_sample_rate=None,
                                 digital_threshold_volts=None):
        digital_sample_rate = self.__to_int(digital_sample_rate)
        analog_sample_rate = self.__to_int(analog_sample_rate)
        digital_threshold_volts = self.__to_float(digital_threshold_volts)
        enabled_digital_chanels = self.__ls_to_int(enabled_digital_chanels)
        enabled_analog_channels = self.__ls_to_int(enabled_analog_channels)
        self.__device_configuration = automation.LogicDeviceConfiguration(
            enabled_digital_channels=enabled_digital_chanels,
            digital_sample_rate=digital_sample_rate,
            enabled_analog_channels=enabled_analog_channels,
            analog_sample_rate=analog_sample_rate,
            digital_threshold_volts=digital_threshold_volts,
        )

    def __to_int(self, value):
        if (value != None):
            value = int(value)
        return value

    def __to_float(self, value):
        if (value != None):
            value = float(value)
        return value

    def __ls_to_int(self, value_list):
        if (value_list != None):
            value_list = [int(i) for i in value_list]
        return value_list

    def set_manual_capture(self):
        self.__capture_configuration = automation.CaptureConfiguration(
            capture_mode=automation.ManualCaptureMode()
        )

    def set_timed_capture(self, duration_seconds):
        duration_seconds = int(duration_seconds)
        self.__capture_configuration = automation.CaptureConfiguration(
            capture_mode=automation.TimedCaptureMode(duration_seconds)
        )

    def start_salea_capture(self, device_id=None):
        if (self.__device_configuration == None):
            raise SaleaConfigurationError(
                "Device Configuration Error. Execute set_device_configuration before start capture.")
        if (self.__capture_configuration == None):
            raise SaleaConfigurationError(
                "Capture Configuration Error. Execute set_timed_capture or set_timed_capture before start capture.")
        self.capture = self.manager.start_capture(
            device_id=device_id,
            device_configuration=self.__device_configuration,
            capture_configuration=self.__capture_configuration)
