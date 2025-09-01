# dashboard/notification_system/telegram_bot.py
import requests
from config.alert_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import setup_logger

logger = setup_logger('telegram_bot')

def send_telegram_alert(message):
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
            logger.info("تم إرسال تنبيه Telegram")
            return True
        else:
            logger.error(f"خطأ في إرسال Telegram: {response.text}")
            return False
    except Exception as e:
        logger.error(f"خطأ في الاتصال بـ Telegram: {str(e)}")
        return False