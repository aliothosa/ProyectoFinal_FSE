import time
import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DT = 9
SCK = 11

hx = HX711(dout_pin=DT, pd_sck_pin=SCK)

print("Reset...")
hx.reset()

# --- TARA MANUAL ---
print("Quitar peso. Midiendo offset...")
time.sleep(1)

# obtenemos 30 muestras para la tara
tara_muestras = hx.get_raw_data(100)
offset = sum(tara_muestras) / len(tara_muestras)

print("Offset =", offset)

print("Leyendo valores...")
try:
    while True:
        lecturas = hx.get_raw_data(10)
        promedio = sum(lecturas) / len(lecturas)
        neto = promedio - offset

        print("Crudo:", promedio, " | Neto:", neto)
        neto = 0
        time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

class LoadCell:
    def __init__(self, dt_pin=9, sck_pin=11):
        self.hx = HX711(dout_pin=dt_pin, pd_sck_pin=sck_pin)
        self.hx.reset()
        self.offset = 0
        self.weight = 0

    def tare(self, samples=100):
        print("Taring... Remove any weight from the load cell.")
        time.sleep(1)
        tara_samples = self.hx.get_raw_data(samples)
        self.offset = sum(tara_samples) / len(tara_samples)
        print("Tare complete. Offset =", self.offset)

    def read_weight(self, samples=10):
        readings = self.hx.get_raw_data(samples)
        average = sum(readings) / len(readings)
        net_weight = average - self.offset
        return net_weight