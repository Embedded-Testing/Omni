import shutil
import time

import Omni.process_manager.process_manager as HostManager
import Omni.applications.Openocd as Openocd
import Omni.applications.Salea as SaleaBackend
from Omni.robotlibraries.gdb.gdb_control import *

current_file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(current_file_path)+"/Temp"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
else:
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)

process_file = folder_path+"/my_process_cfg.json"
openocd_log_file = folder_path+"/OpenOCD_LOG.txt"
salea_log_file = folder_path+"/Salea_LOG.txt"
HostManager.create_config_file(process_file)
Openocd.launch_openocd(process_file, "/usr/bin/openocd", "/usr/share/openocd/scripts/board/stm32f4discovery.cfg",
                       "/usr/share/openocd/scripts/interface/stlink-v2.cfg", openocd_log_file)
SaleaBackend.launch_salea("/usr/local/bin/Logic",
                          salea_log_file, 10430, process_file, headless=True)
SaleaBackend.verify_salea_startup(salea_log_file, 20)
Openocd.verify_openocd(openocd_log_file)
