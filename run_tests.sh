#!/bin/bash
#pytest -k test_gdb_sets_mi_async_on -v
#pytest -k test_open -v
pytest -s test_* -v
python3.9 verify_startup.py
python3.9 verify_shutdown.py

