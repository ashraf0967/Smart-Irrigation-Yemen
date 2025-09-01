// main.ino - الملف الرئيسي لمتحكم ESP32
#include <Arduino.h>
#include "lora_comms.h"
#include "valve_control.h"
#include "sensor_reading.h"
#include "power_management.h"

// تعريف المتغيرات
const int valvePins[] = {23, 22, 21};  // منافذ التحكم بالصمامات
const int sensorPins[] = {34, 35};     // منافذ الحساسات (A0, A1)

void setup() {
  Serial.begin(115200);
  
  // تهيئة الوحدات
  initLoRa();
  initValves(valvePins, 3);
  initSensors(sensorPins, 2);
  initPowerManagement();
  
  Serial.println("System Initialized");
}

void loop() {
  // قراءة الحساسات
  SensorData data = readSensors();
  
  // إرسال البيانات عبر LoRa
  sendLoRaData(data);
  
  // إدارة الطاقة
  managePower();
  
  delay(10000);  // انتظار 10 ثواني
}