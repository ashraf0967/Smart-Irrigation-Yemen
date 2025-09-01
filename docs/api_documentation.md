# توثيق واجهة برمجة التطبيقات (API)

## نقاط النهاية (Endpoints)

### 1. الحصول على بيانات الحساسات
`GET /api/sensor_data`

**الاستجابة:**
```json
{
  "soil": {
    "sensor_id": "soil_001",
    "moisture": 42.5,
    "timestamp": "2023-08-15T12:30:45Z"
  },
  "temperature": {
    "sensor_id": "dht_001",
    "value": 28.5,
    "timestamp": "2023-08-15T12:30:45Z"
  },
  "water": {
    "sensor_id": "tank_001",
    "level": 750.0,
    "capacity": 1000.0,
    "percentage": 75.0
  }
}