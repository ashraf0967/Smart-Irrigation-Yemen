# control_system/scheduler.py
import schedule
import time
from control_system.valve_controller import ValveController
from utils.logger import setup_logger

logger = setup_logger('scheduler')

class IrrigationScheduler:
    def __init__(self):
        self.controller = ValveController()
        self.schedules = {}
        
    def add_schedule(self, valve_id, cron_expression):
        """إضافة جدول ري جديد"""
        self.schedules[valve_id] = cron_expression
        
        # تحويل التعبير الزمني إلى مهمة مجدولة
        if cron_expression.startswith('every'):
            # مثال: "every_30m"
            parts = cron_expression.split('_')
            interval = int(parts[1][:-1])
            unit = parts[1][-1]
            
            if unit == 'm':
                schedule.every(interval).minutes.do(
                    self.activate_valve, valve_id
                )
            elif unit == 'h':
                schedule.every(interval).hours.do(
                    self.activate_valve, valve_id
                )
        else:
            # مثال: "15:30"
            hour, minute = map(int, cron_expression.split(':'))
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(
                self.activate_valve, valve_id
            )
            
        logger.info(f"تمت جدولة الري للصمام {valve_id}: {cron_expression}")
        
    def activate_valve(self, valve_id):
        """تفعيل صمام الري حسب الجدول"""
        # استخدام مدة افتراضية (يمكن التخصيص)
        self.controller.activate_valve(valve_id, 15)
        logger.info(f"تشغيل مجدول للصمام {valve_id}")
        
    def run(self):
        """تشغيل المجدول"""
        logger.info("بدء تشغيل مجدول الري")
        while True:
            schedule.run_pending()
            time.sleep(1)