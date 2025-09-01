// lora_comms.cpp - اتصالات لورا
#include <LoRa.h>
#include "lora_comms.h"

void initLoRa() {
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed!");
    while (1);
  }
  LoRa.setTxPower(20);
  Serial.println("LoRa Initialized");
}

void sendLoRaData(SensorData data) {
  LoRa.beginPacket();
  LoRa.print("Soil:");
  LoRa.print(data.soilMoisture);
  LoRa.print(",Temp:");
  LoRa.print(data.temperature);
  LoRa.print(",Hum:");
  LoRa.print(data.humidity);
  LoRa.endPacket();
}