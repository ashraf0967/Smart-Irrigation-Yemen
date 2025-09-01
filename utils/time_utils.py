from datetime import datetime, timedelta
import pytz

YEMEN_TZ = pytz.timezone('Asia/Aden')

def get_current_time():
    """الحصول على الوقت الحالي بتوقيت اليمن"""
    return datetime.now(YEMEN_TZ)

def format_time(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """تنسيق الوقت حسب التنسيق المطلوب"""
    return dt.strftime(format_str)

def parse_time(time_str, format_str='%Y-%m-%d %H:%M:%S'):
    """تحويل نص الوقت إلى كائن datetime"""
    return datetime.strptime(time_str, format_str).astimezone(YEMEN_TZ)

def add_minutes_to_time(dt, minutes):
    """إضافة دقائق إلى الوقت"""
    return dt + timedelta(minutes=minutes)

def time_until_next(minute, hour=None):
    """حساب الوقت المتبقي حتى الساعة والدقيقة المحددة"""
    now = get_current_time()
    
    if hour is not None:
        next_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_time < now:
            next_time += timedelta(days=1)
    else:
        next_time = now.replace(minute=minute, second=0, microsecond=0)
        if next_time < now:
            next_time += timedelta(hours=1)
    
    return next_time - now