import random
from datetime import datetime, timedelta
from utils.logger import setup_logger

logger = setup_logger('water_level_sim')

class WaterLevelSimulator:
    def __init__(self, sensor_id, capacity=5000):
        self.sensor_id = sensor_id
        self.capacity = capacity  # السعة الكاملة باللتر
        self.current_level = capacity * 0.8  # البدء بـ 80% من السعة
        self.last_update = datetime.utcnow()
        
    def update_level(self, consumption_rate):
        """تحديد مستوى الماء بناء على معدل الاستهلاك"""
        now = datetime.utcnow()
        hours_passed = (now - self.last_update).total_seconds() / 3600
        self.last_update = now
        
        # استهلاك الماء + تبخر
        consumption = consumption_rate * hours_passed
        evaporation = 0.02 * self.current_level * hours_passed
        
        self.current_level -= (consumption + evaporation)
        self.current_level = max(0, self.current_level)
        
        # محاكاة إعادة التعبئة العشوائية
        if random.random() < 0.05 and self.current_level < self.capacity * 0.3:
            refill = random.uniform(self.capacity * 0.2, self.capacity * 0.5)
            self.current_level = min(self.capacity, self.current_level + refill)
            logger.info(f"إعادة تعبئة الخزان {self.sensor_id}: +{refill:.1f}L")
        
        return self.current_level
    
    def read(self, consumption_rate=50):
        """قراءة مستوى الماء"""
        level = self.update_level(consumption_rate)
        percentage = (level / self.capacity) * 100
        
        logger.info(f"مستوى الماء {self.sensor_id}: {percentage:.1f}%")
        return {
            'sensor_id': self.sensor_id,
            'water_level': round(level, 1),
            'capacity': self.capacity,
            'percentage': round(percentage, 1),
            'timestamp': datetime.utcnow().isoformat()
        }