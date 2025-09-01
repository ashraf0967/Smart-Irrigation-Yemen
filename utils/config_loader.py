# utils/config_loader.py
from config import mqtt_config, influxdb_config, lora_config, alert_config, sensor_config
from dotenv import load_dotenv

load_dotenv()

def get_config(config_name):
    """تحميل إعدادات التكوين"""
    configs = {
        'mqtt': mqtt_config.MQTT_CONFIG,
        'influxdb': influxdb_config.INFLUXDB_CONFIG,
        'lora': lora_config.LORA_CONFIG,
        'alert': alert_config.ALERT_CONFIG,
        'sensor': sensor_config.SENSOR_CONFIG
    }
    return configs.get(config_name, {})