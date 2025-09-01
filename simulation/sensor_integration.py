import time
import json
from paho.mqtt import client as mqtt
from config.mqtt_config import MQTT_BROKER, MQTT_PORT, SENSOR_TOPIC
from simulation.sensors.soil_moisture import SoilMoistureSimulator
from simulation.sensors.dht22_sensor import DHT22Simulator
from simulation.sensors.water_level import WaterLevelSimulator
from utils.logger import setup_logger

logger = setup_logger('sensor_integration')

# تهيئة الحساسات
soil_sensor = SoilMoistureSimulator("soil_001", "field_A", "sandy_loam")
dht_sensor = DHT22Simulator("dht_001", "field_A", elevation=1200)
water_sensor = WaterLevelSimulator("tank_001", 10000)

# عميل MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

def collect_and_send():
    """جمع البيانات من جميع الحساسات وإرسالها"""
    soil_data = soil_sensor.read_moisture()
    dht_data = dht_sensor.read()
    water_data = water_sensor.read()
    
    # حزمة البيانات المتكاملة
    sensor_package = {
        "location": "field_A",
        "soil": soil_data,
        "ambient": dht_data,
        "water": water_data,
        "system_status": "nominal",
        "timestamp": time.time()
    }
    
    # إرسال عبر MQTT
    mqtt_client.publish(SENSOR_TOPIC, json.dumps(sensor_package))
    logger.info("تم إرسال بيانات الحساسات")
    return sensor_package

# حلقة التشغيل الرئيسية
if __name__ == "__main__":
    while True:
        try:
            collect_and_send()
            time.sleep(300)  # إرسال كل 5 دقائق
        except Exception as e:
            logger.error(f"خطأ في جمع البيانات: {str(e)}")
            time.sleep(60)