import time
import pigpio



class Servo:
    def __init__(self, servo_pin=23):
        self.servo_pin = servo_pin
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise SystemExit("No se pudo conectar con pigpiod. ¿Está corriendo el servicio?")

    def set_angle(self, angle: int):
        angle = max(0, min(180, angle))
        min_pulse = 500
        max_pulse = 2400
        pulse_width = int(min_pulse + (angle / 180.0) * (max_pulse - min_pulse))
        self.pi.set_servo_pulsewidth(self.servo_pin, pulse_width)

    def stop(self):
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
        self.pi.stop()