import sys
import shutil
import time


my_desired_path = '/home/erick/Desktop/Omini'
sys.path.append(my_desired_path)

from Omini.process_manager.process_manager import *
from Omini.applications.Openocd import *
from Omini.applications.Salea import *
from Omini.robotlibraries.gdb.gdb import *

folder_path="/home/erick/Desktop/Omini/Temp"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
else:
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)

process_file ="/home/erick/Desktop/Omini/Temp/my_process_cfg.json"
openocd_log_file ="/home/erick/Desktop/Omini/Temp/OpenOCD_LOG.txt"
salea_log_file ="/home/erick/Desktop/Omini/Temp/Salea_LOG.txt"
create_config_file(process_file)
launch_openocd(process_file,"/usr/bin/openocd","/usr/share/openocd/scripts/board/stm32f4discovery.cfg","/usr/share/openocd/scripts/interface/stlink-v2.cfg",openocd_log_file)
launch_salea("/usr/local/bin/Logic", salea_log_file, 10430,process_file)
time.sleep(10)
gdb_controller=gdb()
gdb_controller.connect("localhost", "3333")
#gdb_controller.load_elf_file("/path/to/elf/file")
verify_salea_startup(salea_log_file,20)


