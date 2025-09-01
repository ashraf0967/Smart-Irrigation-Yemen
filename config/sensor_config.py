# معايرة الحساسات
SENSOR_CALIBRATION = {
    "soil_moisture": {
        "dry_value": 3500,    # القيمة عند التربة الجافة
        "wet_value": 1500     # القيمة عند التربة المشبعة
    },
    "temperature": {
        "offset": 0.5         # تعويض درجة الحرارة
    },
    "light_sensor": {
        "min_lux": 0,
        "max_lux": 100000
    },
    "battery_voltage": {
        "min_voltage": 3.0,
        "max_voltage": 4.2
    }
}

# إعدادات الحساسات الافتراضية
DEFAULT_SENSOR_VALUES = {
    "soil_moisture": 45.0,
    "temperature": 28.0,
    "humidity": 65.0,
    "light_intensity": 45000.0,
    "battery_percentage": 85.0
}