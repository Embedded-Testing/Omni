import shutil
import time

from Omini.process_manager.process_manager import *
from Omini.applications.Openocd import *
from Omini.applications.Salea import *
from Omini.robotlibraries.gdb.gdb import *

current_file_path = os.path.abspath(__file__)
folder_path= os.path.dirname(current_file_path)+"/Temp"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
else:
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)

process_file =folder_path+"/my_process_cfg.json"
openocd_log_file =folder_path+"/OpenOCD_LOG.txt"
salea_log_file =folder_path+"/Salea_LOG.txt"
create_config_file(process_file)
launch_openocd(process_file,"/usr/bin/openocd","/usr/share/openocd/scripts/board/stm32f4discovery.cfg","/usr/share/openocd/scripts/interface/stlink-v2.cfg",openocd_log_file)
launch_salea("/usr/local/bin/Logic", salea_log_file, 10430,process_file)
time.sleep(10)
gdb_controller=gdb()
gdb_controller.connect("localhost", "3333")
#gdb_controller.load_elf_file("/path/to/elf/file")
verify_salea_startup(salea_log_file,20)


