*** Settings ***
Documentation       Hardware tests for STM32F4DISCO board

Library             Process
Library             Omni.robotlibraries.gdb    WITH NAME    Debugger

Suite Setup         Firmware Start-up


*** Variables ***
${GPIO_INTEGRATION_TEST_ELF}        ${CURDIR}${/}GPIO_integration_tests${/}test_build${/}GPIO_integration_test.elf
${GPIO_INTEGRATION_TEST_SOURCE}     ${CURDIR}${/}GPIO_integration_tests${/}test_build${/}GPIO_integration_test.cpp
${GDB_LOG_PATH}                     ${CURDIR}${/}Temp${/}Gdb_GPIO.log
${DATA_OUT_OFFSET}                  5


*** Test Cases ***
GPIO INTEGRATION TESTS
    [Documentation]    Integration tests for the GPIO module
    [Tags]    gpio_configuration
    Debugger.Insert Breakpoint    source_file_path=${GPIO_INTEGRATION_TEST_SOURCE}    tag=// TEST TAG A
    Debugger.Continue Until Breakpoint
    ${DATA_OUT}    Debugger.Get Object Value    *(gpio_led_green.gpio_base_address+${DATA_OUT_OFFSET})    hex
    Should Be Equal    ${DATA_OUT}    0x0
    Debugger.Insert Breakpoint    source_file_path=${GPIO_INTEGRATION_TEST_SOURCE}    tag=// TEST TAG B
    Debugger.Continue Until Breakpoint
    ${DATA_OUT}    Debugger.Get Object Value    *(gpio_led_green.gpio_base_address+${DATA_OUT_OFFSET})    hex
    Should Be Equal    ${DATA_OUT}    0x1000


*** Keywords ***
Firmware Start-up
    Log    ${GDB_LOG_PATH}
    Debugger.Set Log File Path    ${GDB_LOG_PATH}
    Debugger.Start Logging
    Debugger.Connect    localhost    3333
    Debugger.Load Elf File    ${GPIO_INTEGRATION_TEST_ELF}
    Debugger.Flash
    Debugger.Reset Halt
