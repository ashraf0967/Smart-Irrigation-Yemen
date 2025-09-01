# from influxdb import InfluxDBClient
# from config.influxdb_config import DB_HOST, DB_PORT, DB_NAME, USER, PASSWORD
# from utils.logger import setup_logger
# import json

# logger = setup_logger('influxdb_manager')

# class InfluxDBManager:
#     def __init__(self):
#         self.client = InfluxDBClient(
#             host=DB_HOST,
#             port=DB_PORT,
#             username=USER,
#             password=PASSWORD,
#             database=DB_NAME
#         )
#         self.create_database()
        
#     def create_database(self):
#         """إنشاء قاعدة البيانات إذا لم تكن موجودة"""
#         databases = self.client.get_list_database()
#         if not any(db['name'] == DB_NAME for db in databases):
#             self.client.create_database(DB_NAME)
#             logger.info(f"تم إنشاء قاعدة البيانات {DB_NAME}")
            
#         self.client.switch_database(DB_NAME)
#         logger.info(f"تم التوصيل بقاعدة البيانات {DB_NAME}")
    
#     def write_sensor_data(self, data):
#         """كتابة بيانات الحساس إلى InfluxDB"""
#         json_body = []
        
#         # بيانات التربة
#         json_body.append({
#             "measurement": "soil_moisture",
#             "tags": {
#                 "sensor_id": data['soil']['sensor_id'],
#                 "location": data['location'],
#                 "soil_type": data['soil']['soil_type']
#             },
#             "time": data['soil']['timestamp'],
#             "fields": {
#                 "value": data['soil']['moisture']
#             }
#         })
        
#         # بيانات درجة الحرارة
#         json_body.append({
#             "measurement": "temperature",
#             "tags": {
#                 "sensor_id": data['ambient']['sensor_id'],
#                 "location": data['location']
#             },
#             "time": data['ambient']['timestamp'],
#             "fields": {
#                 "value": data['ambient']['temperature']
#             }
#         })
        
#         # بيانات الرطوبة الجوية
#         json_body.append({
#             "measurement": "humidity",
#             "tags": {
#                 "sensor_id": data['ambient']['sensor_id'],
#                 "location": data['location']
#             },
#             "time": data['ambient']['timestamp'],
#             "fields": {
#                 "value": data['ambient']['humidity']
#             }
#         })
        
#         # بيانات مستوى الماء
#         json_body.append({
#             "measurement": "water_level",
#             "tags": {
#                 "sensor_id": data['water']['sensor_id'],
#                 "location": data['location']
#             },
#             "time": data['water']['timestamp'],
#             "fields": {
#                 "value": data['water']['percentage'],
#                 "volume": data['water']['water_level'],
#                 "capacity": data['water']['capacity']
#             }
#         })
        
#         # كتابة البيانات
#         try:
#             self.client.write_points(json_body)
#             logger.info("تم حفظ بيانات الحساسات في قاعدة البيانات")
#             return True
#         except Exception as e:
#             logger.error(f"خطأ في كتابة البيانات: {str(e)}")
#             return False

# database/influxdb_manager.py
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from config.influxdb_config import INFLUXDB_CONFIG
from utils.logger import setup_logger

logger = setup_logger('influxdb_manager')

class InfluxDBManager:
    def __init__(self):
        self.client = InfluxDBClient(
            url=INFLUXDB_CONFIG['URL'],
            token=INFLUXDB_CONFIG['TOKEN'],
            org=INFLUXDB_CONFIG['ORG']
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.bucket = INFLUXDB_CONFIG['BUCKET']
        logger.info("تم الاتصال بـ InfluxDB 2.x بنجاح")
    
    def write_sensor_data(self, data):
        """كتابة بيانات الحساس إلى InfluxDB"""
        from influxdb_client import Point
        try:
            # إنشاء نقطة بيانات لرطوبة التربة
            soil_point = Point("soil_moisture") \
                .tag("sensor_id", data['soil']['sensor_id']) \
                .tag("location", data['location']) \
                .field("value", data['soil']['moisture']) \
                .time(data['soil']['timestamp'])
            
            # نقطة لدرجة الحرارة
            temp_point = Point("temperature") \
                .tag("sensor_id", data['ambient']['sensor_id']) \
                .tag("location", data['location']) \
                .field("value", data['ambient']['temperature']) \
                .time(data['ambient']['timestamp'])
            
            # نقطة للرطوبة الجوية
            humidity_point = Point("humidity") \
                .tag("sensor_id", data['ambient']['sensor_id']) \
                .tag("location", data['location']) \
                .field("value", data['ambient']['humidity']) \
                .time(data['ambient']['timestamp'])
            
            # نقطة لمستوى الماء
            water_point = Point("water_level") \
                .tag("sensor_id", data['water']['sensor_id']) \
                .tag("location", data['location']) \
                .field("value", data['water']['percentage']) \
                .field("volume", data['water']['water_level']) \
                .time(data['water']['timestamp'])
            
            # الكتابة
            self.write_api.write(bucket=self.bucket, record=[soil_point, temp_point, humidity_point, water_point])
            logger.info("تم حفظ بيانات الحساسات في InfluxDB 2.x")
            return True
        except Exception as e:
            logger.error(f"خطأ في كتابة البيانات: {str(e)}")
            return False