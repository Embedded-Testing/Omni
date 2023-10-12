*** Settings ***
Documentation       Hardware tests for STM32F4DISCO board

Library             Process
Library             Omini.robotlibraries.gdb    WITH NAME    Debugger
Library             Omini.robotlibraries.SaleaLogicAnalyzer.LogicAnalyzer    WITH NAME    SaleaAnalyser
Library             Omini.robotlibraries.SaleaLogicAnalyzer.SaleaConfig

Suite Setup         Firmware Start-up
Suite Teardown      Close Backend Connection


*** Variables ***
${UART_INTEGRATION_TEST_ELF}        /home/erick/Desktop/GitPrjOmini/Omini/tests/integration_tests/UART_integration_tests/test_build/uart.elf
${UART_INTEGRATION_TEST_SOURCE}     /home/erick/Desktop/GitPrjOmini/Omini/tests/integration_tests/UART_integration_tests/test_build/main.c
${CAPTURE_PATH}                     /home/erick/Desktop/GitPrjOmini/Omini/tests/integration_tests/Temp
${GDB_LOG_PATH}                     /home/erick/Desktop/GitPrjOmini/Omini/tests/integration_tests/Temp/Gdb_GPIO.log


*** Test Cases ***
UART INTEGRATION TESTS
    [Documentation]    Integration tests for the uart module
    [Tags]    uart capture tests
    Debugger.Load Elf File    ${UART_INTEGRATION_TEST_ELF}
    Debugger.Flash
    Debugger.Reset Halt
    SaleaAnalyser.Set Timed Capture    3
    SaleaAnalyser.Set Device Configuration    ${2,3}    50_000_000    digital_threshold_volts=3.3
    SaleaAnalyser.Start Capture
    Debugger.Continue Execution
    SaleaAnalyser.Wait Capture End
    SaleaAnalyser.Save Raw    ${CAPTURE_PATH}    UART_TEST.sal
    &{UART_CHANNELS_CFG}    Config Uart Channel
    ...    2
    ...    115200
    ...    8
    ...    1
    ...    None
    ...    LSB
    ...    False
    ...    Normal
    SaleaAnalyser.Add Uart Analyser    ${UART_CHANNELS_CFG}    UART_ANALYSER
    SaleaAnalyser.Export To Csv    ${CAPTURE_PATH}    UART_Integration_TEST.txt    analyser_label=UART_ANALYSER


*** Keywords ***
Firmware Start-up
    Debugger.Set Log File Path    ${GDB_LOG_PATH}
    Debugger.Start Logging
    Debugger.Connect    localhost    3333
    SaleaAnalyser.Connect To Backend

Close Backend Connection
    SaleaAnalyser.Disconnect From Backend
