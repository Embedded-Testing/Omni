from saleae import automation
import __main__


class SaleaConnectionTimeout(Exception):
    pass


class SaleaConfigurationError(Exception):
    pass


def config_spi_channels(MISO=None, MOSI=None, Enable=None, Clock=None) -> dict:
    spi_channels_dict = {}
    if (MISO != None):
        spi_channels_dict["MISO"] = int(MISO)
    if (MOSI != None):
        spi_channels_dict["MOSI"] = int(MOSI)
    if (Enable != None):
        spi_channels_dict["Enable"] = int(Enable)
    if (Clock != None):
        spi_channels_dict["Clock"] = int(Clock)
    return spi_channels_dict


def config_spi_protocol(DATA_FRAME_SIZE, FIRST_BIT, CPOL, CPHA, EnableLineActiveOn) -> dict:
    DATA_FRAME_SIZE = str(DATA_FRAME_SIZE)
    FIRST_BIT = str(FIRST_BIT)
    CPOL = str(CPOL)
    CPHA = str(CPHA)
    EnableLineActiveOn = str(EnableLineActiveOn)
    return __build_protocol_dict(DATA_FRAME_SIZE, FIRST_BIT, CPOL,
                                 CPHA, EnableLineActiveOn)


def __build_protocol_dict(DATA_FRAME_SIZE: str, FIRST_BIT: str, CPOL: str, CPHA: str, EnableLineActiveOn: str) -> dict:
    protocol_dict = {}
    __extract_frame_size(DATA_FRAME_SIZE, protocol_dict)
    __extract_first_bit_type(FIRST_BIT, protocol_dict)
    __extract_polarity(CPOL, protocol_dict)
    __extract_phase(CPHA, protocol_dict)
    __extract_active_line(EnableLineActiveOn, protocol_dict)
    return protocol_dict


def __extract_active_line(EnableLineActiveOn: str, protocol_dict: dict):
    if (EnableLineActiveOn == '0' or EnableLineActiveOn == '1'):
        protocol_dict["EnableLineActive"] = str(EnableLineActiveOn)
    else:
        raise Exception("EnableLineActive value " +
                        EnableLineActiveOn+" not valid")


def __extract_phase(CPHA: str, protocol_dict: dict):
    if (CPHA == '0' or CPHA == '1'):
        protocol_dict["CPHA"] = str(CPHA)
    else:
        raise Exception("CPHA value "+CPHA+" not valid")


def __extract_polarity(CPOL: str, protocol_dict: dict):
    if (CPOL == '0' or CPOL == '1'):
        protocol_dict["CPOL"] = str(CPOL)
    else:
        raise Exception("CPOL value "+CPOL+" not valid")


def __extract_first_bit_type(FIRST_BIT: str, protocol_dict: dict):
    if (FIRST_BIT == 'MSB' or FIRST_BIT == 'LSB'):
        protocol_dict["FIRST_BIT"] = str(FIRST_BIT)
    else:
        raise Exception("FIRST_BIT value "+FIRST_BIT+" not valid")


def __extract_frame_size(DATA_FRAME_SIZE: str, protocol_dict: dict):
    if (DATA_FRAME_SIZE == '8' or DATA_FRAME_SIZE == '16'):
        protocol_dict["DATA_FRAME_SIZE"] = str(DATA_FRAME_SIZE)
    else:
        raise Exception("DATA_FRAME_SIZE value " +
                        DATA_FRAME_SIZE+" not valid")


class LogicAnalyzer:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.__device_configuration = None
        self.__capture_configuration = None
        self.manager = None
        return

    def connect_to_backend(self, port=10430, address='127.0.0.1', timeout_seconds=3.0):
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

    def start_capture(self, device_id=None):
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

    def wait_capture_end(self):
        self.capture.wait()

    def disconnect_from_backend(self):
        self.manager.close()

    def add_spi_analyser(self, SPI_CHANNEL_CFG, PROTOCOL_CFG, label):
        CHANNEL = self._build_spi_channel_cfg(SPI_CHANNEL_CFG)
        PROTOCOL = self._build_protocol_cfg(PROTOCOL_CFG)
        spi_settings = {**CHANNEL, **PROTOCOL}
        self.spi_analyzer = self.capture.add_analyzer(
            'SPI', label=label, settings=spi_settings)
        return

    def _build_protocol_cfg(self, PROTOCOL_CFG):
        cfg = {}
        if "DATA_FRAME_SIZE" in PROTOCOL_CFG.keys():
            if PROTOCOL_CFG["DATA_FRAME_SIZE"] == '8':
                cfg["Bits per Transfer"] = '8 Bits per Transfer (Standard)'
            if PROTOCOL_CFG["DATA_FRAME_SIZE"] == '16':
                cfg["Bits per Transfer"] = '16 Bits per Transfer'
        if "FIRST_BIT" in PROTOCOL_CFG.keys():
            if PROTOCOL_CFG["FIRST_BIT"] == "MSB":
                cfg["Significant Bit"] = 'Most Significant Bit First (Standard)'
            if PROTOCOL_CFG["FIRST_BIT"] == "LSB":
                cfg["Significant Bit"] = 'Least Significant Bit First'
        if "CPOL" in PROTOCOL_CFG.keys():
            if PROTOCOL_CFG["CPOL"] == "0":
                cfg["Clock State"] = 'Clock is Low when inactive (CPOL = 0)'
            if PROTOCOL_CFG["CPOL"] == "1":
                cfg["Clock State"] = 'Clock is High when inactive (CPOL = 1)'
        if "CPHA" in PROTOCOL_CFG.keys():
            if PROTOCOL_CFG["CPHA"] == "0":
                cfg["Clock Phase"] = 'Data is Valid on Clock Leading Edge (CPHA = 0)'
            if PROTOCOL_CFG["CPHA"] == "1":
                cfg["Clock Phase"] = 'Data is Valid on Clock Trailing Edge (CPHA = 1)'
        if "EnableLineActive" in PROTOCOL_CFG.keys():
            if PROTOCOL_CFG["EnableLineActive"] == "0":
                cfg["Enable Line"] = 'Enable line is Active Low (Standard)'
            if PROTOCOL_CFG["EnableLineActive"] == "1":
                cfg["Enable Line"] = 'Enable line is Active High'
        return cfg

    def _build_spi_channel_cfg(self, SPI_CHANNEL_CFG):
        cfg = {}
        if "MISO" in SPI_CHANNEL_CFG.keys():
            cfg["MISO"] = int(SPI_CHANNEL_CFG["MISO"])
        if "MOSI" in SPI_CHANNEL_CFG.keys():
            cfg["MOSI"] = int(SPI_CHANNEL_CFG["MOSI"])
        if "Enable" in SPI_CHANNEL_CFG.keys():
            cfg["Enable"] = int(SPI_CHANNEL_CFG["Enable"])
        if "Clock" in SPI_CHANNEL_CFG.keys():
            cfg["Clock"] = int(SPI_CHANNEL_CFG["Clock"])
        return cfg
