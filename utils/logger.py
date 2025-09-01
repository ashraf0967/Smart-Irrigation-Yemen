# utils/logger.py
import logging
import sys
from datetime import datetime

def setup_logger(name, log_file=None, level=logging.INFO):
    """تهيئة نظام التسجيل"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # تنسيق الرسائل
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # معالج وحدة التحكم
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # معالج ملفات السجل (إذا تم توفيره)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger