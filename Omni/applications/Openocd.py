import subprocess
import argparse
import time
from datetime import datetime
import Omni.process_manager.process_manager as process_manager
import re


class ProcessStartupError(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        error_message = super().__str__()
        if self.error_code is not None:
            return f"{error_message}"
        return error_message


def launch_openocd(process_file, openocd_path, board_cfg_file_path, interface_cfg_file_path, open_ocd_log_path):
    process_manager.verify_file(process_file)
    openocd_log_fd = open(open_ocd_log_path, 'w')
    open_ocd_launch = [openocd_path, "-f",
                       board_cfg_file_path, "-f", interface_cfg_file_path]
    process = subprocess.Popen(
        open_ocd_launch, stdout=openocd_log_fd, stderr=openocd_log_fd)
    openocd_jobpid = str(process.pid)
    current_time = datetime.now().strftime("%H:%M:%S")
    open_ocd_process_entry = {
        "application": "Open OCD",
        "pid": openocd_jobpid,
        "log_file": open_ocd_log_path,
        "process_call": " ".join(open_ocd_launch),
        "start_time": current_time,
        "port": 3333,
        "pgrep_string": "openocd",
    }
    process_manager.append_process_data_to_file(
        open_ocd_process_entry, process_file)
    process_manager.pretty_print_json(open_ocd_process_entry)


def verify_openocd(open_ocd_log_path, wait_time=5):
    pattern = "Listening on port \\d* for gdb connections"
    file_contents_try1 = read_log(open_ocd_log_path)
    found_try1 = re.search(pattern, file_contents_try1)
    if (found_try1 == None):
        time.sleep(wait_time)
    file_contents_try2 = read_log(open_ocd_log_path)
    found_try2 = re.search(pattern, file_contents_try2)
    if (found_try2 == None):
        raise ProcessStartupError(
            "Openocd process did not started propperly ")
    else:
        return


def read_log(log_file_path):
    with open(log_file_path, 'r') as log:
        file_contents = log.read()
    return file_contents


# Call from folder: embedded-integration-test-framework
# Example Call: python3 -m Omni.applications.Openocd --path /usr/bin/openocd --log ./.Transfer_Area/OpenOcdLog.txt --board /usr/share/openocd/scripts/board/stm32f4discovery.cfg --interface /usr/share/openocd/scripts/interface/stlink-v2.cfg --proc ./.Process_Info/CmdlineOpenOcd.txt
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str,
                        help='Path to the Openocd Application')
    parser.add_argument('--log', type=str,
                        help='Path to file where the Salea log will be saved')
    parser.add_argument(
        '--board', type=str, help='Port that will be exposed by the salea application')
    parser.add_argument('--interface', type=str,
                        help='Path to file where process information will be saved')
    parser.add_argument(
        '--proc', type=str, help='Path to file where process information will be saved')

    args = parser.parse_args()
    process_manager.create_config_file(args.proc)
    launch_openocd(args.proc, args.path, args.board, args.interface, args.log)
    time.sleep(10)
