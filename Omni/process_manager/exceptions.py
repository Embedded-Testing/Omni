class ProcessStartupError(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        error_message = super().__str__()
        if self.error_code is not None:
            return f"{error_message}"
        return error_message


class ProcessStartupError(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        error_message = super().__str__()
        if self.error_code is not None:
            return f"{error_message}"
        return error_message


class PortBusyError(Exception):
    def __init__(self, port_number, process_id):
        super().__init__(
            f"Port {port_number} is busy with process id {process_id}")
        self.port_number = port_number
        self.process_id = process_id

    def __str__(self):
        # Format the custom error message with port number and process ID
        return f"Port {self.port_number} is in use by process with id {self.process_id}."
