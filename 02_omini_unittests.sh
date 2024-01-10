#!/bin/bash
set -e

# Define ANSI escape codes for text formatting
BOLD_BLUE='\e[1;34m'
BOLD_GREEN='\e[1;32m'
RESET='\e[0m'

echo -e "${BOLD_BLUE}Activating the Python virtual environment...${RESET}"
source venv/bin/activate

echo -e "${BOLD_BLUE}Running unit tests with pytest...${RESET}"
pytest ./Omni/tests/unit_tests/test_* -v

echo -e "${BOLD_GREEN}Unit tests completed successfully.${RESET}"

echo -e "${BOLD_BLUE}Installing Omni package...${RESET}"
python3 setup.py sdist
pip install dist/Omni-0.0.1.tar.gz
echo -e "${BOLD_GREEN}Omni package installed.${RESET}"



