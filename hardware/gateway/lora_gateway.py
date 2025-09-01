# lora_gateway.py - استقبال بيانات لورا
from datetime import datetime
import serial
from data_processor import process_sensor_data

ser = serial.Serial('COM4', 115200)  # تغيير المنفذ حسب الجهاز

def receive_lora_data():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            try:
                sensor_data = parse_data(data)
                process_sensor_data(sensor_data)
            except Exception as e:
                print(f"Error processing data: {e}")

def parse_data(raw):
    parts = raw.split(',')
    data = {}
    for part in parts:
        key, value = part.split(':')
        data[key] = float(value)
    return {
        'timestamp': datetime.utcnow().isoformat(),
        'soil_moisture': data['Soil'],
        'temperature': data['Temp'],
        'humidity': data['Hum']
    }

if __name__ == "__main__":
    receive_lora_data()