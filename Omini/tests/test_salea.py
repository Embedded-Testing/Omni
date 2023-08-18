import os
import unittest
from unittest.mock import patch,ANY,MagicMock,mock_open
import shutil
from ..applications.Salea import *
from ..process_manager.process_manager import *

folder_path="./TempSalea"
DummyProcess_file="./TempSalea/my_process_cfg.json"

salea_path ="/path/to/salea"
board_cfg_file_path ="/board/board.cfg"
salea_log_path =folder_path+"/Salea.txt"
dummy_port=7890

class TestSalea(unittest.TestCase):
    
    @classmethod
    def setup_class(cls):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            shutil.rmtree(folder_path)
            os.makedirs(folder_path)

    def test_launch_salea_raises_exception_if_process_file_dont_exist(self):
        with self.assertRaises(FileNotFoundError):
            launch_salea(salea_path,salea_log_path,dummy_port,DummyProcess_file)
    
    @patch('subprocess.Popen', side_effect=None)
    def test_launch_salea_dont_raise_exception_if_process_file_exist(self,mock_subprocess):
        create_config_file(DummyProcess_file)
        launch_salea(salea_path,salea_log_path,dummy_port,DummyProcess_file)
        os.remove(DummyProcess_file)
    
    def test_launch_salea_raises_exception_if_file_has_bad_format(self):
        file_path ="TempSalea/my_bad_format_file.json"
        with open(file_path, 'w') as f:
            f.write('This is a dummy file.')
        with self.assertRaises(ValueError):
            launch_salea(salea_path,salea_log_path,dummy_port,file_path)
        os.remove(file_path)

    @patch('subprocess.Popen', side_effect=None)
    def test_launches_openocd_application_correct_call(self,mock_subprocess):
        create_config_file(DummyProcess_file)
        process_file=os.path.abspath(DummyProcess_file)
        salea_launch_command=str(salea_path)+" "+"--automation --automationPort "+str(dummy_port)
        launch_salea(salea_path,salea_log_path,dummy_port,process_file)
        mock_subprocess.assert_called_with(salea_launch_command.split(),stdout=ANY,stderr=ANY)
        os.remove(DummyProcess_file)
    
    @patch('subprocess.Popen', side_effect=None)
    def test_launches_openocd_application_correct_log(self,mock_subprocess):
        create_config_file(DummyProcess_file)
        process_file=os.path.abspath(DummyProcess_file)
        salea_launch_command=str(salea_path)+" "+"--automation --automationPort "+str(dummy_port)
        launch_salea(salea_path,salea_log_path,dummy_port,process_file)
        mock_subprocess.assert_called_with(salea_launch_command.split(),stdout=ANY,stderr=ANY)
        call_args = mock_subprocess.call_args
        stdout_value = call_args[1]['stdout']
        stderr_value = call_args[1]['stderr']
        assert(stdout_value.name==salea_log_path)
        assert(stderr_value.name==salea_log_path)       
        os.remove(DummyProcess_file)

    @patch('time.sleep', return_value=None)
    def test_verify_salea_startup_does_nothing_if_line_is_in_log(self,mock_sleep):
        mock_log_content = "[2023-07-28 09:16:44.025835] [I] [tid  67216] [main] [logic_device_node.cpp:407] set led"
        with patch("builtins.open", mock_open(read_data=mock_log_content)):
            verify_salea_startup("path/to/your/mock/log_file.txt")

    @patch('time.sleep', return_value=None)
    def test_verify_salea_startup_raise_exception_if_line_is_not_in_log(self,mock_sleep):
        mock_log_content = "\n XXXXXXinvalid line that does not content the search string"
        with patch("builtins.open", mock_open(read_data=mock_log_content)):
            with self.assertRaises(Exception):
                verify_salea_startup("path/to/your/mock/log_file.txt")
        

    @patch('subprocess.Popen', side_effect=None)
    @patch('Omini.process_manager.process_manager.append_process_data_to_file', side_effect=None)
    def test_launches_openocd_creates_correct_process_entry(self,mock_append_process_data,mock_subprocess):
        mock_popen_instance = MagicMock()
        mock_popen_instance.pid = 12345
        mock_subprocess.return_value = mock_popen_instance
        salea_launch_command=str(salea_path)+" "+"--automation --automationPort "+str(dummy_port)
        process_file=os.path.abspath(DummyProcess_file)
        create_config_file(DummyProcess_file)
        launch_salea(salea_path,salea_log_path,dummy_port,process_file)
        call_args = mock_append_process_data.call_args
        salea_process_entry =call_args[0][0]
        assert (salea_process_entry["application"]=="Salea Logic Analyser")
        assert (salea_process_entry["pid"]=="12345")
        assert (salea_process_entry["log_file"]==salea_log_path)
        assert (salea_process_entry["process_call"]==salea_launch_command)
        assert (salea_process_entry["port"]==dummy_port)
        assert (salea_process_entry["pgrep_string"]=="Logic")
        os.remove(DummyProcess_file)
        
    @classmethod
    def teardown_class(cls):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)