from simulation.sensor_integration import collect_and_send
from database.influxdb_manager import InfluxDBManager
from ai_engine.irrigation_decision import IrrigationAI
from control_system.valve_controller import ValveController
from utils.logger import setup_logger
import time

logger = setup_logger('main')

def main():
    # تهيئة المكونات
    db_manager = InfluxDBManager()
    ai_engine = IrrigationAI()
    valve_controller = ValveController()
    
    logger.info("بدء تشغيل نظام الري الذكي")
    
    while True:
        try:
            # 1. جمع بيانات الحساسات
            sensor_data = collect_and_send()
            
            # 2. حفظ البيانات في قاعدة البيانات
            db_manager.write_sensor_data(sensor_data)
            
            # 3. اتخاذ قرار الري
            soil_data = sensor_data['soil']
            ambient_data = sensor_data['ambient']
            
            irrigation_needed = ai_engine.predict(
                soil_moisture=soil_data['moisture'],
                temperature=ambient_data['temperature'],
                humidity=ambient_data['humidity'],
                crop_type='wheat'
            )
            
            # 4. التحكم في الصمام
            if irrigation_needed:
                duration = ai_engine.calculate_irrigation_duration(soil_data['moisture'])
                valve_controller.activate_valve(duration)
            
            # 5. الانتظار للدورة التالية
            time.sleep(300)
            
        except KeyboardInterrupt:
            logger.info("إيقاف النظام بواسطة المستخدم")
            break
        except Exception as e:
            logger.error(f"خطأ غير متوقع: {str(e)}")
            time.sleep(60)

if __name__ == "__main__":
    main()