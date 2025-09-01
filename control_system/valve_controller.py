# control_system/valve_controller.py
import time
from config.mqtt_config import MQTT_CONFIG
from paho.mqtt import client as mqtt
from utils.logger import setup_logger

logger = setup_logger('valve_controller')

class ValveController:
    def __init__(self):
        self.valves = {}  # {valve_id: {status, last_activation, duration}}
        self.mqtt_client = self.setup_mqtt()
        
    def setup_mqtt(self):
        """تهيئة عميل MQTT"""
        client = mqtt.Client()
        client.username_pw_set(MQTT_CONFIG['USER'], MQTT_CONFIG['PASSWORD'])
        client.connect(MQTT_CONFIG['BROKER'], MQTT_CONFIG['PORT'], MQTT_CONFIG['KEEPALIVE'])
        return client
        
    def activate_valve(self, valve_id, duration):
        """تفعيل صمام ري معين"""
        try:
            if valve_id not in self.valves:
                self.valves[valve_id] = {
                    'status': 'closed',
                    'last_activation': None,
                    'duration': 0
                }
                
            if self.valves[valve_id]['status'] == 'open':
                logger.warning(f"الصمام {valve_id} مفتوح بالفعل")
                return False
                
            # إرسال أمر التحكم عبر MQTT
            command = {
                'valve_id': valve_id,
                'action': 'open',
                'duration': duration
            }
            self.mqtt_client.publish(
                MQTT_CONFIG['TOPIC_CONTROL'], 
                str(command)
            )
            
            # تحديث الحالة المحلية
            self.valves[valve_id]['status'] = 'open'
            self.valves[valve_id]['last_activation'] = time.time()
            self.valves[valve_id]['duration'] = duration
            
            logger.info(f"تم تفعيل الصمام {valve_id} لمدة {duration} دقائق")
            return True

        except Exception as e:
            logger.error(f"فشل إرسال أمر MQTT: {str(e)}")
            self.reconnect_mqtt()
        
    def deactivate_valve(self, valve_id):
        """إلغاء تفعيل صمام ري"""
        if valve_id not in self.valves or self.valves[valve_id]['status'] == 'closed':
            logger.warning(f"الصمام {valve_id} مغلق بالفعل")
            return False
            
        # إرسال أمر التحكم عبر MQTT
        command = {
            'valve_id': valve_id,
            'action': 'close'
        }
        self.mqtt_client.publish(
            MQTT_CONFIG['TOPIC_CONTROL'], 
            str(command)
        )
        
        # تحديث الحالة المحلية
        self.valves[valve_id]['status'] = 'closed'
        self.valves[valve_id]['duration'] = 0
        
        logger.info(f"تم إيقاف الصمام {valve_id}")
        return True
        
    def update_valve_statuses(self):
        """تحديث حالة الصمامات (يجب استدعاؤها بانتظام)"""
        for valve_id, status in self.valves.items():
            if status['status'] == 'open':
                elapsed = (time.time() - status['last_activation']) / 60
                remaining = max(0, status['duration'] - elapsed)
                
                if remaining <= 0:
                    self.deactivate_valve(valve_id)
                else:
                    self.valves[valve_id]['duration'] = remaining
                    self.valves[valve_id]['last_activation'] = time.time()