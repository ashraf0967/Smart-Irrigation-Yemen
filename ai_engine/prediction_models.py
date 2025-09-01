import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from utils.logger import setup_logger

logger = setup_logger('prediction_models')

class IrrigationModel:
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = self.load_or_create_model(model_type)
        
    def load_or_create_model(self, model_type):
        model_path = f'ai_engine/models/{model_type}.pkl'
        try:
            model = joblib.load(model_path)
            logger.info(f"تم تحميل النموذج {model_type}")
            return model
        except FileNotFoundError:
            logger.info(f"إنشاء نموذج جديد: {model_type}")
            return self.create_model(model_type)
    
    def create_model(self, model_type):
        if model_type == 'random_forest':
            return RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_type == 'gradient_boosting':
            return GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
        elif model_type == 'neural_network':
            return MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=1000, random_state=42)
        else:
            raise ValueError(f"نوع النموذج غير معروف: {model_type}")
    
    def train(self, X, y):
        """تدريب النموذج على البيانات"""
        self.model.fit(X, y)
        joblib.dump(self.model, f'ai_engine/models/{self.model_type}.pkl')
        logger.info(f"تم تدريب وحفظ النموذج {self.model_type}")
    
    def predict_irrigation_duration(self, features):
        """توقع مدة الري المطلوبة"""
        prediction = self.model.predict([features])
        return max(5, min(30, int(prediction[0])))
    
    def predict_water_consumption(self, features):
        """توقع استهلاك المياه اليومي"""
        prediction = self.model.predict([features])
        return max(10, int(prediction[0]))