from src.hardware.LoadCell import LoadCell
from src.hardware.Servo import Servo
import time


def dispatch_food(objetivo_gramos: float, tolerancia_gramos: float = 5.0):
    load_cell = LoadCell()
    load_cell.tare()
    servo = Servo()

    print(f"Despachando comida para alcanzar {objetivo_gramos} g (±{tolerancia_gramos} g)...")
    
    try:
        peso_inicial = load_cell.get_weight()
        if peso_inicial >= objetivo_gramos:
            print("El peso inicial ya cumple o excede el objetivo. No se requiere despacho.")
            return
        servo.set_angle(90)  # Abrir compuerta
        time.sleep(1)  # Esperar a que la comida comience a fluir
        while True:
            peso_actual = load_cell.get_weight()
            print(f"Peso actual: {peso_actual:.2f} g")

            if peso_actual >= objetivo_gramos - tolerancia_gramos:
                print("Objetivo alcanzado.")
                break

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Despacho interrumpido por el usuario.")

    finally:
        print("Peso final:", load_cell.get_weight(), "g")

if __name__ == "__main__":
    dispatch_food(200)# Desp