import time
import pigpio

SERVO_PIN = 18  # GPIO para la señal del SG90

pi = pigpio.pi()
if not pi.connected:
    raise SystemExit("No se pudo conectar con pigpiod. ¿Está corriendo el servicio?")

# Conversión de ángulo (0-180) a ancho de pulso para SG90
def set_angle(angle):
    # limita ángulo a 0-180 por si acaso
    angle = max(0, min(180, angle))
    # ajusta estos valores si tu servo zumba en los extremos
    min_pulse = 500   # µs  (≈ 0 grados)
    max_pulse = 2400  # µs  (≈ 180 grados)

    pulse_width = int(min_pulse + (angle / 180.0) * (max_pulse - min_pulse))
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

try:

    print("Centro (90°)")
    set_angle(90)
    time.sleep(1)

    print("Min (0°)")
    set_angle(0)
    time.sleep(1)

    print("Max (180°)")
    set_angle(180)
    time.sleep(1)

    print("Barrido...")
    for ang in range(0, 181, 10):
        set_angle(ang)
        time.sleep(0.2)
    for ang in range(180, -1, -10):
        set_angle(ang)
        time.sleep(0.2)

except KeyboardInterrupt:
    pass
finally:
    # apagar el servo para que no quede haciendo fuerza
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    pi.stop()

class Servo:
    def __init__(self, servo_pin=16)
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