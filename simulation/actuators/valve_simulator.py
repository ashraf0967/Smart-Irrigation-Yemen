# simulation/actuators/valve_simulator.py
import time
from utils.logger import setup_logger

logger = setup_logger('valve_simulator')

class ValveSimulator:
    def __init__(self, valve_id):
        self.valve_id = valve_id
        self.status = "closed"
        self.last_activation = None
        self.duration_left = 0
        
    # التصحيح: معالجة القيم السالبة
    def update(self):
        if self.status == "open" and self.duration_left > 0:
            elapsed = max(0, (time.time() - self.last_activation))  # منع القيم السالبة
        
    def open_valve(self, duration):
        """محاكاة فتح صمام الري"""
        if self.status == "open":
            logger.warning(f"الصمام {self.valve_id} مفتوح بالفعل")
            return False
            
        self.status = "open"
        self.last_activation = time.time()
        self.duration_left = duration
        logger.info(f"فتح الصمام {self.valve_id} لمدة {duration} دقائق")
        return True
        
    def close_valve(self):
        """محاكاة إغلاق صمام الري"""
        if self.status == "closed":
            logger.warning(f"الصمام {self.valve_id} مغلق بالفعل")
            return False
            
        self.status = "closed"
        self.duration_left = 0
        logger.info(f"إغلاق الصمام {self.valve_id}")
        return True
        
    def update(self):
        """تحديث حالة الصمام (يجب استدعاؤها بانتظام)"""
        if self.status == "open" and self.duration_left > 0:
            elapsed = (time.time() - self.last_activation) / 60  # تحويل إلى دقائق
            self.duration_left = max(0, self.duration_left - elapsed)
            self.last_activation = time.time()
            
            if self.duration_left <= 0:
                self.close_valve()
                
        return {
            'valve_id': self.valve_id,
            'status': self.status,
            'duration_left': self.duration_left
        }