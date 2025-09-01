import requests
from config.alert_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SMS_API_KEY
from utils.logger import setup_logger
import json
from datetime import datetime

logger = setup_logger('alert_system')

class AlertSystem:
    def __init__(self):
        self.alert_history = []
    
    def send_telegram_alert(self, message):
        """إرسال تنبيه عبر Telegram"""
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                logger.info(f"تم إرسال تنبيه Telegram: {message}")
                return True
            else:
                logger.error(f"فشل إرسال Telegram: {response.text}")
                return False
        except Exception as e:
            logger.error(f"خطأ في إرسال Telegram: {str(e)}")
            return False
    
    def send_sms_alert(self, phone_number, message):
        """إرسال تنبيه عبر SMS"""
        url = "https://api.smsprovider.com/v1/send"
        headers = {'Authorization': f'Bearer {SMS_API_KEY}'}
        payload = {
            'to': phone_number,
            'message': message,
            'sender': 'IrrigationSys'
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                logger.info(f"تم إرسال SMS إلى {phone_number}")
                return True
            else:
                logger.error(f"فشل إرسال SMS: {response.text}")
                return False
        except Exception as e:
            logger.error(f"خطأ في إرسال SMS: {str(e)}")
            return False
    
    def check_system_alerts(self, system_data):
        """فحص حالة النظام وإرسال تنبيهات إذا لزم الأمر"""
        alerts = []
        
        # تنبيهات مستوى الماء
        if system_data['water']['percentage'] < 20:
            msg = f"⚠️ انخفاض مستوى الماء: {system_data['water']['percentage']}% فقط!"
            alerts.append(('water', msg))
        
        # تنبيهات رطوبة التربة
        if system_data['soil']['moisture'] < 25:
            msg = f"⚠️ انخفاض رطوبة التربة: {system_data['soil']['moisture']}%"
            alerts.append(('soil', msg))
        
        # تنبيهات البطارية
        if system_data['battery']['charge_percentage'] < 30:
            msg = f"🔋 بطارية منخفضة: {system_data['battery']['charge_percentage']}%"
            alerts.append(('battery', msg))
        
        # إرسال التنبيهات
        for alert_type, message in alerts:
            if not self.is_recent_alert(alert_type):
                self.send_telegram_alert(message)
                self.alert_history.append((alert_type, datetime.utcnow()))
        
        return alerts
    
    def is_recent_alert(self, alert_type, max_minutes=60):
        """التحقق مما إذا تم إرسال تنبيه مماثل مؤخرًا"""
        now = datetime.utcnow()
        for a_type, timestamp in self.alert_history:
            if a_type == alert_type and (now - timestamp).total_seconds() < max_minutes * 60:
                return True
        return False