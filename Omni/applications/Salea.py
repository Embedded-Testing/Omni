import subprocess
import argparse
import time
import Omni.process_manager.process_manager as process_manager
from datetime import datetime
import re

global salea_jobpid
global salea_launch_command


class ProcessStartupError(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        error_message = super().__str__()
        if self.error_code is not None:
            return f"{error_message}"
        return error_message


def launch_salea(salea_app_path, log_file_path, port, process_file, headless=False):
    process_manager.verify_file(process_file)
    salea_launch_command = str(salea_app_path)+" " + \
        "--automation --automationPort "+str(port)
    if (headless):
        salea_launch_command = "xvfb-run " + salea_launch_command
    salea_log_fd = open(log_file_path, 'w')
    process = subprocess.Popen(
        salea_launch_command.split(), stdout=salea_log_fd, stderr=salea_log_fd)
    salea_jobpid = str(process.pid)
    current_time = datetime.now().strftime("%H:%M:%S")
    salea_process_entry = {
        "application": "Salea Logic Analyser",
        "pid": salea_jobpid,
        "log_file": log_file_path,
        "process_call": salea_launch_command,
        "start_time": current_time,
        "port": port,
        "pgrep_string": "Logic",
    }
    process_manager.append_process_data_to_file(
        salea_process_entry, process_file)
    process_manager.pretty_print_json(salea_process_entry)
    return


def close_salea_application():
    pgrep_command = ["pgrep", "Logic"]
    logic_pids = subprocess.check_output(pgrep_command).decode().splitlines()
    print(logic_pids)
    for pid in logic_pids:
        kill_command = ["kill", pid]
        subprocess.run(kill_command)


def verify_salea_startup(log_file_path, wait_time=5):
    pattern = "logic_device_node.*set.led"
    file_contents_try1 = read_log(log_file_path)
    found_try1 = re.search(pattern, file_contents_try1)
    if (found_try1 == None):
        time.sleep(wait_time)
    file_contents_try2 = read_log(log_file_path)
    found_try2 = re.search(pattern, file_contents_try2)
    if (found_try2 == None):
        raise ProcessStartupError(
            "Salea Process did not started propperly within "+str(wait_time)+"s")
    else:
        return


def read_log(log_file_path):
    with open(log_file_path, 'r') as log:
        file_contents = log.read()
    return file_contents


# Call from folder: embedded-integration-test-framework
# Example Call: python3 -m Omni.applications.Launch_Salea --path /usr/local/bin/Logic --log ./.Transfer_Area/SaleaLog.txt --port 10430 --proc ./.Process_Info/CmdlineSalea.json
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str,
                        help='Path to the Salea Application')
    parser.add_argument('--log', type=str,
                        help='Path to file where the Salea log will be saved')
    parser.add_argument(
        '--port', type=str, help='Port that will be exposed by the salea application')
    parser.add_argument(
        '--proc', type=str, help='Path to file where process information will be saved')

    args = parser.parse_args()
    process_manager.create_config_file(args.proc)
    launch_salea(args.path, args.log, args.port, args.proc)
    time.sleep(30)
    close_salea_application()
