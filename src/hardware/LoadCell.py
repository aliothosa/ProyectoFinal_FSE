import time
import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DT = 17
SCK = 27

# ----- FACTOR DE CALIBRACIÓN -----
# Según tus mediciones:
#   Δ ≈ 71004 unidades para ~172 g
#   71004 / 172 ≈ 412.2 unidades por gramo
CALIBRACION = 412.0  # Ajustable según afinación fina


class LoadCell:
    def __init__(self, dt_pin=DT, sck_pin=SCK, calibration_factor=CALIBRACION, offset:int=None):
        self.hx = HX711(dout_pin=dt_pin, pd_sck_pin=sck_pin)
        self.calibration_factor = calibration_factor
        if offset:
            self.offset = offset
        else:
            self.offset = 0.0
            self.tare()

    def tare(self, samples=50):
        print("Taring load cell...")
        time.sleep(1)
        tara_muestras = self.hx.get_raw_data(samples)
        self.offset = sum(tara_muestras) / len(tara_muestras)
        print(f"Tare complete. Offset = {self.offset}")

    def get_weight(self, samples=10):
        lecturas = self.hx.get_raw_data(samples)
        promedio = sum(lecturas) / len(lecturas)
        neto_crudo = promedio - self.offset
        gramos = neto_crudo / self.calibration_factor
        return gramos