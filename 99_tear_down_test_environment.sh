#!/bin/bash

# Define ANSI escape codes for text formatting
BOLD_BLUE='\e[1;34m'
BOLD_GREEN='\e[1;32m'
RESET='\e[0m'

source venv/bin/activate
echo -e "${BOLD_BLUE}Deactivating the virtual environment...${RESET}"
deactivate

venv_name="venv"
echo -e "${BOLD_BLUE}Removing the virtual environment '$venv_name'...${RESET}"
rm -rf $venv_name

echo -e "${BOLD_GREEN}Test Environment tear-down complete.${RESET}"

