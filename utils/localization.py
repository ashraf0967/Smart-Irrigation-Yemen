# قاموس الترجمات
ARABIC_TRANSLATIONS = {
    "system_status": "حالة النظام",
    "operational": "يعمل",
    "maintenance": "صيانة",
    "soil_moisture": "رطوبة التربة",
    "temperature": "درجة الحرارة",
    "humidity": "الرطوبة",
    "light_intensity": "شدة الإضاءة",
    "battery_level": "مستوى البطارية",
    "valve_status": "حالة الصمام",
    "on": "قيد التشغيل",
    "off": "متوقف",
    "irrigation_duration": "مدة الري",
    "minutes": "دقائق",
    "alert": "تنبيه",
    "low_soil_moisture": "رطوبة تربة منخفضة",
    "low_battery": "بطارية منخفضة",
    "high_temperature": "درجة حرارة مرتفعة",
    "settings": "الإعدادات",
    "save": "حفظ",
    "cancel": "إلغاء",
    "schedule": "جدولة",
    "daily": "يومي",
    "weekly": "أسبوعي",
    "custom": "مخصص"
}

def translate(key, lang='ar'):
    """ترجمة المفتاح إلى اللغة المطلوبة"""
    if lang == 'ar':
        return ARABIC_TRANSLATIONS.get(key, key)
    return key  # الإرجاع بالإنجليزية إذا لم تكن الترجمة متوفرة

def localize_numbers(number, lang='ar'):
    """توطين الأرقام حسب اللغة"""
    if lang == 'ar':
        arabic_numbers = '٠١٢٣٤٥٦٧٨٩'
        return ''.join(arabic_numbers[int(d)] for d in str(number))
    return str(number)