# # config/influxdb_config.py
# import os
# from dotenv import load_dotenv

# load_dotenv()

# INFLUXDB_CONFIG = {
#     'HOST': os.getenv('INFLUX_HOST', 'localhost'),
#     'PORT': int(os.getenv('INFLUX_PORT', 8086)),
#     'DB_NAME': os.getenv('INFLUX_DB', 'irrigation_db'),
#     'USER': os.getenv('INFLUX_USER', 'admin'),
#     'PASSWORD': os.getenv('INFLUX_PASSWORD', 'password'),
#     'RETENTION': os.getenv('INFLUX_RETENTION', '52w')
# }

# config/influxdb_config.py
import os
from dotenv import load_dotenv

load_dotenv()

INFLUXDB_CONFIG = {
    'URL': os.getenv('INFLUXDB_URL', 'http://localhost:8086'),
    'TOKEN': os.getenv('INFLUXDB_TOKEN', 'nB7MMZyg2YRsY78o2jNfqs6aarTzjcbieYQwyV_EAaykx5LFoPmb64Elm1vqU2mMqW_wrqcosh2PcR-OfIrNhA=='),
    'ORG': os.getenv('INFLUXDB_ORG', 'YemenAgri'),
    'BUCKET': os.getenv('INFLUXDB_BUCKET', 'sensor_data'),
    'RETENTION': os.getenv('INFLUXDB_RETENTION', '52w')  # فترة الاحتفاظ بالبيانات
}