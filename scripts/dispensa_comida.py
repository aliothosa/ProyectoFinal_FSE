import os
import sys

# Ruta absoluta a este archivo: .../ProyectoFinal_FSE/scripts/dispensa_comida.py
CURRENT_FILE = os.path.abspath(__file__)

# Proyecto raíz: .../ProyectoFinal_FSE
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))

# Carpeta src: .../ProyectoFinal_FSE/src
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

# Aseguramos que src/ esté en sys.path
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# 👇 OJO: a partir de aquí importas SIN "src."
from hardware.LoadCell import LoadCell
from hardware.Servo import Servo
from hardware.Buzzer import Buzzer
import time

OFFSET_LOAD_CELL = -464106.52  # Ajustar si se conoce un offset específico

def dispatch_food(objetivo_gramos: float, tolerancia_gramos: float = 5.0):
    load_cell = LoadCell(offset=OFFSET_LOAD_CELL)
    servo = Servo()
    buzzer = Buzzer() 

    print(f"Despachando comida para alcanzar {objetivo_gramos} g (±{tolerancia_gramos} g)...")
    
    try:
        
        peso_inicial = load_cell.get_weight()
        if peso_inicial >= objetivo_gramos:
            print("El peso inicial ya cumple o excede el objetivo. No se requiere despacho.")
            return
        servo.set_angle(165)  # Abrir compuerta
        time.sleep(1)  # Esperar a que la comida comience a fluir
        while True:
            peso_actual = load_cell.get_weight()
            print(f"Peso actual: {peso_actual:.2f} g")

            if peso_actual >= objetivo_gramos - tolerancia_gramos:
                print("Objetivo alcanzado.")
                break

            time.sleep(0.1)
        servo.set_angle(65)  # Cerrar compuerta
        time.sleep(1)
        print("Peso final:", load_cell.get_weight(), "g")

        buzzer.play_sound("C5", duration=3.0)
        time.sleep(1)

    except KeyboardInterrupt:
        print("Despacho interrumpido por el usuario.")

    finally:
        servo.set_angle(65)  # Cerrar compuerta
        print("Peso final:", load_cell.get_weight(), "g")

if __name__ == "__main__":
    dispatch_food(80)# Desp