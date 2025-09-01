from flask import Flask, render_template, jsonify, request
from database.influxdb_manager import InfluxDBManager
from control_system.valve_controller import ValveController
from utils.logger import setup_logger
import json
from datetime import datetime
# Import or define alert_system
# Mock alert_system if import fails
class MockAlertSystem:
    def get_recent_alerts(self):
        return []

alert_system = MockAlertSystem()

app = Flask(__name__)
logger = setup_logger('web_interface')
db_manager = InfluxDBManager()
valve_controller = ValveController()

@app.route('/')
def dashboard():
    """لوحة التحكم الرئيسية"""
    return render_template('index.html')

@app.route('/api/sensor_data')
def get_sensor_data():
    """الحصول على أحدث بيانات الحساسات"""
    try:
        # استعلام قاعدة البيانات للحصول على أحدث القراءات
        query = """
        SELECT * FROM soil_moisture
        ORDER BY time DESC
        LIMIT 1
        """
        soil_data = db_manager.client.query(query).raw

        # استعلام بيانات درجة الحرارة
        temp_query = """
        SELECT * FROM temperature
        ORDER BY time DESC
        LIMIT 1
        """
        temp_data = db_manager.client.query(temp_query).raw

        # استعلام بيانات البطارية
        battery_query = """
        SELECT * FROM battery
        ORDER BY time DESC
        LIMIT 1
        """
        battery_data = db_manager.client.query(battery_query).raw

        return jsonify({
            'soil': soil_data,
            'temperature': temp_data,
            'battery': battery_data
        })
    except Exception as e:
        logger.error(f"خطأ في استرجاع بيانات الحساسات: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/control/valve', methods=['POST'])
def control_valve():
    """التحكم في صمام الري"""
    try:
        data = request.json
        valve_id = data.get('valve_id')
        action = data.get('action')
        duration = data.get('duration', 5)
        
        if action == 'on':
            valve_controller.activate_valve(valve_id, duration)
            return jsonify({'status': 'success', 'message': f'تم تشغيل الصمام لمدة {duration} دقائق'})
        elif action == 'off':
            valve_controller.deactivate_valve(valve_id)
            return jsonify({'status': 'success', 'message': 'تم إيقاف الصمام'})
        else:
            return jsonify({'status': 'error', 'message': 'إجراء غير صالح'}), 400
    except Exception as e:
        logger.error(f"خطأ في التحكم بالصمام: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/status')
def system_status():
    """حالة النظام العام"""
    return jsonify({
        'status': 'operational',
        'last_update': datetime.utcnow().isoformat(),
        'valves': valve_controller.get_valve_statuses(),
        'alerts': alert_system.get_recent_alerts()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)