from saleae import automation
import os


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
        self.analyzer_dicts = {}
        return

    def connect_to_backend(self, port=10430, address='127.0.0.1', timeout_seconds=3.0) -> None:
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
                                 digital_threshold_volts=None) -> None:
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

    def set_manual_capture(self) -> None:
        self.__capture_configuration = automation.CaptureConfiguration(
            capture_mode=automation.ManualCaptureMode()
        )

    def set_timed_capture(self, duration_seconds: int) -> None:
        duration_seconds = int(duration_seconds)
        self.__capture_configuration = automation.CaptureConfiguration(
            capture_mode=automation.TimedCaptureMode(duration_seconds)
        )

    def start_capture(self, device_id=None) -> None:
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

    def wait_capture_end(self) -> None:
        self.capture.wait()

    def disconnect_from_backend(self) -> None:
        self.manager.close()

    def add_i2c_analyser(self, i2c_channel_cfg: dict, label: str):
        self.__validate_analyser_label(label)
        i2c_analyzer = self.capture.add_analyzer(
            'I2C', label=label, settings=i2c_channel_cfg)
        self.__save_analyser(label, i2c_analyzer)

    def add_spi_analyser(self, SPI_CHANNEL_CFG: dict, PROTOCOL_CFG: dict, label: str) -> None:
        self.__validate_analyser_label(label)
        spi_settings = self.__build_spi_settings(SPI_CHANNEL_CFG, PROTOCOL_CFG)
        spi_analyzer = self.capture.add_analyzer(
            'SPI', label=label, settings=spi_settings)
        self.__save_analyser(label, spi_analyzer)

    def __save_analyser(self, label, analyzer):
        self.__validate_analyser_label(label)
        self.analyzer_dicts[label] = analyzer

    def __build_spi_settings(self, SPI_CHANNEL_CFG, PROTOCOL_CFG):
        CHANNEL = self._build_spi_channel_cfg(SPI_CHANNEL_CFG)
        PROTOCOL = self._build_protocol_cfg(PROTOCOL_CFG)
        spi_settings = {**CHANNEL, **PROTOCOL}
        return spi_settings

    def __validate_analyser_label(self, label):
        if (label in self.analyzer_dicts):
            raise ValueError(
                f"Analysers must have unique labels. Label {label} already used.")

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

    def export_to_csv(self, folder_path: str, file_name: str, analyser_label, radix="HEXADECIMAL") -> None:
        radix = self.__extract_radix(radix)
        path = os.path.join(folder_path, file_name)
        if (not analyser_label in self.analyzer_dicts.keys()):
            raise ValueError(
                f"Analyser {analyser_label} not added. You must first add the analyser with the add_*_analyser methods.")
        ExportConfiguration = automation.capture.DataTableExportConfiguration(
            self.analyzer_dicts[analyser_label], radix)
        self.capture.export_data_table(
            filepath=path,
            analyzers=[ExportConfiguration]
        )

    def __extract_radix(self, radix):
        radix = str.upper(radix)
        if (radix == "HEXADECIMAL"):
            return automation.capture.RadixType.HEXADECIMAL
        elif (radix == "BINARY"):
            return automation.capture.RadixType.BINARY
        elif (radix == "DECIMAL"):
            return automation.capture.RadixType.DECIMAL
        elif (radix == "ASCII"):
            return automation.capture.RadixType.ASCII
        else:
            raise ValueError(
                "Invalid value for radix. Valid values: \"HEXADECIMAL\" \"BINARY\" \"DECIMAL\" \"ASCII\" ")

    def save_raw(self, folder_path: str, file_name: str):
        capture_filepath = os.path.join(folder_path, file_name)
        self.capture.save_capture(filepath=capture_filepath)
