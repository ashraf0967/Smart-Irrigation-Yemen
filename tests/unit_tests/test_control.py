import pytest
from control_system.valve_controller import ValveController
from control_system.alerts_system import AlertSystem

def test_valve_activation():
    """اختبار تفعيل وإيقاف الصمام"""
    controller = ValveController()
    
    # تفعيل الصمام 1 لمدة 5 دقائق
    controller.activate_valve(1, 5)
    assert controller.valves[1]['status'] == 'on'
    
    # إيقاف الصمام
    controller.deactivate_valve(1)
    assert controller.valves[1]['status'] == 'off'

def test_alert_system():
    """اختبار إرسال التنبيهات"""
    alert_system = AlertSystem()
    
    # إرسال تنبيه Telegram
    assert alert_system.send_telegram_alert("اختبار تنبيه") == True
    
    # إرسال تنبيه SMS (محاكاة)
    assert alert_system.send_sms_alert("+967711223344", "اختبار SMS") == True

def test_alert_thresholds():
    """اختبار عتبات التنبيه"""
    alert_system = AlertSystem()
    
    # بيانات نظام مع مستويات منخفضة
    system_data = {
        'water': {'percentage': 15},
        'soil': {'moisture': 20},
        'battery': {'charge_percentage': 25}
    }
    
    alerts = alert_system.check_system_alerts(system_data)
    assert len(alerts) == 3  # يجب إرسال 3 تنبيهات