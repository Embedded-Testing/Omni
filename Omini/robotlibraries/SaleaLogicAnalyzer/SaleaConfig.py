
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
