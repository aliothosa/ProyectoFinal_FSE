from queue import Queue
import RPi.GPIO as GPIO
from src.interface.LCDKeyboard import LCDKeyboard
from src.functions.Cron import despachar_tarea
import time
from threading import Thread    

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class ListenerBoton(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.time_since_last_instruction = 0.0
        self.interface : LCDKeyboard | None = None
        self.q : Queue | None = None
        self.engage = False

    def run(self):
        while True:
            if GPIO.input(18) == GPIO.LOW:
                print("Botón presionado")
                self.engage = True
                self.start_operations()
                time.sleep(0.3)  # anti-rebote

            if not self.engage:
                time.sleep(1)
            
    def start_operations(self):
        self.q = Queue()
        self.interface = LCDKeyboard(q=self.q)
        self.interface.start()
        t_inicial = time.perf_counter()
        self.interface.force_write("Bienvenido", line=0)

        while self.engage:
            try:
                if not self.q.empty():
                    instruccion, hora, minuto = self.q.get()
                    mensaje = despachar_tarea(instruccion, f"{hora}", f"{minuto}")
                    if mensaje:
                        self.interface.force_write_rotate(mensaje, line=0)

                time_since_last_instruction = time.perf_counter() - t_inicial
                
                if time_since_last_instruction > 120.0:
                    self.interface.force_write_rotate("Tiempo de inactividad excedido", line=0)
                    self.engage = False
                    break

            except Exception as e:
                print("Error en el loop principal:", e)
                self.engage = False
                break

if __name__ == "__main__":
    try:
        main = ListenerBoton()
        main.start()
        main.join()
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        print("Error en la aplicación principal:", e)
        GPIO.cleanup()