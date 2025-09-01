// sensor_reading.h
#ifndef SENSOR_READING_H
#define SENSOR_READING_H

struct SensorData {
    float soilMoisture;
    float temperature;
    float humidity;
};

void initSensors(int pins[], int count);
SensorData readSensors();

#endif