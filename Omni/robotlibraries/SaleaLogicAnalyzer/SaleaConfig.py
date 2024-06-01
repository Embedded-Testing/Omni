from . import SaleaLogicAnalyzer


def config_uart_channel(Channel: int, BitRate: int, BitsPerFrame: int, StopBits: float,
                        Parity: str, Indianess: str, Inversion: bool, AddressMode: str) -> dict:
    __verify_bitrate(BitRate)
    return {"Input Channel": Channel,
            "Bit Rate (Bits/s)": __build_bit_rate(BitRate),
            "Bits per Frame": __build_bits_per_frame_string(BitsPerFrame),
            "Stop Bits": __build_stop_bit_string(StopBits),
            "Parity Bit": __build_parity_string(Parity),
            "Significant Bit": __build_significant_bit_str(Indianess),
            "Signal inversion": __build_inversion_str(Inversion),
            "Mode": __build_mode_string(AddressMode)}


def __build_bit_rate(BitRate: int) -> int:
    __verify_bitrate(BitRate)
    return BitRate


def __verify_bitrate(BitRate: int) -> None:
    if (BitRate <= 0):
        raise ValueError(
            "Invalid value for BitRate. Value must be positive.")


def __build_bits_per_frame_string(BitsPerFrame: int) -> str:
    __verify_bits_per_frame(BitsPerFrame)
    v = str(BitsPerFrame)+" Bits per Transfer"
    if (BitsPerFrame == 8):
        v += " (Standard)"
    return v


def __verify_bits_per_frame(BitsPerFrame: int) -> None:
    if (BitsPerFrame <= 0 or BitsPerFrame > 64):
        raise ValueError(
            "Invalid value for Bits Per Frame. Value must be positive and less than 65.")


def __build_stop_bit_string(StopBits: float) -> str:
    if (StopBits == 1):
        v = "1 Stop Bit (Standard)"
    else:
        v = str(StopBits)+" Stop Bits"
    return v


def __build_parity_string(Parity: str) -> str:
    if (Parity == "None"):
        v = "No Parity Bit (Standard)"
    elif (Parity == "Even"):
        v = "Even Parity Bit"
    elif (Parity == "Odd"):
        v = "Odd Parity Bit"
    else:
        raise ValueError(
            "Invalid value for Parity. Valied values are: None,Odd and Even.")
    return v


def __build_significant_bit_str(Indianess) -> str:
    if (Indianess == "LSB"):
        return "Least Significant Bit Sent First (Standard)"
    elif (Indianess == "MSB"):
        return "Most Significant Bit Sent First"
    else:
        raise ValueError(
            "Invalid value for Indianess. Valied values are: MSB or LSB.")


def __build_inversion_str(Inversion: bool):
    if (Inversion == True):
        return "Inverted"
    else:
        return "Non Inverted (Standard)"


def __build_mode_string(AddressMode: str) -> str:
    if (AddressMode == "Normal"):
        return "Normal"
    elif (AddressMode == "MP"):
        return "MP - Address indicated by MSB=0"
    elif (AddressMode == "MDB"):
        return "MDB - Address indicated by MSB=1 (TX only)"
    else:
        raise ValueError(
            "Invalid value for AddressMode. Valied values are: Normal or MP or MDB.")


def config_i2c_channels(SCL: int, SDA: int) -> dict:
    i2c_channels_dict = {}
    i2c_channels_dict["SCL"] = int(SCL)
    i2c_channels_dict["SDA"] = int(SDA)
    return i2c_channels_dict


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
        raise SaleaLogicAnalyzer.SaleaConfigurationError(__form_not_valid_msg(
            "EnableLineActive", EnableLineActiveOn, ['0', '1']))


def __extract_phase(CPHA: str, protocol_dict: dict):
    if (CPHA == '0' or CPHA == '1'):
        protocol_dict["CPHA"] = str(CPHA)
    else:
        raise SaleaLogicAnalyzer.SaleaConfigurationError(
            __form_not_valid_msg("CPHA", CPHA, ['0', '1']))


def __extract_polarity(CPOL: str, protocol_dict: dict):
    if (CPOL == '0' or CPOL == '1'):
        protocol_dict["CPOL"] = str(CPOL)
    else:
        raise SaleaLogicAnalyzer.SaleaConfigurationError(
            __form_not_valid_msg("CPOL", CPOL, ['0', '1']))


def __extract_first_bit_type(FIRST_BIT: str, protocol_dict: dict):
    if (FIRST_BIT == 'MSB' or FIRST_BIT == 'LSB'):
        protocol_dict["FIRST_BIT"] = str(FIRST_BIT)
    else:
        raise SaleaLogicAnalyzer.SaleaConfigurationError(
            __form_not_valid_msg("FIRST_BIT", FIRST_BIT, ['MSB', 'LSB']))


def __extract_frame_size(DATA_FRAME_SIZE: str, protocol_dict: dict):
    if (DATA_FRAME_SIZE == '8' or DATA_FRAME_SIZE == '16'):
        protocol_dict["DATA_FRAME_SIZE"] = str(DATA_FRAME_SIZE)
    else:
        raise SaleaLogicAnalyzer.SaleaConfigurationError(__form_not_valid_msg(
            "DATA_FRAME_SIZE", DATA_FRAME_SIZE, ['8', '16']))


def __form_not_valid_msg(parameter, val, valid_values: list):
    valid_values_str = ', '.join(map(str, valid_values))
    exception_msg = (
        f"Invalid value for '{parameter}'. "
        f"Provided value: '{val}'. Valid values are: {valid_values_str}."
    )
    return exception_msg
