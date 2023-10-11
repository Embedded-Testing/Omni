from Omini.process_manager.process_manager import *
from Omini.applications.Openocd import *
from Omini.applications.Salea import *
from Omini.robotlibraries.gdb.gdb import *

current_file_path = os.path.abspath(__file__)
process_file = os.path.dirname(current_file_path)+"/Temp/my_process_cfg.json"

close_applications(process_file)
