# dashboard/notification_system/sms_integration.py
import requests
from config.alert_config import SMS_API_KEY, ALERT_PHONE_NUMBERS
from utils.logger import setup_logger

logger = setup_logger('sms_integration')

def send_sms_alert(message):
    """إرسال تنبيه عبر SMS"""
    url = "https://api.smsprovider.com/v1/send"
    headers = {
        'Authorization': f'Bearer {SMS_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    for phone in ALERT_PHONE_NUMBERS:
        payload = {
            'to': phone,
            'message': message,
            'sender': 'IrrigationSys'
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                logger.info(f"تم إرسال SMS إلى {phone}")
            else:
                logger.error(f"خطأ في إرسال SMS: {response.text}")
        except Exception as e:
            logger.error(f"خطأ في الاتصال بمزود SMS: {str(e)}")