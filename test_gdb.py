import unittest
from unittest.mock import patch, MagicMock
import subprocess
from .robotlibraries.gdb.gdb import *
from pygdbmi.gdbcontroller import *
from pygdbmi.constants import *
import json
import os



def read_from_json(file):
    with open(file, 'r') as input_data_file:
        data = json.load(input_data_file)
    return data


def gdb_write_responses(param):
    if "-gdb-set mi-async on" in param:
        return read_from_json("./robotlibraries/gdb/gdb_responses/mi_assync_on_cmd.json")
    if "pwd" in param:
        return read_from_json("./robotlibraries/gdb/gdb_responses/pwd.json")
    else:
        raise Exception("ERROR IN STUB")

def compare_files(file1_path, file2_path):
    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_contents = file1.read()
            file2_contents = file2.read()

            if file1_contents == file2_contents:
                return True
            else:
                return False
    except OSError as e:
        print(f"Error occurred while comparing files: {e}")


class TestGdbCtor(unittest.TestCase):

    @patch('subprocess.check_call', side_effect=subprocess.CalledProcessError(
        1, "arm-none-eabi-gdb", "Command 'arm-none-eabi-gdb --version' failed"))
    def test_gdb_not_installed_raise_exception(self, mock_check_call):
        with self.assertRaises(FileNotFoundError):
            gdb()

    @patch('pygdbmi.gdbcontroller.GdbController.get_gdb_response',
           return_value=read_from_json("./robotlibraries/gdb/gdb_responses/initial_resp.json"))
    @patch('pygdbmi.gdbcontroller.GdbController.write', side_effect=gdb_write_responses)
    def test_gdb_saves_version(self, mock_gdb_read, mock_gdb_write):
        my_instance = gdb()
        self.assertEqual(my_instance.version, "10.3-2021.10")
        return

    @patch('pygdbmi.gdbcontroller.GdbController.write', side_effect=gdb_write_responses)
    def test_gdb_sets_mi_async_on(self, mock_gdb_write):
        gdb()
        mock_gdb_write.assert_called_with('-gdb-set mi-async on')
        return

    @patch('pygdbmi.gdbcontroller.GdbController.get_gdb_response', return_value=read_from_json(
        "./robotlibraries/gdb/gdb_responses/initial_resp.json"))
    @patch('pygdbmi.gdbcontroller.GdbController.write', side_effect=gdb_write_responses)
    def test_gdb_saves_working_dir(self, mock_gdb_write, mock_gdb_get_resp):
        my_instance = gdb()
        self.assertEqual(my_instance.working_dir, "/home/erick/Desktop/EITF")
        return


class TestGdb(unittest.TestCase):

    def gdb_responses_open_ocd(self, param):
        if "-target-select extended-remote" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_connect_cmd.json")
        elif "monitor version" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/monitor_version_openocd.json")
        elif "-file-exec-and-symbols" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_load_cmd_found.json")
        elif "-exec-continue" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue.json")
        elif "-target-download" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_load_open_ocd.json")
        elif "monitor reset halt" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_monitor_reset_halt_openocd.json")
        elif "-exec-interrupt" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_exec_interrupt.json")
        elif "info program" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/info_program_running.json")
        elif "-break-insert" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_break_insert.json")
        elif "cd" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/cd_dir.json")
        elif "-break-delete" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_bp_del_all.json")
        else:
            raise Exception("ERROR IN STUB")

    def gdb_bp(self, param):
        if "info program" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/info_prog_stoped_bp.json")
        elif "-break-list" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_bp_list.json")
        elif "-exec-next" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/next_rsp1.json")
        elif "print /d my_var" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/print_var_dec.json")
        elif "print /x my_var" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/print_var_hex.json")
        elif "print /x my_bad_payload_var" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/print_var_bad_payload.json")
        elif "print /t my_var" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/print_var_bin.json")
        elif "print /x non_existent_var" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/print_var_symbol_n_found.json")
        elif "print /x no_exist_struct" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/print_struct_bad2.json")
        elif "print /x my_struct" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/print_struct_hex.json")
        else:
            raise Exception("ERROR IN STUB")

    def gdb_bp_2(self, param):
        if "info program" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/info_prog_stoped_bp2.json")
        elif "-break-list" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_bp_list2.json")
        else:
            raise Exception("ERROR IN STUB")

    def gdb_bp_3(self, param):
        if "info program" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/info_prog_stoped_bp3.json")
        elif "-break-list" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_bp_list.json")
        else:
            raise Exception("ERROR IN STUB")

    @patch('subprocess.check_call')
    def setUp(self, subprocess_check_call_mock):
        subprocess_check_call_mock.return_value = None
        self.instance = gdb()
        self.mock_gdb_controller = MagicMock()
        self.instance.gdb_controller = self.mock_gdb_controller

    def test_gdb_loads_elf(self):
        self.mock_gdb_controller.write.return_value = read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_load_cmd_found.json")
        path = "/path/to/elf/file"
        self.instance.load_elf_file(path)
        self.mock_gdb_controller.write.assert_called_once_with(
            "-file-exec-and-symbols "+path)

    def test_gdb_loads_elf_not_found(self):
        self.mock_gdb_controller.write.return_value = read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_load_cmd_not_found.json")
        path = "/path/to/elf/file"
        with self.assertRaises(FileNotFoundError):
            self.instance.load_elf_file(path)

    def test_gdb_loads_error_msg(self):
        self.mock_gdb_controller.write.return_value = read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_load_cmd_generic_error.json")
        path = "/path/to/elf/file"
        with self.assertRaises(GdbResponseError):
            self.instance.load_elf_file(path)

    def test_gdb_connect_correct_call(self):
        self.mock_gdb_controller.write.return_value = read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_connect_cmd.json")
        self.instance.connect("localhost", "3333")
        self.mock_gdb_controller.write.assert_any_call(
            "-target-select extended-remote localhost:3333")
        return

    def test_gdb_connect_malformed_msg(self):
        self.mock_gdb_controller.write.return_value = read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_connect_cmd_generic_error.json")
        with self.assertRaises(GdbResponseError):
            self.instance.connect("localhost", "3333")

    def test_gdb_connect_identifies_openocd_stub(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.assertEqual(self.instance.server, "Open On-Chip Debugger")

    def gdbserver_responses_gdbserver(self, param):
        if "-target-select extended-remote" in param:
            return read_from_json("./robotlibraries/gdb/gdb_responses/mi_connect_cmd.json")
        elif param == 'monitor version':
            return read_from_json("./robotlibraries/gdb/gdb_responses/monitor_version_gdbserver.json")
        elif param == 'monitor help':
            return read_from_json("./robotlibraries/gdb/gdb_responses/monitor_help_gdbserver.json")
        else:
            raise Exception("ERROR IN STUB")

    def test_gdb_connect_identifies_jlink_gdbserver_stub(self):
        self.mock_gdb_controller.write.side_effect = self.gdbserver_responses_gdbserver
        self.instance.connect("localhost", "3333")
        self.assertEqual(self.instance.server, "SEGGER J-Link GDB Server")

    def test_gdb_connect_error(self):
        self.mock_gdb_controller.write.side_effect = GdbTimeoutError(
            ValueError)
        with self.assertRaises(ConnectionError):
            self.instance.connect("localhost", "3334")

    def test_gdb_flash(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()

    def test_gdb_flash_raises_exception_if_not_connected(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.load_elf_file("/path/to/elf/file")
        with self.assertRaises(ConnectionError):
            self.instance.flash()

    def test_gdb_flash_raises_exception_if_elf_not_loaded(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        with self.assertRaises(GdbFlashError):
            self.instance.flash()

    def test_gdb_flash_raise_exception_malformed_resp(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_load_open_ocd_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.flash()

    def test_gdb_continue_raise_exception_if_not_connected(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.load_elf_file("/path/to/elf/file")
        with self.assertRaises(ConnectionError):
            self.instance.continue_execution()

    def test_gdb_continue_raise_exception_if_not_loaded(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        with self.assertRaises(GdbFlashError):
            self.instance.continue_execution()
        return

    def test_gdb_continue_correct_call(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.continue_execution()
        self.mock_gdb_controller.write.assert_any_call("-exec-continue")
        return

    def test_gdb_continue_malformed_resp(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.continue_execution()
        return

    def test_gdb_monitor_reset_halt_openocd(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.reset_halt()
        self.mock_gdb_controller.write.assert_any_call("monitor reset halt")
        return

    def test_gdb_monitor_reset_halt_gdbserver_raises_exception(self):
        self.mock_gdb_controller.write.side_effect = self.gdbserver_responses_gdbserver
        self.instance.connect("localhost", "3333")
        with self.assertRaises(NotImplementedError):
            self.instance.reset_halt()
        return

    def test_gdb_monitor_reset_halt_raise_exception_if_not_connected(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        with self.assertRaises(ConnectionError):
            self.instance.reset_halt()
        return

    def test_gdb_monitor_reset_halt_raise_exception_if_malformed_resp(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_monitor_reset_halt_openocd_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.reset_halt()
        return

    def test_gdb_pause_correct_call(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.continue_execution()
        self.instance.pause()
        self.mock_gdb_controller.write.assert_any_call("-exec-interrupt")
        return

    def test_gdb_pause_malformed_resp(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.continue_execution()
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_monitor_reset_halt_openocd_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.pause()
        return

    def test_gdb_info_program_running(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.continue_execution()
        self.assertEqual(self.instance.get_program_state(), "running")
        return

    def test_gdb_info_program_stopped(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.continue_execution()
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/info_program_stopped.json")]
        self.assertEqual(self.instance.get_program_state(), "stopped")
        return

    def test_gdb_info_program_malformed_resp(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.continue_execution()
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/info_program_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.get_program_state()
        return

    def test_gdb_info_program_not_connected_raises_exception(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        with self.assertRaises(ConnectionError):
            self.instance.get_program_state()
        return

    def test_gdb_set_breakpoint(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", 20)
        self.mock_gdb_controller.write.assert_any_call(
            "-break-insert --source MySourceFile.cpp --line 20")
        self.instance.insert_breakpoint("MySourceFile.cpp", 21)
        self.mock_gdb_controller.write.assert_any_call(
            "-break-insert --source MySourceFile.cpp --line 21")
        self.instance.insert_breakpoint("MySourceFileA.cpp", 20)
        self.mock_gdb_controller.write.assert_any_call(
            "-break-insert --source MySourceFileA.cpp --line 20")
        return

    def test_gdb_set_breakpoint_with_tag(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.working_dir = "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses"
        self.instance.insert_breakpoint(
            "MySourceFile.cpp", tag="TEST TAG A")
        self.instance.insert_breakpoint(
            "MySourceFile.cpp", tag="TEST TAG B")
        self.mock_gdb_controller.write.assert_any_call(
            "-break-insert --source MySourceFile.cpp --line 16")
        self.mock_gdb_controller.write.assert_any_call(
            "-break-insert --source MySourceFile.cpp --line 18")
        return

    def test_gdb_set_breakpoint_with_tag_src_not_found(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.working_dir = "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses"
        with self.assertRaises(FileNotFoundError):
            self.instance.insert_breakpoint(
                "NotExistingFile.cpp", tag="TEST TAG A")
        return

    def test_gdb_set_breakpoint_tag_not_found(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.working_dir = "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses"
        with self.assertRaises(TagNotFoundError):
            self.instance.insert_breakpoint(
                "MySourceFile.cpp", tag="Non Existing Tag")
        return

    def test_gdb_set_breakpoint_raises_exception_if_tag_and_line_are_set(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.working_dir = "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses"
        with self.assertRaises(ValueError):
            self.instance.insert_breakpoint(
                "MySourceFile.cpp", 3, tag="TEST TAG A")
        return

    def test_gdb_set_breakpoint_raises_exception_if_tag_and_line_are_not_set(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.working_dir = "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses"
        with self.assertRaises(ValueError):
            self.instance.insert_breakpoint(
                "MySourceFile.cpp")
        return

    def test_gdb_set_breakpoint_raises_exception_if_tag_found_twice_or_more(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.working_dir = "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses"
        with self.assertRaises(TagError):
            self.instance.insert_breakpoint(
                "MyBadSourceFile.cpp", tag="TEST TAG A")
        return

    def test_gdb_set_breakpoint_bad_source_file_raise_exception(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_break_insert_wrong_file.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.insert_breakpoint("WrongFileName", 20)
        return

    def test_gdb_set_breakpoint_bad_lineNumber_raise_exception(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_break_insert_bad_line.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.insert_breakpoint("MySourceFileA.cpp", 500)
        return

    def test_gdb_set_breakpoint_malformed_result_msg_raise_exception(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_break_insert_malformed_rsp.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.insert_breakpoint("MySourceFileA.cpp", 500)
        return

    def test_gdb_set_breakpoint_malformed_gdb_response_raise_exception(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_break_insert_malformed_gdb_rsp.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.insert_breakpoint("MySourceFileA.cpp", 20)
        return

    def test_gdb_set_breakpoint_hw(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.insert_breakpoint(
            "MySourceFileA.cpp", 20, break_type="hardware")
        self.mock_gdb_controller.write.assert_any_call(
            "-break-insert --source MySourceFileA.cpp --line 20 -h")
        return

    def test_gdb_set_breakpoint_temp(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.insert_breakpoint(
            "MySourceFileA.cpp", 20, break_type="temporary")
        self.mock_gdb_controller.write.assert_any_call(
            "-break-insert --source MySourceFileA.cpp --line 20 -t")
        return

    def test_gdb_set_breakpoint_invalid_type(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        with self.assertRaises(ValueError):
            self.instance.insert_breakpoint(
                "MySourceFileA.cpp", 20, break_type="InvalidType")
        return

    def test_gdb_change_directory_changes_working_dir(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.change_working_dir("/a/test/working/dir")
        self.mock_gdb_controller.write.assert_called_once_with(
            "cd "+"/a/test/working/dir")
        self.assertEqual(self.instance.working_dir, "/a/test/working/dir")
        return

    def test_gdb_change_directory_raise_exception_if_dir_does_not_exist(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/cd_bad_dir.json")]
        with self.assertRaises(FileNotFoundError):
            self.instance.change_working_dir("/a/bad/dir")
        return

    def test_gdb_change_directory_malformed_gdb_response_raise_exception(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/cd_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.change_working_dir("/a/bad/dir")
        return

    def test_gdb_continue_until_breakpoint_hit_on_read(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", 20)
        self.mock_gdb_controller.write.side_effect = [read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_no_hit_write.json")]
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.continue_until_breakpoint(timeout_sec=5)
        self.mock_gdb_controller.write.assert_any_call("-exec-continue")
        self.mock_gdb_controller.get_gdb_response.assert_called_once_with(
            5, True)
        return

    def test_gdb_continue_until_breakpoint_hit_on_write(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", 20)
        self.mock_gdb_controller.write.side_effect = [read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_write.json")]
        self.instance.continue_until_breakpoint(timeout_sec=5)
        self.mock_gdb_controller.write.assert_any_call("-exec-continue")
        self.mock_gdb_controller.get_gdb_response.assert_not_called()
        return

    def test_gdb_continue_until_breakpoint_raise_exception_if_malformed_answer(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", 20)
        self.mock_gdb_controller.write.side_effect = [read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_no_hit_write.json")]
        self.mock_gdb_controller.get_gdb_response.side_effect = [read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_no_hit_read_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.continue_until_breakpoint(timeout_sec=5)
        return

    def test_gdb_continue_until_breakpoint_raise_exception_if_not_connected(self):
        with self.assertRaises(ConnectionError):
            self.instance.continue_until_breakpoint(timeout_sec=5)
        return

    def test_gdb_continue_until_breakpoint_raise_exception_if_timeout(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = GdbTimeoutError
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", 20)
        with self.assertRaises(GdbTimeoutError):
            self.instance.continue_until_breakpoint(timeout_sec=1)
        return

    def test_gdb_stopped_at_breakpoint_raises_exception_if_not_stopped(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_execution()
        with self.assertRaises(GdbValueError):
            self.instance.stopped_at_breakpoint_with_tag(
                "MySourceFile.cpp", "TEST TAG A")
        return

    def test_gdb_stopped_at_breakpoint_with_tag_returns_true_if_tag_hit_breakpoint_index_1(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        tag_hit = self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        assert tag_hit == True

    def test_gdb_stopped_at_breakpoint_with_tag_returns_true_if_tag_hit_breakpoint_index_2(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG E")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp_2
        tag_hit = self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG E")
        assert tag_hit == True

    def test_gdb_stopped_at_breakpoint_with_tag_raise_exception_if_invalid_index(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG E")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp_3
        with self.assertRaises(GdbResponseError):
            self.instance.stopped_at_breakpoint_with_tag(
                "MySourceFile.cpp", "TEST TAG E")

    def test_gdb_stopped_at_breakpoint_with_tag_raises_exception_if_tag_not_found(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        with self.assertRaises(TagNotFoundError):
            self.instance.stopped_at_breakpoint_with_tag(
                "MySourceFile.cpp", "MY WRONG TAG")
        return

    def test_gdb_delete_all_bp_deletes_all_breakpoints(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.delete_all_breakpoints()

    def test_gdb_delete_all_bp_deletes_raises_exception_malformed_response(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.mock_gdb_controller.write.side_effect = [read_from_json(
            "./robotlibraries/gdb/gdb_responses/mi_bp_del_all_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.delete_all_breakpoints()

    def test_gdb_next_makes_correct_call_to_gdb(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        self.instance.next()
        self.mock_gdb_controller.write.assert_called_with('-exec-next')

    def test_gdb_next_raises_exception_if_gdb_rsp_malformed_not_stopped(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        self.mock_gdb_controller.write.side_effect = [read_from_json(
            "./robotlibraries/gdb/gdb_responses/next_rsp_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.next()

    def test_gdb_next_raises_exception_if_gdb_rsp_malformed_not_end_stepping_range(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        self.mock_gdb_controller.write.side_effect = [read_from_json(
            "./robotlibraries/gdb/gdb_responses/next_rsp_malformed2.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.next()

    def test_gdb_next_does_not_raise_exception_if_notify_msg_is_in_other_position(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        self.mock_gdb_controller.write.side_effect = [read_from_json(
            "./robotlibraries/gdb/gdb_responses/next_rsp2.json")]
        self.instance.next()

    def test_gdb_get_variable_dec_value_correct_call(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        a = self.instance.get_variable_value("my_var", "dec")
        self.mock_gdb_controller.write.assert_called_with('print /d my_var')

    def test_gdb_get_variable_hex_value_correct_call(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        a = self.instance.get_variable_value("my_var", "hex")
        self.mock_gdb_controller.write.assert_called_with('print /x my_var')

    def test_gdb_get_variable_bin_value_correct_call(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        a = self.instance.get_variable_value("my_var", "bin")
        self.mock_gdb_controller.write.assert_called_with('print /t my_var')

    def test_gdb_get_variable_invalid_format_raise_exception(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        with self.assertRaises(ValueError):
            self.instance.get_variable_value("my_var", "Not_Valid_Value")

    def test_gdb_get_variable_return_dec_value(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        variable_my_var = self.instance.get_variable_value("my_var", "dec")
        self.assertEqual('3', variable_my_var)

    def test_gdb_get_variable_return_hex_value(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        variable_my_var = self.instance.get_variable_value("my_var", "hex")
        self.assertEqual('0x3', variable_my_var)

    def test_gdb_get_variable_return_bin_value(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        variable_my_var = self.instance.get_variable_value("my_var", "bin")
        self.assertEqual('11', variable_my_var)

    def test_gdb_get_variable_raise_exception_empty_payload(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        with self.assertRaises(GdbResponseError):
            self.instance.get_variable_value("my_bad_payload_var", "hex")

    def test_gdb_get_variable_raise_exception_symbol_not_found(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        with self.assertRaises(GdbResponseError):
            self.instance.get_variable_value("non_existent_var", "hex")

    def test_gdb_get_variable_raise_exception_symbol_not_found_for_structures(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        with self.assertRaises(GdbResponseError):
            self.instance.get_variable_value("no_exist_struct", "hex")

    def test_gdb_get_struct_as_hex_return_struct(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        variable_my_var = self.instance.get_object_value("my_struct", "hex")
        self.assertEqual('{var1 = 0x3, var2 = 0xc, var3 = 0x40020c00}', variable_my_var)

    def test_gdb_get_struct_as_hex_return_struct(self):
        self.mock_gdb_controller.write.side_effect = self.gdb_responses_open_ocd
        self.mock_gdb_controller.get_gdb_response.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_continue_stop_break_hit_read.json")]
        self.instance.connect("localhost", "3333")
        self.instance.load_elf_file("/path/to/elf/file")
        self.instance.change_working_dir(
            "/home/erick/Desktop/EITF/embedded-integration-test-framework/Robot Framework Libraries/GDB/gdb_responses")
        self.instance.flash()
        self.instance.insert_breakpoint("MySourceFile.cpp", tag="TEST TAG A")
        self.instance.continue_until_breakpoint(timeout_sec=1)
        self.mock_gdb_controller.write.side_effect = self.gdb_bp
        self.instance.stopped_at_breakpoint_with_tag(
            "MySourceFile.cpp", "TEST TAG A")
        variable_my_var = self.instance.get_object_value("my_struct", "hex")
        self.assertEqual('{var1 = 0x3, var2 = 0xc, var3 = 0x40020c00}', variable_my_var)

    def test_gdb_send_command_creates_json(self):
        file_path = './my_command_generated.json'
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/my_command.json")]
        self.instance.send_command("my_command","my_command_generated.json")
        self.mock_gdb_controller.write.assert_any_call("my_command")
        assert os.path.exists(file_path), f"File '{file_path}' does not exist."
        os.remove(file_path)


    def test_gdb_send_command_creates_json_with_eq_content(self):
        file_path = './my_command_generated.json'
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/my_command.json")]
        self.instance.send_command("my_command","my_command_generated.json")
        self.mock_gdb_controller.write.assert_any_call("my_command")
        assert os.path.exists(file_path), f"File '{file_path}' does not exist."
        os.remove(file_path)


    def test_gdb_log_file_change_name_correct_call(self):
        log_file_path = './my_log_file.txt'
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_file_cmd.json")]
        self.instance.set_log_file_path(log_file_path)
        self.mock_gdb_controller.write.assert_any_call("-gdb-set logging file "+log_file_path)

    def test_gdb_log_file_does_nothing_on_done_rsp(self):
        log_file_path = './my_log_file.txt'
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_file_cmd.json")]
        self.instance.set_log_file_path(log_file_path)
        self.mock_gdb_controller.write.assert_any_call("-gdb-set logging file "+log_file_path)
    
    def test_gdb_log_file_raise_exception_on_error(self):
        log_file_path = './my_log_file.txt'
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_file_cmd_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.set_log_file_path(log_file_path)

    def test_gdb_log_file_raise_exception_on_malformed_rsp(self):
        log_file_path = './my_log_file.txt'
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_file_cmd_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.set_log_file_path(log_file_path)

    def test_gdb_log_file_start_log(self):
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_on_off_cmd.json")]
        self.instance.start_logging()
        self.mock_gdb_controller.write.assert_any_call("--gdb-set logging on")

    def test_gdb_log_file_start_raise_exception_on_error_rsp(self):
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_file_cmd_error.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.start_logging()

    def test_gdb_log_file_start_raise_exception_on_malformed_rsp(self):
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_file_cmd_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.start_logging()
            
    def test_gdb_log_file_stop_log(self):
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_on_off_cmd.json")]
        self.instance.stop_logging()
        self.mock_gdb_controller.write.assert_any_call("--gdb-set logging off")
        

    def test_gdb_log_file_stop_raise_exception_on_error_rsp(self):
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_file_cmd_error.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.stop_logging()

    def test_gdb_log_file_stop_raise_exception_on_malformed_rsp(self):
        self.mock_gdb_controller.write.side_effect = [
            read_from_json("./robotlibraries/gdb/gdb_responses/mi_set_log_file_cmd_malformed.json")]
        with self.assertRaises(GdbResponseError):
            self.instance.stop_logging()


if __name__ == '__main__':
    unittest.main()


# To implement flash erase_address
