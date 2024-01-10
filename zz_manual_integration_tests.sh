#!/bin/bash
./01_prepare_test_environment.sh
./02_omini_unittests.sh
./99_tear_down_test_environment.sh

#!/bin/bash
./01_prepare_test_environment.sh
echo -e "${BOLD_BLUE}Activating the Python virtual environment...${RESET}"
source venv/bin/activate
echo -e "${BOLD_BLUE}Installing Omni package...${RESET}"
python3 setup.py sdist
pip install dist/Omni-0.0.1.tar.gz
echo -e "${BOLD_GREEN}Omni package installed.${RESET}"
./03_omini_start_host_applications.sh
./04_omini_integrationtests.sh
./98_omini_stop_host_applications.sh
./99_tear_down_test_environment.sh