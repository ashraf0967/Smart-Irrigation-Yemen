# إعدادات نظام التنبيهات
TELEGRAM_BOT_TOKEN = "759945559:AAEIahtIy_GgGs1o"
TELEGRAM_CHAT_ID = "5784555553"
SMS_API_KEY = "sk_test_EXAMPLE123"
ALERT_PHONE_NUMBERS = ["+967712345678", "+967798765432"]

# عتبات التنبيه
ALERT_THRESHOLDS = {
    "soil_moisture": 25.0,    # أقل من 25% رطوبة تربة
    "water_level": 20.0,      # أقل من 20% مستوى ماء
    "battery": 30.0,          # أقل من 30% شحن بطارية
    "temperature": 40.0       # أعلى من 40°C درجة حرارة
}

# فترات التكرار للتنبيهات (دقائق)
ALERT_REPEAT_INTERVALS = {
    "soil_moisture": 120,
    "water_level": 240,
    "battery": 60,
    "temperature": 180
}