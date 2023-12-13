*** Settings ***
Documentation       Hardware tests for STM32F4DISCO board

Library             Process
Library             Omini.robotlibraries.gdb    WITH NAME    Debugger
Library             Omini.robotlibraries.SaleaLogicAnalyzer.LogicAnalyzer    WITH NAME    SaleaAnalyser
Library             Omini.robotlibraries.SaleaLogicAnalyzer.SaleaConfig

Suite Setup         Firmware Start-up
Suite Teardown      Close Backend Connection


*** Variables ***
${SPI_INTEGRATION_TEST_ELF}         ${CURDIR}${/}SPI_integration_tests${/}test_build${/}SPI_DataSend_Blocking_test.elf
${SPI_INTEGRATION_TEST_SOURCE}      ${CURDIR}${/}SPI_integration_tests${/}test_build${/}SPI_DataSend_Blocking_test.cpp
${CAPTURE_PATH}                     ${CURDIR}${/}Temp
${GDB_LOG_PATH}                     ${CURDIR}${/}Temp/Gdb_SPI.log


*** Test Cases ***
SPI INTEGRATION TESTS
    [Documentation]    Integration tests for the SPI module
    [Tags]    spi capture tests
    Debugger.Load Elf File    ${SPI_INTEGRATION_TEST_ELF}
    Debugger.Flash
    Debugger.Reset Halt
    Debugger.Continue Execution
    SaleaAnalyser.Set Timed Capture    5
    SaleaAnalyser.Set Device Configuration    ${4,5}    50_000_000    digital_threshold_volts=3.3
    SaleaAnalyser.Start Capture
    SaleaAnalyser.Wait Capture End
    SaleaAnalyser.Save Raw    ${CAPTURE_PATH}    SPI_DATA_SEND_BLOCK_TEST.sal
    &{SPI_CHANNELS_CFG}    Config Spi Channels    MOSI=4    Clock=5
    &{PROTOCOL_CFG}    Config Spi Protocol
    ...    DATA_FRAME_SIZE=8
    ...    FIRST_BIT=MSB
    ...    CPOL=0
    ...    CPHA=0
    ...    EnableLineActiveOn=0
    SaleaAnalyser.Add Spi Analyser
    ...    SPI_CHANNEL_CFG=&{SPI_CHANNELS_CFG}
    ...    PROTOCOL_CFG=&{PROTOCOL_CFG}
    ...    label=SPI_CAP
    SaleaAnalyser.Export To Csv    ${CAPTURE_PATH}    SPI_DATA_SEND_BLOCK_TEST.txt    analyser_label=SPI_CAP


*** Keywords ***
Firmware Start-up
    Debugger.Set Log File Path    ${GDB_LOG_PATH}
    Debugger.Start Logging
    Debugger.Connect    localhost    3333
    SaleaAnalyser.Connect To Backend

Close Backend Connection
    SaleaAnalyser.Disconnect From Backend
