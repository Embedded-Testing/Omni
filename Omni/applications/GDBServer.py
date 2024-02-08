import subprocess
import Omni.process_manager.process_manager as process_manager
from datetime import datetime


def launch_gdbserver(process_file:str, gdbserver_log_file: str, gdbserver_path:str, jlink_interface:str, board_interface_type:str, port:str, device:str, extra_parameters:str='')->None:
    process_manager.verify_file(process_file)
    gdbserver_launch_cmd = __build_gdbserver_cmd(gdbserver_path, jlink_interface, board_interface_type, port, device, extra_parameters)
    with open(gdbserver_log_file, 'w') as gdbserver_log_fd:
        process = subprocess.Popen(
            gdbserver_launch_cmd, stdout=gdbserver_log_fd, stderr=gdbserver_log_fd)
        gdbserver_pid = str(process.pid)
        gdb_server_process_entry = __build_gdbserver_entry(gdbserver_log_file, port, gdbserver_launch_cmd, gdbserver_pid)
        process_manager.append_process_data_to_file(
            gdb_server_process_entry, process_file)
        process_manager.pretty_print_json(gdb_server_process_entry)

def __build_gdbserver_entry(gdbserver_log_file, port, gdbserver_launch_cmd, gdbserver_pid):
    current_time = datetime.now().strftime("%H:%M:%S")
    gdb_server_process_entry = {
        "application": "JLinkGDBServerCL",
        "pid": gdbserver_pid,
        "log_file": str(gdbserver_log_file),
        "process_call": " ".join(gdbserver_launch_cmd),
        "start_time": current_time,
        "port": port,
        "pgrep_string": "JLinkGDBServerCL",
    }
    return gdb_server_process_entry

def __build_gdbserver_cmd(gdbserver_path, jlink_interface, board_interface_type, port, device, extra_parameters):
    gdbserver_launch_cmd = [gdbserver_path, '-select',
                            jlink_interface, '-device',device, '-if',board_interface_type, '-port',port]
    gdbserver_launch_cmd += extra_parameters.split()
    return gdbserver_launch_cmd
