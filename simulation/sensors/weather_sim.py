# simulation/sensors/weather_sim.py
import random
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger('weather_simulator')

class WeatherSimulator:
    def __init__(self, location="yemen_farm"):
        self.location = location
        self.weather_types = ['sunny', 'cloudy', 'rainy', 'stormy']
        self.current_weather = 'sunny'
        
    # التصحيح: إضافة تحقق من القيم الراجعة
    def simulate_weather(self):
        if not self.weather_types:
            raise ValueError("لم يتم تعريف أنواع الطقس")
       
    def simulate_weather(self):
        """محاكاة تغيرات الطقس بناء على الموسم والوقت"""
        now = datetime.utcnow()
        month = now.month
        
        # احتمالات الطقس حسب الشهر (اليمن)
        if 6 <= month <= 8:  # الصيف
            weights = [0.7, 0.2, 0.1, 0.0]  # مشمس غالباً
        elif 9 <= month <= 11:  # الخريف
            weights = [0.4, 0.3, 0.2, 0.1]  # أمطار متفرقة
        else:  # الشتاء والربيع
            weights = [0.5, 0.3, 0.15, 0.05]  # معتدل
            
        self.current_weather = random.choices(
            self.weather_types, 
            weights=weights, 
            k=1
        )[0]
        
        logger.info(f"حالة الطقس الحالية: {self.current_weather}")
        return {
            'location': self.location,
            'weather': self.current_weather,
            'timestamp': datetime.utcnow().isoformat()
        }