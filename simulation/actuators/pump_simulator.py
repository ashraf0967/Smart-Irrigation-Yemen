# simulation/actuators/pump_simulator.py
import random
from utils.logger import setup_logger

logger = setup_logger('pump_simulator')

class PumpSimulator:
    def __init__(self, pump_id):
        self.pump_id = pump_id
        self.status = "off"
        self.pressure = 0.0  # بار
        self.flow_rate = 0.0  # لتر/دقيقة
        
    def start_pump(self):
        """محاكاة تشغيل المضخة"""
        self.status = "on"
        self.pressure = random.uniform(2.5, 4.0)
        self.flow_rate = random.uniform(15.0, 30.0)
        logger.info(f"تشغيل المضخة {self.pump_id}")
        return True
        
    def stop_pump(self):
        """محاكاة إيقاف المضخة"""
        self.status = "off"
        self.pressure = 0.0
        self.flow_rate = 0.0
        logger.info(f"إيقاف المضخة {self.pump_id}")
        return True
        
    def get_status(self):
        """الحصول على حالة المضخة"""
        return {
            'pump_id': self.pump_id,
            'status': self.status,
            'pressure': self.pressure,
            'flow_rate': self.flow_rate
        }