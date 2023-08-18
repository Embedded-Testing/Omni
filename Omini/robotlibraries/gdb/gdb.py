#!/usr/bin/python
# MIT License
#
# Copyright (c) 2023 Erick Setubal Bacurau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
from pygdbmi.gdbcontroller import *
from pygdbmi.constants import *
import json
import re
from .source_utility import *
import os


class GdbResponseError(Exception):
    pass

class GdbConnectionError(Exception):
    pass

class GdbFlashError(Exception):
    pass


def save_as_json(response, file):
    with open(file, "w") as log_file:
        json.dump(response, log_file)
    return


class gdb:

    def __init__(self, gdb_path='/usr/bin/arm-none-eabi-gdb'):
        self.server = ""
        self.connected_to_server = False
        self.elf_loaded = False
        self.working_dir = ""
        self.__is_gdb_installed()
        self.gdb_controller = GdbController(
            command=[gdb_path, '--interpreter=mi3'])
        inital_resp = self.gdb_controller.get_gdb_response()
        self.version = self.__get_version(inital_resp)
        self.get_working_dir()
        response_list = self.gdb_controller.write("-gdb-set mi-async on")
        return

    def get_working_dir(self):
        pattern = r'Working directory (.+).'
        response_list = self.gdb_controller.write("pwd")
        payload_working_dir = response_list[1]['payload']
        match = re.search(pattern, payload_working_dir)
        self.working_dir = match.group(1)

    def __get_version(self, inital_resp) -> str:
        pattern = r'\b\d+\.\d+-\d+\.\d+\b'
        match = re.search(pattern, inital_resp[1]["payload"])
        return match.group(0)

    def pause(self):
        mi_pause_cmd = "-exec-interrupt"
        response_list = self.gdb_controller.write(mi_pause_cmd)
        self.__verify_pause(response_list)

    def __verify_pause(self, response_list):
        r = response_list[2]["payload"]
        if ("received signal SIGINT, Interrupt" in r):
            return
        else:
            raise GdbResponseError

    def __is_gdb_installed(self) -> bool:
        """Check if GDB (GNU Debugger) is installed on the system.

        :raises FileNotFoundError: If the version command fails because the GDB executable is not found.
        :return: True if GDB is installed, False otherwise.
        :rtype: bool
        :Example:
        __is_gdb_installed()
        True
        """
        version_cmd = ["arm-none-eabi-gdb", "--version"]
        try:
            subprocess.check_call(
                version_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
        except subprocess.CalledProcessError:
            raise FileNotFoundError(
                f"Command '{' '.join(version_cmd)}' failed: GDB not found")
        else:
            return True

    def load_elf_file(self, path):
        mi_load_cmd = "-file-exec-and-symbols "+path
        response_list = self.gdb_controller.write(mi_load_cmd)
        self.__verify_load_file_error(response_list)

    def __verify_load_file_error(self, response_list):
        response = response_list[-1]
        if (response["message"] != "error"):
            self.elf_loaded = True
            return
        else:
            self.__raise_load_elf_exceptions(response)
        return

    def __raise_load_elf_exceptions(self, response):
        if (self.__is_not_found_error(response)):
            raise FileNotFoundError(response["payload"]["msg"])
        else:
            raise GdbResponseError(
                'Gdb Response Error. Gdb response: '+json.dumps(response))

    def __is_not_found_error(self, response):
        return "No such file or directory" in response["payload"]["msg"]

    def connect(self, ip, port):
        mi_connect_cmd = "-target-select extended-remote "+ip+":"+port
        try:
            rsp = self.gdb_controller.write(mi_connect_cmd)[-1]
            if (self.__is_connected_in_response(rsp)):
                self.server = self.__get_server_type()
                self.connected_to_server = True
            else:
                raise GdbResponseError(
                    'Gdb Response Error. Gdb response:'+json.dumps(rsp))
        except GdbTimeoutError:
            raise ConnectionError("Timeout connecting to "+ip+":"+port)
        return

    def __is_connected_in_response(self, response):
        if (response["message"] == "connected"):
            return True
        else:
            return False

    def __get_server_type(self):
        response_list = self.gdb_controller.write("monitor version")
        if (self.__is_server_open_ocd(response_list) == True):
            return "Open On-Chip Debugger"
        else:
            response_list = self.gdb_controller.write("monitor help")
            rsp = response_list[1]["payload"]
            if ("SEGGER J-Link GDB Server" in rsp):
                return "SEGGER J-Link GDB Server"

    def __is_server_open_ocd(self, response_list):
        rsp = response_list[1]
        if ("Open On-Chip Debugger" in rsp["payload"]):
            return True
        else:
            return False

    def continue_execution(self):
        self.__verify_server_connection()
        self.__verify_if_elf_loaded()
        response_list = self.__execute_continue_cmd()
        self.__verify_continue_execution(response_list)

    def __execute_continue_cmd(self):
        return self.gdb_controller.write("-exec-continue")

    def __verify_continue_execution(self, response_list):
        rsp = response_list[0]
        if (rsp["type"] != "result" or rsp["message"] != "running"):
            raise GdbResponseError(
                "-exec-continue command failed: malformed response")

    def flash(self):
        self.__verify_server_connection()
        self.__verify_if_elf_loaded()
        response_list = self.gdb_controller.write("-target-download")
        for r in response_list:
            if (("download" in r["payload"]) == False):
                raise GdbResponseError

    def __verify_server_connection(self):
        if (self.connected_to_server == False):
            raise ConnectionError("Not connected to server")

    def __verify_if_elf_loaded(self):
        if (self.elf_loaded == False):
            raise GdbFlashError("Elf File not loaded")

    def reset_halt(self):
        self.__verify_server_connection()
        self.__verify_server_type_for_reset_init()
        response_list = self.gdb_controller.write("monitor reset halt")
        self.__verify_reset_halt(response_list)

    def __verify_server_type_for_reset_init(self):
        if (self.server == "Open On-Chip Debugger"):
            return
        elif (self.server == "SEGGER J-Link GDB Server"):
            raise NotImplementedError(
                "reset init not implemented for SEGGER J-Link GDB Server")
        else:
            raise NotImplementedError(
                "reset init not implemented for" + self.server)

    def __verify_reset_halt(self, response_list):
        for r in response_list:
            if (isinstance(r["payload"], str) and "target halted due to debug-request" in r["payload"]):
                return
        raise GdbResponseError(
            "monitor reset halt command failed: malformed response")

    def get_program_state(self):
        self.__verify_server_connection()
        response_list = self.gdb_controller.write("info program")
        if (self.__is_program_running(response_list)):
            return "running"
        elif (self.__is_program_stopped(response_list)):
            return "stopped"
        else:
            raise GdbResponseError

    def __is_program_running(self, response_list):
        running_msg = response_list[1]["payload"]
        return "Selected thread is running" in running_msg

    def __is_program_stopped(self, response_list):
        stoped_msg = response_list[2]["payload"]
        return "Program stopped" in stoped_msg

    def insert_breakpoint(self, source_file, line_number=-1, break_type="", tag=""):
        line_number = self.__seek_line_number_from_src_file(
            source_file, tag, line_number)
        bp_cmd = self.__build_bp_cmd(source_file, line_number, break_type)
        response_list = self.gdb_controller.write(bp_cmd)
        self.__verify_bp_cmd_response(response_list)
        return

    def __seek_line_number_from_src_file(self, source_file, tag="", line_number=-1):
        if (tag != "" and line_number != -1):
            raise ValueError(
                "Invalid arguments. line_number and tag cannot be defined at the same time")
        elif (tag != "" and line_number == -1):
            return line_of_test_tag(tag, self.working_dir+'/'+source_file)
        elif (tag == "" and line_number != -1):
            return line_number
        else:
            raise ValueError(
                "Invalid arguments. line_number or tag must be defined")

    def __verify_bp_cmd_response(self, response_list):
        if (len(response_list) == 2):
            result_msg = response_list[1]
        elif ((len(response_list) == 1)):
            result_msg = response_list[0]
            self.__verify_result_msg(result_msg)
            raise GdbResponseError("malformed result_msg")
        else:
            raise GdbResponseError("malformed response from gdb")

    def __verify_result_msg(self, result_msg):
        if ("error" in result_msg["message"]):
            payload_error_msg = result_msg["payload"]["msg"]
            if ("No line" in payload_error_msg or "No source file named" in payload_error_msg):
                raise GdbResponseError(result_msg["payload"]["msg"])
        else:
            return

    def __build_bp_cmd(self, source_file, line_number, break_type):
        break_type_flag = self.__map_breakpoint_flag(break_type)
        bp_cmd = f"-break-insert --source {source_file} --line {line_number} {break_type_flag}"
        return bp_cmd.rstrip()

    def __map_breakpoint_flag(self, break_type):
        breakpoint_flags_map = {"hardware": "-h", "temporary": "-t", "": ""}
        if (break_type not in breakpoint_flags_map):
            raise ValueError(
                "Invalid break_type argument. Valid types: hardware, temporary and \"\".")
        return breakpoint_flags_map[break_type]

    def change_working_dir(self, directory):
        response_list = self.gdb_controller.write("cd "+directory)
        self.__verify_cd_response(response_list)
        self.working_dir = directory
        return

    def __verify_cd_response(self, response_list):
        if ("Working directory" in response_list[1]["payload"]):
            return
        elif (response_list[2]["message"] == "error" and
              "No such file or directory" in response_list[2]["payload"]["msg"]):
            raise FileNotFoundError(response_list[2]["payload"]["msg"])
        else:
            raise GdbResponseError("malformed response from gdb")

    def continue_until_breakpoint(self, timeout_sec=1):
        self.__verify_server_connection()
        response_cont_cmd = self.__execute_continue_cmd()
        if (self.__breakpoint_hit(response_cont_cmd) == True):
            return
        else:
            response_read = self.gdb_controller.get_gdb_response(
                timeout_sec, True)
            if (self.__breakpoint_hit(response_read) == True):
                return
            else:
                raise GdbResponseError("malformed response from gdb")

    def __breakpoint_hit(self, response):
        for entry in response:
            if (entry["type"] == "notify" and entry["message"] == "stopped" and entry["payload"]["reason"] == "breakpoint-hit"):
                return True
        return False

    def stopped_at_breakpoint_with_tag(self, source_file, tag):
        info_program_rsp_list = self.gdb_controller.write("info program")
        self.__verify_stopped_at_breakpoint_st(info_program_rsp_list)
        bp_index = self.__seek_breakpoint_index(info_program_rsp_list)
        resp_break_list = self.gdb_controller.write("-break-list")
        bp_entry = self.__get_breakpoint_entry(bp_index, resp_break_list)
        filename = self.__get_bp_file_name(bp_entry)
        line_number = self.__get_breakpoint_line(bp_entry)
        line = line_of_test_tag(tag, self.working_dir+'/'+source_file)
        if (line == line_number and filename == source_file):
            return True
        else:
            return False

    def __get_breakpoint_entry(self, bp_index, response_list):
        bp_entries = response_list[0]["payload"]["BreakpointTable"]["body"]
        for e in bp_entries:
            if e["number"] == bp_index:
                return e
        raise GdbResponseError(
            "Invalid breakpoint index"+bp_index+"in breakpoints list")

    def __get_breakpoint_line(self, bp_entry):
        return int(bp_entry["line"])

    def __get_bp_file_name(self, bp_entry):
        full_path = bp_entry["fullname"]
        return os.path.basename(full_path)

    def __seek_breakpoint_index(self, response_list):
        stoped_at_bp_payload = response_list[3]["payload"]
        match = re.search(r"breakpoint (\d+)", stoped_at_bp_payload)
        breakpoint_index = match.group(1)
        return breakpoint_index

    def __verify_stopped_at_breakpoint_st(self, response_list):
        if (self.__get_program_running_state(response_list) != "Stopped at breakpoint"):
            raise GdbResponseError("Program is not stopped at breakpoint")

    def __get_program_running_state(self, response_list):
        if (len(response_list) == 3 and "Selected thread is running" in response_list[1]["payload"]):
            return "Running"
        elif (len(response_list) == 6 and "Program stopped at" in response_list[2]["payload"]):
            if ("It stopped at breakpoint" in response_list[3]["payload"]):
                return "Stopped at breakpoint"
            else:
                return "Stopped"
        else:
            raise GdbResponseError("malformed message")

    def delete_all_breakpoints(self):
        del_breakpoints_rsp_list = self.gdb_controller.write("-break-delete")
        return self.__verify_done_response_bp(del_breakpoints_rsp_list)

    def __verify_done_response_bp(self, rsp_list):
        if ("done" in rsp_list[0]["message"]):
            return
        else:
            raise GdbResponseError("Malformed response from -break-delete")

    def next(self):
        next_rsp_list = self.gdb_controller.write("-exec-next")
        return self.__verify_next_response(next_rsp_list)

    def __verify_next_response(self, next_rsp_list):
        for entry in next_rsp_list:
            if ("notify" in entry["type"] and "stopped" in entry["message"]):
                if ("end-stepping-range" in entry["payload"]["reason"]):
                    return
        raise GdbResponseError("Malformed response from -exec-next")

    def __extract_object_string(self, var_response_list):
        payload = var_response_list[1]["payload"]
        match = re.search(r"=\s(.*)\n", payload)
        if (match == None):
            raise GdbResponseError(
                "Malformated value for payload. Got '{}'".format(payload))
        return match.group(1)

    def __verify_format(self, format):
        if (format != "dec" and format != "hex" and format != "bin"):
            raise ValueError(
                "Invalid value for 'format' parameter. Expected values: 'dec', 'hex', or 'bin'. Got: '{}'".format(format))

    def ___extract_type(self, format):
        if (format == "dec"):
            return '/d'
        elif (format == "hex"):
            return '/x'
        elif (format == "bin"):
            return '/t'
        else:
            raise ValueError(
                "Invalid value for 'format' parameter. ___extract_type wrongly used")

    def get_variable_value(self, variable_name, format):
        return self.get_object_value(variable_name, format)

    def get_object_value(self, object_name, format):
        self.__verify_format(format)
        print_type = self.___extract_type(format)
        var_response_list = self.gdb_controller.write(
            "print "+print_type+" "+object_name)
        object_string = self.__extract_object_string(var_response_list)
        return object_string

    def send_command(self, command, response_file):
        response_list = self.gdb_controller.write(command)
        save_as_json(response_list, response_file)

    def set_log_file_path(self, log_file_path):
        response_list = self.gdb_controller.write(
            "-gdb-set logging file "+log_file_path)
        self.__verify_set_log_file_rsp(response_list)

    def __verify_set_log_file_rsp(self, response_list):
        if (self.__is_response_valid(response_list)):
            return
        elif (self.__is_msg_in_payload(response_list)):
            raise GdbResponseError(
                "Error on set_log_file_path message from gdb: "+response_list[0]["payload"]["msg"])
        else:
            raise GdbResponseError("Malformed message from GDB")

    def start_logging(self):
        response_list = self.gdb_controller.write("--gdb-set logging on")
        if (self.__is_response_valid(response_list)):
            return
        elif (self.__is_msg_in_payload(response_list)):
            raise GdbResponseError(
                "Error on start_logging message from gdb: "+response_list[0]["payload"]["msg"])
        else:
            raise GdbResponseError(
                "Malformed message from GDB on start_logging")

    def stop_logging(self):
        response_list = self.gdb_controller.write("--gdb-set logging off")
        if (self.__is_response_valid(response_list)):
            return
        elif (self.__is_msg_in_payload(response_list)):
            raise GdbResponseError(
                "Error on start_logging message from gdb: "+response_list[0]["payload"]["msg"])
        else:
            raise GdbResponseError(
                "Malformed message from GDB on stop_logging")

    def __is_msg_in_payload(self, response_list):
        return "msg" in response_list[0]["payload"]

    def __is_response_valid(self, response_list):
        return response_list[0]["type"] == "result" and response_list[0]["message"] == "done"

    def __del__(self):
        return
