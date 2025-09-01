import schedule
import time
from datetime import datetime
from control_system.valve_controller import ValveController
from ai_engine.irrigation_decision import IrrigationAI
from utils.logger import setup_logger

logger = setup_logger('irrigation_scheduler')

class IrrigationScheduler:
    def __init__(self):
        self.valve_controller = ValveController()
        self.ai_engine = IrrigationAI()
        self.schedules = {}
    
    def add_schedule(self, valve_id, cron_expression, duration=None):
        """إضافة جدول ري جديد"""
        # التصحيح: منع الجدولة المكررة
        if valve_id in self.schedules:
            logger.warning(f"الصمام {valve_id} لديه جدول مسبقاً")
            return False
        self.schedules[valve_id] = {
            'cron': cron_expression,
            'duration': duration,
            'job': schedule.every()
        }
        
        # تحليل التعبير الزمني
        parts = cron_expression.split()
        if len(parts) == 5:
            # جدولة يومية
            self.schedules[valve_id]['job'].day.at(f"{parts[1]}:{parts[0]}").do(
                self.activate_valve, valve_id, duration
            )
        elif ' ' not in cron_expression:
            # فترات زمنية (كل X دقائق/ساعات)
            value, unit = int(cron_expression[:-1]), cron_expression[-1]
            if unit == 'm':
                self.schedules[valve_id]['job'].minutes(value).do(
                    self.activate_valve, valve_id, duration
                )
            elif unit == 'h':
                self.schedules[valve_id]['job'].hours(value).do(
                    self.activate_valve, valve_id, duration
                )
        
        logger.info(f"تمت جدولة الري للصمام {valve_id}: {cron_expression}")
    
    def activate_valve(self, valve_id, duration=None):
        """تفعيل صمام الري"""
        if duration is None:
            # استخدام الذكاء الاصطناعي لتحديد المدة
            current_data = self.get_current_sensor_data(valve_id)
            duration = self.ai_engine.calculate_irrigation_duration(
                current_data['soil_moisture']
            )
        
        self.valve_controller.activate_valve(valve_id, duration)
        logger.info(f"تم تفعيل الصمام {valve_id} لمدة {duration} دقائق")
    
    def get_current_sensor_data(self, valve_id):
        """الحصول على أحدث بيانات الحساسات (محاكاة)"""
        # في التطبيق الفعلي، سيتم استرجاع البيانات من قاعدة البيانات
        return {
            'soil_moisture': 35.0,
            'temperature': 28.5,
            'humidity': 65.0
        }
    
    def run(self):
        """تشغيل جدولة المهام"""
        logger.info("بدء تشغيل مجدول الري")
        while True:
            schedule.run_pending()
            time.sleep(1)