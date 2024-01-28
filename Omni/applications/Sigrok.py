import multiprocessing
from Omni.applications.Sigrok_backend import sigrok_process
import Omni.process_manager.process_manager as process_manager
import Omni.process_manager.network_lib as network
import Omni.process_manager.exceptions as process_exceptions
import os
from datetime import datetime

sigrok_process_entry = {
    "application": "Sigrok process",
    "pid": 'not defined',
    "log_file": 'not defined',
    "process_call": "multiprocessing in launch_sigrok_process_host in Sigrok_process.py",
    "start_time": 'not defined',
    "port": 'not defined',
    "pgrep_string": "Sigrok_process",
}


def launch_sigrok_process_host(port, process_file, log_file):
    process_manager.verify_file(process_file)
    _verify_port(port)
    sigrok_host_process = _start_sigrok_process(port, log_file)
    print("Sigrok Server started...")
    print("Server started with PID:", sigrok_host_process.pid)
    sigrok_process_entry["pid"] = sigrok_host_process.pid
    sigrok_process_entry["log_file"] = str(log_file)
    sigrok_process_entry["port"] = port
    process_manager.append_process_data_to_file(
        sigrok_process_entry, process_file)
    os._exit(0)


def _start_sigrok_process(port, log_file):
    sigrok_host_process = multiprocessing.Process(
        target=sigrok_process, args=(port, log_file))
    sigrok_host_process.daemon = False
    sigrok_host_process.start()
    return sigrok_host_process


def _verify_port(port):
    if (network.is_port_free(port) == False):
        process_id = network.get_process_listening_on_port(port)
        raise process_exceptions.PortBusyError(
            port, process_id)


def verify_sigrok_process(port):
    if (network.is_port_listening(port)):
        pass
    else:
        raise process_exceptions.ProcessStartupError(
            "Sigrok process did not started propperly ")
