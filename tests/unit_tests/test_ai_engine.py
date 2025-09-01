import pytest
from ai_engine.irrigation_decision import IrrigationAI

def test_irrigation_decision():
    """اختبار قرارات الري"""
    ai = IrrigationAI()
    
    # حالة تحتاج ري
    assert ai.predict(25, 35, 30) == True
    
    # حالة لا تحتاج ري
    assert ai.predict(45, 25, 60) == False
    
    # حالة حافة
    assert ai.predict(30, 40, 35) == True

def test_irrigation_duration():
    """اختبار حساب مدة الري"""
    ai = IrrigationAI()
    
    # حالة عجز كبير
    assert ai.calculate_irrigation_duration(20) == 8  # (60-20)/5 = 8 دقائق
    
    # حالة عجز متوسط
    assert ai.calculate_irrigation_duration(35) == 5  # (60-35)/5 = 5 دقائق
    
    # حالة قريبة من المستوى المطلوب
    assert ai.calculate_irrigation_duration(55) == 5  # الحد الأدنى

def test_model_loading():
    """اختبار تحميل النموذج"""
    ai = IrrigationAI(model_path='ai_engine/models/test_model.pkl')
    # يجب أن يعود للقواعد الأساسية إذا لم يوجد النموذج
    assert ai.predict(25, 30, 40) == True