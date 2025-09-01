import random
from datetime import datetime
import math
from utils.logger import setup_logger

logger = setup_logger('light_sensor_sim')

class LightSensorSimulator:
    def __init__(self, sensor_id, location):
        self.sensor_id = sensor_id
        self.location = location
        self.lux_values = {
            'night': (0, 10),
            'dawn': (10, 1000),
            'day': (1000, 100000),
            'dusk': (10, 1000)
        }
    
    def read_light_intensity(self):
        now = datetime.utcnow()
        hour = now.hour + now.minute/60.0
        
        # تحديد الفترة الزمنية
        if 5 <= hour < 6:
            period = 'dawn'
        elif 6 <= hour < 18:
            period = 'day'
        elif 18 <= hour < 19:
            period = 'dusk'
        else:
            period = 'night'
        
        # توليد قيمة إضاءة واقعية
        min_lux, max_lux = self.lux_values[period]
        
        # تأثير الغيوم (عشوائي)
        cloud_factor = 0.3 if random.random() > 0.7 else 1.0
        
        # توليد قيمة الإضاءة مع تغييرات تدريجية
        base_value = (min_lux + max_lux) / 2
        if period == 'day':
            # نمط جيبي خلال النهار
            hour_offset = hour - 6
            sin_value = math.sin(math.pi * hour_offset / 12)
            lux_value = min_lux + (max_lux - min_lux) * sin_value
        else:
            lux_value = random.uniform(min_lux, max_lux)
        
        lux_value *= cloud_factor
        lux_value = max(0, min(100000, lux_value))
        
        logger.info(f"قراءة حساس الإضاءة {self.sensor_id}: {lux_value:.1f} لوكس")
        return {
            'sensor_id': self.sensor_id,
            'light_intensity': round(lux_value, 1),
            'period': period,
            'timestamp': datetime.utcnow().isoformat()
        }