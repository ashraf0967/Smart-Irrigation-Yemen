import os
import shutil
from datetime import datetime
from config.influxdb_config import INFLUX_DB, BACKUP_DIR
from utils.logger import setup_logger

logger = setup_logger('backup_system')

def create_backup():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    try:
        # إنشاء مجلد النسخ الاحتياطي إذا لم يكن موجوداً
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # اسم ملف النسخة الاحتياطية
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"{INFLUX_DB}_{timestamp}.bak")
        
        # نسخ ملف قاعدة البيانات
        db_file = f"{INFLUX_DB}.db"
        shutil.copy2(db_file, backup_file)
        
        logger.info(f"تم إنشاء نسخة احتياطية: {backup_file}")
        return backup_file
    except Exception as e:
        logger.error(f"فشل في إنشاء النسخة الاحتياطية: {str(e)}")
        return None

def restore_backup(backup_file):
    """استعادة قاعدة البيانات من نسخة احتياطية"""
    try:
        # التحقق من وجود ملف النسخة الاحتياطية
        if not os.path.exists(backup_file):
            logger.error(f"ملف النسخة الاحتياطية غير موجود: {backup_file}")
            return False
        
        # نسخ ملف النسخة الاحتياطية إلى موقع قاعدة البيانات
        db_file = f"{INFLUX_DB}.db"
        shutil.copy2(backup_file, db_file)
        
        logger.info(f"تم استعادة قاعدة البيانات من: {backup_file}")
        return True
    except Exception as e:
        logger.error(f"فشل في استعادة النسخة الاحتياطية: {str(e)}")
        return False

def auto_backup_schedule():
    """جدولة النسخ الاحتياطي التلقائي"""
    import schedule
    import time
    
    # نسخة احتياطية يومية في 2 صباحاً
    schedule.every().day.at("02:00").do(create_backup)
    
    logger.info("تم تفعيل الجدولة التلقائية للنسخ الاحتياطي")
    while True:
        schedule.run_pending()
        time.sleep(3600)  # التحقق كل ساعة