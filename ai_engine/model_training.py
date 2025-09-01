# ai_engine/model_training.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
from utils.logger import setup_logger
import os

logger = setup_logger('model_training')

def train_irrigation_model(data_path='ai_engine/data/irrigation_data.csv'):
    """تدريب نموذج للتنبؤ بمدة الري المطلوبة"""
    # التصحيح: معالجة الملفات غير الموجودة
    if not os.path.exists(data_path):
        logger.error(f"ملف البيانات غير موجود: {data_path}")
        return None, 0
    try:
        # تحميل البيانات
        data = pd.read_csv(data_path)
        logger.info(f"تم تحميل بيانات التدريب: {len(data)} صف")
        
        # تحضير البيانات
        X = data[['soil_moisture', 'temperature', 'humidity', 'crop_type_code']]
        y = data['irrigation_duration']
        
        # تقسيم البيانات
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # تدريب النموذج
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # تقييم النموذج
        score = model.score(X_test, y_test)
        logger.info(f"دقة النموذج: {score:.2f}")
        
        # حفظ النموذج
        joblib.dump(model, 'ai_engine/models/irrigation_model.pkl')
        logger.info("تم حفظ النموذج المدرب")
        
        return model, score
    except Exception as e:
        logger.error(f"خطأ في تدريب النموذج: {str(e)}")
        return None, 0