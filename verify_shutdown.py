import sys
import shutil
import time

my_desired_path = '/home/erick/Desktop/Omini'
sys.path.append(my_desired_path)

from Omini.process_manager.process_manager import *
from Omini.applications.Openocd import *
from Omini.applications.Salea import *
from Omini.robotlibraries.gdb.gdb import *


process_file ="/home/erick/Desktop/Omini/automation/Temp/my_process_cfg.json"
close_applications(process_file)

