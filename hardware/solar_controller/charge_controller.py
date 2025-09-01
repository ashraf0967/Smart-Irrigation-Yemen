# charge_controller.py
import RPi.GPIO as GPIO
import time

class ChargeController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.solar_pin = 18
        self.battery_pin = 23
        GPIO.setup(self.solar_pin, GPIO.IN)
        GPIO.setup(self.battery_pin, GPIO.OUT)
        
    def manage_charging(self):
        while True:
            solar_voltage = self.read_solar()
            if solar_voltage > 5.0:  # جهد كافي للشحن
                GPIO.output(self.battery_pin, True)
            else:
                GPIO.output(self.battery_pin, False)
            time.sleep(60)
    
    def read_solar(self):
        # محاكاة قراءة الجهد (يتم استبدالها بقراءة حقيقية)
        return 6.2  # فولت