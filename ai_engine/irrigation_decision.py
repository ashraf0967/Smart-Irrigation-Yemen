import joblib
import numpy as np
from datetime import datetime
from config.sensor_config import SENSOR_CALIBRATION
from utils.logger import setup_logger

logger = setup_logger('ai_engine')

class IrrigationAI:
    def __init__(self, model_path='ai_engine/models/irrigation_model.pkl'):
        try:
            self.model = joblib.load(model_path)
            logger.info("تم تحميل نموذج الذكاء الاصطناعي بنجاح")
        except FileNotFoundError:
            self.model = None
            logger.warning("لم يتم العثور على نموذج مدرب، استخدام القواعد الأساسية")
    
    def predict(self, soil_moisture, temperature, humidity, crop_type='wheat'):
        """توقع احتياجات الري باستخدام الذكاء الاصطناعي"""
        if self.model:
            # تحويل البيانات إلى مصفوفة للإدخال
            input_data = np.array([[soil_moisture, temperature, humidity]])
            prediction = self.model.predict(input_data)
            return bool(prediction[0])
        else:
            # استخدام القواعد الأساسية إذا لم يكن النموذج متوفرًا
            threshold = 30  # قيمة افتراضية للعتبة
            if soil_moisture < threshold:
                return True
            if temperature > 35 and humidity < 40 and soil_moisture < threshold + 5:
                return True
            return False
    
    def calculate_irrigation_duration(self, soil_moisture, target_moisture=60):
        """حساب مدة الري المطلوبة"""
        moisture_deficit = max(0, target_moisture - soil_moisture)
        # افتراض: 1 دقيقة ري لكل 5% عجز في الرطوبة
        return min(30, max(5, int(moisture_deficit / 5)))