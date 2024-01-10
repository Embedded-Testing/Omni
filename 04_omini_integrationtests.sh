#!/bin/bash
set -e

# ANSI escape codes for bold blue text
BLUE_BOLD='\e[1;34m'
# ANSI escape codes for bold green text
GREEN_BOLD='\e[1;32m'
# ANSI escape code to reset text formatting
RESET='\e[0m'

echo -e "${BLUE_BOLD}Activating the Python virtual environment...${RESET}"
source venv/bin/activate

echo -e "${BLUE_BOLD}Running integration tests for GPIO...${RESET}"
robot --outputdir ./Omni/tests/integration_tests/Temp/GPIO --report Omni_Integration_GPIO.html ./Omni/tests/integration_tests/Omni_Integration_GPIO.robot

echo -e "${BLUE_BOLD}Running integration tests for SPI...${RESET}"
robot --outputdir Omni/tests/integration_tests/Temp/SPI --report Omni_Integration_SPI.html ./Omni/tests/integration_tests/Omni_Integration_SPI.robot

echo -e "${BLUE_BOLD}Running integration tests for I2C...${RESET}"
robot --outputdir Omni/tests/integration_tests/Temp/I2C --report Omni_Integration_I2C.html ./Omni/tests/integration_tests/Omni_Integration_I2C.robot

# Uncomment the following line if needed
#echo -e "${BLUE_BOLD}Running integration tests for UART...${RESET}"
#robot --outputdir Omni/tests/integration_tests/Temp/UART --report Omni_Integration_UART.html ./Omni/tests/integration_tests/Omni_Integration_UART.robot

echo -e "${GREEN_BOLD}Integration tests completed successfully.${RESET}"
