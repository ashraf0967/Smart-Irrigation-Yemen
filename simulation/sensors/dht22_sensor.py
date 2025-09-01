import random
from datetime import datetime, timedelta
import math
from utils.logger import setup_logger

logger = setup_logger('dht_simulator')

class DHT22Simulator:
    def __init__(self, sensor_id, location, elevation=0):
        self.sensor_id = sensor_id
        self.location = location
        self.elevation = elevation
        self.last_temp = 25.0
        self.last_humidity = 60.0
        
    def read(self):
        """محاكاة قراءات درجة الحرارة والرطوبة"""
        # نمط يومي: أكثر برودة في الليل، أكثر دفئًا خلال النهار
        now = datetime.utcnow()
        hour = now.hour + now.minute/60.0
        
        # معادلة درجة الحرارة مع نمط جيبي
        temp_base = 20.0 + 10.0 * math.sin(math.pi * (hour - 6) / 12.0)
        temp = temp_base - (self.elevation * 0.0065)  # تأثير الارتفاع
        
        # إضافة تقلب عشوائي
        temp += random.uniform(-1.5, 1.5)
        
        # نمط الرطوبة (عكس درجة الحرارة)
        humidity_base = 70.0 - 30.0 * math.sin(math.pi * (hour - 6) / 12.0)
        humidity = max(15.0, min(95.0, humidity_base + random.uniform(-5, 5)))
        
        # تسجيل القيم للاستخدام في القراءة التالية
        self.last_temp = temp
        self.last_humidity = humidity
        
        logger.info(f"قراءة DHT22 {self.sensor_id}: {temp:.1f}°C, {humidity:.1f}%")
        return {
            'sensor_id': self.sensor_id,
            'temperature': round(temp, 1),
            'humidity': round(humidity, 1),
            'timestamp': datetime.utcnow().isoformat()
        }