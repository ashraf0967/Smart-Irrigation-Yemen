# config/mqtt_config.py
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_CONFIG = {
    'BROKER': os.getenv('MQTT_BROKER', 'test.mosquitto.org'),
    'PORT': int(os.getenv('MQTT_PORT', 1883)),
    'USER': os.getenv('MQTT_USER', ''),
    'PASSWORD': os.getenv('MQTT_PASSWORD', ''),
    'TOPIC_SENSOR': os.getenv('SENSOR_TOPIC', 'yemen_irrigation/sensor_data'),
    'TOPIC_CONTROL': os.getenv('CONTROL_TOPIC', 'yemen_irrigation/control_commands'),
    'KEEPALIVE': int(os.getenv('MQTT_KEEPALIVE', 60)),
}

MQTT_BROKER = MQTT_CONFIG['BROKER']
MQTT_PORT = MQTT_CONFIG['PORT']
SENSOR_TOPIC = MQTT_CONFIG['TOPIC_SENSOR']