from datetime import datetime
from pydantic import BaseModel
from pydantic import validator

class SensorData(BaseModel):
    sensor_id: str
    value: float
    timestamp: datetime
    location: str
    sensor_type: str
    
    # التصحيح: إضافة تحقق من صحة البيانات
    @validator('value')
    def value_range(cls, v, field):
        if field.name == 'soil_moisture' and not (0 <= v <= 100):
            raise ValueError('رطوبة التربة يجب أن تكون بين 0 و 100')
        return v

class ValveStatus(BaseModel):
    valve_id: str
    status: str  # open/closed
    duration_left: float  # دقائق
    last_activation: datetime

class SystemStatus(BaseModel):
    timestamp: datetime
    active_valves: int
    water_consumption: float  # لتر
    energy_consumption: float  # واط/ساعة
    alerts: list[str]