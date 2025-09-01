# utils/data_validation.py
import re
from datetime import datetime

def validate_email(email):
    """التحقق من صحة البريد الإلكتروني"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """التحقق من صحة رقم الهاتف (التنسيق اليمني)"""
    pattern = r'^\+9677[0-9]{8}$'
    return re.match(pattern, phone) is not None

def validate_date(date_str, format='%Y-%m-%d'):
    """التحقق من صحة التاريخ"""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def validate_sensor_data(data):
    """التحقق من صحة بيانات الحساس"""
    required_fields = ['sensor_id', 'value', 'timestamp', 'sensor_type']
    if not all(field in data for field in required_fields):
        return False
        
    if not isinstance(data['value'], (int, float)):
        return False
        
    if not validate_date(data['timestamp'][:10]):
        return False
        
    return True