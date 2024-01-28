import Omni.applications.Sigrok as Sigrok
import Omni.process_manager.process_manager as process_manager
import os
import pathlib
import shutil
import time

temporary_folder = pathlib.Path("./TempSigrok")
process_file_path = temporary_folder / "ProcessFile.json"
log_file_path = temporary_folder / "SigrokLog.txt"


def create_temp_folder():
    folder_name = temporary_folder
    folder_name.mkdir(parents=True, exist_ok=True)


def cleanup_temp_folder():
    if os.path.exists(temporary_folder):
        shutil.rmtree(temporary_folder)


port = 10430
cleanup_temp_folder()
create_temp_folder()
process_manager.create_config_file(process_file_path)
Sigrok.launch_sigrok_process_host(port, process_file_path, log_file_path)
time.sleep(10)
process_manager.close_applications(process_file_path)

