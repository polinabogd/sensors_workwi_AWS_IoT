// Wokwi Custom Chip - For docs and examples see:
// https://docs.wokwi.com/chips-api/getting-started
//
// SPDX-License-Identifier: MIT
// Copyright 2023 Кто-то

#include "wokwi-api.h"
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  pin_t tx_pin;
  pin_t rx_pin;
  int co2Value;
} chip_data_t;

void chip_timer_callback(void *data) {
  chip_data_t *chip_data = (chip_data_t*)data;
  int co2Value = attr_read(chip_data->co2Value);

  // Simulate UART transmission of CO2 value
  uint8_t response[9] = {0xFF, 0x86, (co2Value >> 8) & 0xFF, co2Value & 0xFF, 0x00, 0x00, 0x00, 0x00, 0x79};
  for (int i = 0; i < 9; i++) {
    pin_write(chip_data->tx_pin, response[i]);
  }
}

void chip_init() {
  chip_data_t *chip_data = (chip_data_t*)malloc(sizeof(chip_data_t));
  chip_data->co2Value = attr_init("tdsValue", 400); // Initial CO2 value (for simulation)
  chip_data->tx_pin = pin_init("TX", OUTPUT);
  chip_data->rx_pin = pin_init("RX", INPUT);

  const timer_config_t config = {
    .callback = chip_timer_callback,
    .user_data = chip_data,
  };

  timer_t timer_id = timer_init(&config);
  timer_start(timer_id, 1000, true); // Update every 1000 milliseconds
}
