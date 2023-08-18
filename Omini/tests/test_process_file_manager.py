import os
import unittest
from unittest.mock import patch,MagicMock,call
from io import StringIO
import sys
import shutil

from ..process_manager.process_manager import *

dummy_entry1 = {
    "application": "AnotherApp",
    "pid": 1234,
    "log_file": "another_app.log",
    "process_call": "python another_app.py",
    "pgrep_string": "App"
    }

dummy_entry2 = {
    "application": "AnotherApp2",
    "pid": 1233,
    "log_file": "another_app.log",
    "process_call": "python another_app.py",
    "pgrep_string": "App"
    }

invalid_entry = {
    "invalid": "AnotherApp",
    }


class TestProcessManager(unittest.TestCase):
    
    @classmethod
    def setup_class(cls):
        folder_path="Temp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            shutil.rmtree(folder_path)
            os.makedirs(folder_path)
        

    def test_process_file_print_error_if_file_exists(self):
        file_path ="Temp/my_existing_file.json"
        with open(file_path, 'w') as f:
            f.write('This is a dummy file.')
        captured_output = StringIO()
        sys.stdout = captured_output
        create_config_file(file_path)
        sys.stdout = sys.__stdout__
        printed_string = captured_output.getvalue().strip()
        assert "ERROR: FILE ALREADY EXISTS" in printed_string
        os.remove(file_path)
        

    def test_append_process_data_to_file_saves_one_into_file(self):
        file_path ="Temp/my_process_cfg.json"
        create_config_file(file_path)
        append_process_data_to_file(dummy_entry1,file_path)
        with open(file_path, "r") as file:
            actual_data = json.load(file)
        assert actual_data == [dummy_entry1]
        os.remove(file_path)

    def test_append_process_data_to_file_saves_two_entries_into_file(self):
        file_path ="Temp/my_process_cfg.json"
        create_config_file(file_path)
        append_process_data_to_file(dummy_entry1,file_path)
        append_process_data_to_file(dummy_entry2,file_path)
        with open(file_path, "r") as file:
            actual_data = json.load(file)
        assert actual_data == [dummy_entry1,dummy_entry2]
        os.remove(file_path)

    def test_append_process_data_to_file_throws_exception_if_entry_incomplete(self):
        file_path ="Temp/my_process_cfg.json"
        create_config_file(file_path)
        with self.assertRaises(InvalidProcessEntry):
            append_process_data_to_file(invalid_entry,file_path)
        os.remove(file_path)

    def test_append_process_data_to_file_saves_process_data_into_file(self):
        file_path ="Temp/my_process_cfg.json"
        create_config_file(file_path)
        append_process_data_to_file(dummy_entry1,file_path)
        with open(file_path, "r") as file:
            actual_data = json.load(file)
        assert actual_data == [dummy_entry1]
        os.remove(file_path)

    def test_append_process_data_to_file_throws_exception_file_not_found(self):
        file_path ="Temp/nonexistent_file.json"
        with self.assertRaises(FileNotFoundError):
            append_process_data_to_file(dummy_entry1,file_path)

    def test_manager_deletes_file_if_file_empty(self):
        file_path ="Temp/my_process_cfg.json"
        create_config_file(file_path)
        delete_config_file(file_path)
        self.assertFalse( os.path.isfile(file_path))
    
    def test_manager_does_not_deletes_file_if_file_not_empty(self):
        file_path ="Temp/my_process_cfg.json"
        create_config_file(file_path)
        append_process_data_to_file(dummy_entry1,file_path)
        delete_config_file(file_path)
        self.assertTrue(os.path.isfile(file_path))
        os.remove(file_path)

    @patch('subprocess.run', side_effect=None)
    def test_manager_kills_all_applications(self,mock_subprocess_run):
        file_path ="Temp/my_process_cfg.json"
        create_config_file(file_path)
        append_process_data_to_file(dummy_entry1,file_path)
        append_process_data_to_file(dummy_entry2,file_path)
        close_applications(file_path)
        expected_calls = [call.mock_subprocess_run(["kill", dummy_entry1["pid"]]),call.mock_subprocess_run(["kill", dummy_entry2["pid"]])]
        mock_subprocess_run.assert_has_calls(expected_calls)
        os.remove(file_path)

    # def test_manager_verifies_if_application_closed(self,mock_subprocess_run):
    #     file_path ="Temp/my_process_cfg.json"
    #     create_config_file(file_path)
    #     append_process_data_to_file(dummy_entry1,file_path)
    #     append_process_data_to_file(dummy_entry2,file_path)
    #     close_applications(file_path)
    #     expected_calls = [call.mock_subprocess_run(["kill", dummy_entry1["pid"]]),call.mock_subprocess_run(["kill", dummy_entry2["pid"]])]
    #     mock_subprocess_run.assert_has_calls(expected_calls)
    #     os.remove(file_path)

    @classmethod
    def teardown_class(cls):
        folder_path="Temp"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)


        