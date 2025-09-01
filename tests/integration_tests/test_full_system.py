import pytest
from main import main
from simulation.sensor_integration import collect_and_send
from database.influxdb_manager import InfluxDBManager

@pytest.fixture(scope="module")
def db_setup():
    """تهيئة قاعدة البيانات للاختبار"""
    db_manager = InfluxDBManager()
    yield db_manager
    # تنظيف بعد الاختبار (اختياري)

def test_full_integration(db_setup):
    """اختبار التكامل الكامل للنظام"""
    # 1. جمع بيانات الحساسات
    sensor_data = collect_and_send()
    
    # 2. التحقق من بنية البيانات
    assert 'soil' in sensor_data
    assert 'ambient' in sensor_data
    assert 'water' in sensor_data
    
    # 3. تخزين البيانات في قاعدة البيانات
    result = db_setup.write_sensor_data(sensor_data)
    assert result == True
    
    # 4. استرجاع البيانات للتأكد من التخزين
    query = f"SELECT * FROM soil_moisture WHERE sensor_id='{sensor_data['soil']['sensor_id']}'"
    data = db_setup.client.query(query)
    assert len(data) > 0