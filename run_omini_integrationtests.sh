python3 ./Omini/tests/integration_tests/startup.py
robot --outputdir Omini/tests/integration_tests/Temp/GPIO --report Omini_Integration_GPIO.html ./Omini/tests/integration_tests/Omini_Integration_GPIO.robot
robot --outputdir Omini/tests/integration_tests/Temp/I2C --report Omini_Integration_I2C.html ./Omini/tests/integration_tests/Omini_Integration_I2C.robot
robot --outputdir Omini/tests/integration_tests/Temp/SPI --report Omini_Integration_SPI.html ./Omini/tests/integration_tests/Omini_Integration_SPI.robot
robot --outputdir Omini/tests/integration_tests/Temp/UART --report Omini_Integration_UART.html ./Omini/tests/integration_tests/Omini_Integration_UART.robot
python3 ./Omini/tests/integration_tests/shutdown.py

