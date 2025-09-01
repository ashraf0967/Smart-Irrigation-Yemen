// power_management.cpp - إدارة الطاقة
#include "power_management.h"

void initPowerManagement() {
  // تهيئة ADC لمراقبة البطارية
  analogReadResolution(12);
}

float getBatteryVoltage() {
  int raw = analogRead(36);  // منفذ ADC1_CH0 (GPIO36)
  return raw * (3.3 / 4095.0) * 2.0;  // قسمة الجهد
}

void managePower() {
  float voltage = getBatteryVoltage();
  if (voltage < 3.3) {
    Serial.println("Low Battery Warning!");
  }
}