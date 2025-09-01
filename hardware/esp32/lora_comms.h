// lora_comms.h
#ifndef LORA_COMMS_H
#define LORA_COMMS_H

#include "sensor_reading.h"

void initLoRa();
void sendLoRaData(SensorData data);

#endif