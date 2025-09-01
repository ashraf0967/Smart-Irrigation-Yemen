# import pytest
# from hardware.esp32.sensor_reading import setupSensors, readSensors

# def test_sensor_reading_integration():
#     """اختبار تكامل قراءة الحساسات (يتطلب عتاد فعلي)"""
#     # هذا الاختبار سيعمل فقط في بيئة العتاد الفعلي
#     try:
#         setupSensors()
#         readings = readSensors()
        
#         # التحقق من وجود القراءات
#         assert hasattr(readings, 'soilMoisture')
#         assert hasattr(readings, 'temperature')
#         assert hasattr(readings, 'humidity')
#         assert hasattr(readings, 'lightIntensity')
#         assert hasattr(readings, 'batteryVoltage')
        
#         # التحقق من النطاقات المعقولة
#         assert 0 <= readings.soilMoisture <= 100
#         assert -10 <= readings.temperature <= 50
#         assert 0 <= readings.humidity <= 100
#         assert 0 <= readings.lightIntensity <= 100000
#         assert 3.0 <= readings.batteryVoltage <= 4.2
        
#     except ImportError:
#         pytest.skip("يتطلب بيئة أجهزة فعلية")