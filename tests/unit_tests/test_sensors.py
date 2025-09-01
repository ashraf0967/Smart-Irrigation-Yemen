import pytest
from simulation.sensors.soil_moisture import SoilMoistureSimulator
from simulation.sensors.dht22_sensor import DHT22Simulator
from simulation.sensors.water_level import WaterLevelSimulator

def test_soil_moisture_range():
    """التحقق من بقاء رطوبة التربة ضمن النطاق المعقول"""
    sensor = SoilMoistureSimulator("test_sensor", "test_loc", "sandy")
    data = sensor.read_moisture()
    assert 0 <= data['moisture'] <= 100

def test_dht22_values():
    """التحقق من قيم درجة الحرارة والرطوبة"""
    sensor = DHT22Simulator("test_sensor", "test_loc")
    data = sensor.read()
    assert -40 <= data['temperature'] <= 80
    assert 0 <= data['humidity'] <= 100

def test_water_level_consumption():
    """اختبار استهلاك مستوى الماء"""
    sensor = WaterLevelSimulator("test_sensor", 1000)
    initial_level = sensor.current_level
    sensor.read(consumption_rate=100)  # استهلاك 100 لتر/ساعة
    assert sensor.current_level < initial_level

def test_water_level_refill():
    """اختبار إعادة تعبئة الخزان"""
    sensor = WaterLevelSimulator("test_sensor", 1000)
    sensor.current_level = 200  # مستوى منخفض
    sensor.read(consumption_rate=10)
    # هناك احتمال 5% لإعادة التعبئة
    # سنجبر إعادة التعبئة للاختبار
    sensor.current_level = 200
    sensor.read(consumption_rate=10)
    assert sensor.current_level > 200