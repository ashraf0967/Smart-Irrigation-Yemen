#include <Arduino.h>
#include "sensor_reading.h"
#include <DHT.h>
#include <Adafruit_Sensor.h>

#define DHTPIN 4
#define DHTTYPE DHT22
#define SOIL_MOISTURE_PIN 34
#define LIGHT_SENSOR_PIN 35

DHT dht(DHTPIN, DHTTYPE);

void setupSensors() {
  dht.begin();
  pinMode(SOIL_MOISTURE_PIN, INPUT);
  pinMode(LIGHT_SENSOR_PIN, INPUT);
}

SensorReadings readSensors() {
  SensorReadings readings;
  
  // قراءة رطوبة التربة (0-4095)
  int soilRaw = analogRead(SOIL_MOISTURE_PIN);
  readings.soilMoisture = map(soilRaw, 1500, 3500, 0, 100); // معايرة للتربة اليمنية
  
  // قراءة درجة الحرارة والرطوبة الجوية
  readings.temperature = dht.readTemperature();
  readings.humidity = dht.readHumidity();
  
  // قراءة شدة الإضاءة
  int lightRaw = analogRead(LIGHT_SENSOR_PIN);
  readings.lightIntensity = map(lightRaw, 0, 4095, 0, 100000); // 0-100,000 لوكس
  
  // قراءة جهد البطارية
  readings.batteryVoltage = analogRead(36) * (3.3 / 4095.0) * 2.0; // قسمة الجهد
  
  return readings;
}