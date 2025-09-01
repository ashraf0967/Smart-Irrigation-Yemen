import json
from utils.logger import setup_logger
from database.influxdb_manager import InfluxDBManager
from paho.mqtt import client as mqtt
from config.mqtt_config import MQTT_CONFIG

logger = setup_logger('data_processor')

class DataProcessor:
    def __init__(self):
        self.db_manager = InfluxDBManager()
    
    def process_sensor_data(self, data):
        client = mqtt.Client()
        client.connect(MQTT_CONFIG['BROKER'], MQTT_CONFIG['PORT'])
        client.publish(MQTT_CONFIG['TOPIC_SENSOR'], str(data))
    
    def process_packet(self, packet):
        try:
            data = json.loads(packet)
            
            # التحقق من صحة الحزمة
            required_fields = ['node_id', 'soil', 'temp', 'hum', 'light', 'battery']
            if not all(field in data for field in required_fields):
                logger.warning("حزمة بيانات غير صالحة")
                return False
            
            # إنشاء نقاط البيانات للتخزين
            influx_points = [
                {
                    "measurement": "soil_moisture",
                    "tags": {"node_id": data['node_id']},
                    "fields": {"value": data['soil']}
                },
                {
                    "measurement": "temperature",
                    "tags": {"node_id": data['node_id']},
                    "fields": {"value": data['temp']}
                },
                {
                    "measurement": "humidity",
                    "tags": {"node_id": data['node_id']},
                    "fields": {"value": data['hum']}
                },
                {
                    "measurement": "light_intensity",
                    "tags": {"node_id": data['node_id']},
                    "fields": {"value": data['light']}
                },
                {
                    "measurement": "battery",
                    "tags": {"node_id": data['node_id']},
                    "fields": {
                        "voltage": data['battery']['voltage'],
                        "percentage": data['battery']['percentage']
                    }
                }
            ]
            
            # تخزين البيانات
            self.db_manager.write_points(influx_points)
            logger.info(f"تم معالجة وتخزين بيانات العقدة {data['node_id']}")
            return True
            
        except json.JSONDecodeError:
            logger.error("خطأ في فك تشفير JSON")
            return False
        except Exception as e:
            logger.error(f"خطأ في معالجة البيانات: {str(e)}")
            return False