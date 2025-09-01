import random
from datetime import datetime, timedelta
from utils.logger import setup_logger

logger = setup_logger('battery_sim')

class BatterySimulator:
    def __init__(self, sensor_id, capacity=3400):
        self.sensor_id = sensor_id
        self.capacity = capacity  # السعة بالمللي أمبير ساعة
        self.current_charge = capacity * 0.85  # البدء بـ 85%
        self.last_update = datetime.utcnow()
        self.consumption_rates = {
            'active': 80,    # mA في وضع النشاط
            'transmit': 120, # mA أثناء الإرسال
            'sleep': 0.005   # mA في وضع السكون
        }
    
    def update_charge(self, state, duration_hours):
        """تحديث شحن البطارية بناء على حالة النظام"""
        consumption = self.consumption_rates[state] * duration_hours
        self.current_charge -= consumption
        self.current_charge = max(0, min(self.capacity, self.current_charge))
        return self.current_charge
    
    def simulate_solar_charge(self, light_intensity):
        """محاكاة شحن الطاقة الشمسية"""
        # افتراض: 20W solar panel efficiency
        charge_rate = light_intensity / 1000 * 0.15  # 0.15A لكل 1000 لوكس
        self.current_charge = min(self.capacity, self.current_charge + charge_rate)
        return charge_rate
    
    def read(self, system_state, light_data):
        """قراءة حالة البطارية"""
        now = datetime.utcnow()
        hours_passed = (now - self.last_update).total_seconds() / 3600
        self.last_update = now
        
        # تحديث استهلاك الطاقة
        self.update_charge(system_state, hours_passed)
        
        # محاكاة الشحن الشمسي إذا كانت هناك إضاءة كافية
        if light_data['light_intensity'] > 10000:
            charge_rate = self.simulate_solar_charge(light_data['light_intensity'])
            logger.info(f"شحن البطارية {self.sensor_id}: +{charge_rate:.2f}mA")
        
        charge_percentage = (self.current_charge / self.capacity) * 100
        voltage = 3.0 + (self.current_charge / self.capacity) * 1.2
        
        logger.info(f"حالة البطارية {self.sensor_id}: {charge_percentage:.1f}%")
        return {
            'sensor_id': self.sensor_id,
            'charge_percentage': round(charge_percentage, 1),
            'voltage': round(voltage, 2),
            'capacity': self.capacity,
            'timestamp': datetime.utcnow().isoformat()
        }