import random
import time
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger('soil_simulator')

class SoilMoistureSimulator:
    def __init__(self, sensor_id, location, soil_type="clay"):
        self.sensor_id = sensor_id
        self.location = location
        self.soil_type = soil_type
        self.base_moisture = 35.0 if soil_type == "clay" else 25.0
        
    def read_moisture(self):
        """محاكاة قراءة رطوبة التربة مع تأثيرات بيئية"""
        # تأثير الوقت من اليوم (الرطوبة أعلى في الصباح)
        hour = datetime.now().hour
        time_factor = 1.2 if 5 <= hour <= 8 else 1.0
        
        # تأثير عشوائي + اتجاه طويل المدى
        base_value = self.base_moisture * time_factor
        noise = random.gauss(0, 1.5)
        trend = -0.05 if datetime.now().hour > 10 else 0.02
        
        moisture = max(10.0, min(95.0, base_value + noise + trend))
        
        logger.info(f"قراءة حساس التربة {self.sensor_id}: {moisture:.1f}%")
        return {
            'sensor_id': self.sensor_id,
            'moisture': round(moisture, 1),
            'location': self.location,
            'timestamp': datetime.utcnow().isoformat(),
            'soil_type': self.soil_type
        }