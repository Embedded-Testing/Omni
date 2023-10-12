#include "GPIO_Driver.hpp"
#include "Reset_Clock_Control.hpp"
#include "spi.hpp"

void SPI2_GPIO_init(void);

using namespace SPI_DATATYPES;
RC_Control gRCC_Control = RC_Control();

/*
PB14 --> SPI2_MISO
PB15 --> SPI2_MOSI
PB13 --> SPI2_SCLK
PB12 --> SPI2_NSS
ALT fun --> 5
*/

const SPI_CONFIG my_spi_cfg = {.mode = MASTER,
                               .bus_config = FULL_DUPLEX,
                               .baud_rate_divisor = _256,
                               .clk_polarity = CLK_IDLE_LOW,
                               .clk_phase = CAPTURE_ON_FIRST_EDGE,
                               .slave_management = SOFTWARE};

const GPIO_CONFIG spi_pin_config = {.pin_mode_cfg = alternate,
                                    .output_type_cfg = push_pull,
                                    .speed_type_cfg = high_speed,
                                    .pull_type_cfg = no_pull,
                                    .alt_fun_type_cfg = AF5};

void SPI2_GPIO_init(void) {
  // GPIO_Driver SPI2_MISO = GPIO_Driver(PORT_B, PIN_POS_14, spi_pin_config);
  GPIO_Driver SPI2_MOSI = GPIO_Driver(PORT_B, PIN_POS_15, spi_pin_config);
  GPIO_Driver SPI2_SCLK = GPIO_Driver(PORT_B, PIN_POS_13, spi_pin_config);
  // GPIO_Driver SPI2_NSS = GPIO_Driver(PORT_B, PIN_POS_12, spi_pin_config);
}

uint8_t MsgBuffer[] = {0x65, 0x66, 0x67, 0x68};
const uint32_t buffer_sz = sizeof(MsgBuffer) / sizeof(MsgBuffer[0]);

void delay(void) {
  for (uint32_t i = 0; i < 500000; i++)
    ;
}

int main() {
  SPI2_GPIO_init();  // TEST_TAG_A
  SPI<uint8_t> myspi = SPI<uint8_t>(SPI2, my_spi_cfg);
  while (1) {
    myspi.send_data(MsgBuffer, buffer_sz);
    delay();
  }
}
