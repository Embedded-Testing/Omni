*** Settings ***
Documentation       Hardware tests for STM32F4DISCO board

Library             Process
Library             Omni.robotlibraries.gdb    WITH NAME    Debugger
Library             Omni.robotlibraries.SaleaLogicAnalyzer.LogicAnalyzer    WITH NAME    SaleaAnalyser
Library             Omni.robotlibraries.SaleaLogicAnalyzer.SaleaConfig

Suite Setup         Firmware Start-up
Suite Teardown      Close Backend Connection


*** Variables ***
${I2C_INTEGRATION_TEST_ELF}         ${CURDIR}${/}I2C_integration_tests${/}test_build${/}i2c_hal.elf
${I2C_INTEGRATION_TEST_SOURCE}      ${CURDIR}${/}I2C_integration_tests${/}test_build${/}main.c
${CAPTURE_PATH}                     ${CURDIR}${/}Temp
${GDB_LOG_PATH}                     ${CURDIR}${/}Temp${/}Gdb_I2C.log


*** Test Cases ***
I2C INTEGRATION TESTS
    [Documentation]    Integration tests for the I2c module
    [Tags]    i2c capture tests
    Debugger.Load Elf File    ${I2C_INTEGRATION_TEST_ELF}
    Debugger.Flash
    Debugger.Reset Halt
    Debugger.Insert Breakpoint    source_file_path=${I2C_INTEGRATION_TEST_SOURCE}    tag=HAL_Delay(25);

    SaleaAnalyser.Set Timed Capture    3
    SaleaAnalyser.Set Device Configuration    ${0,1}    100_000_000    digital_threshold_volts=3.3
    SaleaAnalyser.Start Capture
    Debugger.Continue Until Breakpoint    timeout_sec=3
    ${DATA_OUT}    Debugger.Get Object Value    (MANUF_ID)    hex
    Should Be Equal    ${DATA_OUT}    0x54
    ${DATA_OUT}    Debugger.Get Object Value    (DEV_ID)    hex
    Should Be Equal    ${DATA_OUT}    0x400
    Debugger.Continue Execution
    SaleaAnalyser.Wait Capture End
    SaleaAnalyser.Save Raw    ${CAPTURE_PATH}    I2C_TEST.sal
    &{I2C_CHANNELS_CFG}    Config I2c Channels    SCL=0    SDA=1
    SaleaAnalyser.Add I2c Analyser    i2c_channel_cfg=&{I2C_CHANNELS_CFG}    label=I2C_CAP
    SaleaAnalyser.Export To Csv    ${CAPTURE_PATH}    I2C_Integration_TEST.txt    analyser_label=I2C_CAP


*** Keywords ***
Firmware Start-up
    Debugger.Set Log File Path    ${GDB_LOG_PATH}
    Debugger.Start Logging
    Debugger.Connect    localhost    3333
    SaleaAnalyser.Connect To Backend

Close Backend Connection
    SaleaAnalyser.Disconnect From Backend
