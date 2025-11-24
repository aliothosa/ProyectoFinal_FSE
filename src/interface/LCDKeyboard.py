from src.hardware.LCD import LCD
from src.hardware.MatrixKeyboard import MatrixKeyboard
from src.interface.Instructions import Tarea
from queue import Queue
from threading import Thread

import time

class LCDKeyboard(Thread):
    def __init__(self, q: Queue = Queue()):
        super().__init__()
        self.lcd = LCD()
        self.queue = Queue()
        self.queue_salida = q
        self.keyboard = MatrixKeyboard(self.queue)
        self.keyboard.start()

    def run(self):
        try:
            self.lcd.write("Instruccion:", line=0)
            while True:
                self.lcd.write(self.keyboard.get_string(), line=1)
                if not self.queue.empty():
                    self.parse_instruccion(self.queue.get())
                    self.lcd.write(" "*16, line=1)
                    self.lcd.clear()
                    self.lcd.write("Instruccion:\n" + self.keyboard.get_string(), line=0)
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.keyboard.stop()
            self.lcd.clear()
            self.lcd.write("Shutting down...", line=0)
            time.sleep(2)
            self.lcd.clear()

    def parse_instruccion(self, instruction: str):
        try:
            pieces = instruction.strip().upper().split()
            if len(pieces) < 3:
                self.lcd.write_rotate("Formato esperado: <A|B> HH MM (ej: 'A 12 30')", line=0)

            accion = pieces[0]
            if accion not in ["A", "B", "BB", "BA", "AA", "#"]:
                self.lcd.write_rotate("Accion desconocida, usa A o B", line=0)
                return
            
            hora = pieces[1]
            if not hora.isdigit() or not (0 <= int(hora) <= 23):
                self.lcd.write_rotate("Hora invalida, usa 00-23", line=0)
                return
            
            minuto = pieces[2]
            if not minuto.isdigit() or not (0 <= int(minuto) <= 59):
                self.lcd.write_rotate("Minuto invalido, usa 00-59", line=0)
                return

            match accion:
                case "A":
                    self.lcd.write_rotate(f"Dispensando comida a las {hora}:{minuto}", line=0)
                    self.queue_salida.put((Tarea.AGREGAR_TAREA, int(hora), int(minuto)))
                case "B":
                    self.lcd.write_rotate(f"Borrando instruccion a las {hora}:{minuto}", line=0)
                    self.queue_salida.put((Tarea.ELIMINAR_TAREA, int(hora), int(minuto)))
                case "BB":
                    self.lcd.write("Borrando hora", line=0)
                    self.queue_salida.put((Tarea.BORRAR_TAREAS_HORA, int(hora), 0))
                case "BA":
                    self.lcd.write("Borrando todas", line=0)
                    self.queue_salida.put((Tarea.BORRAR_TODAS_LAS_TAREAS, 0, 0))
                case "#":
                    self.lcd.write("Listando IDs", line=0)
                    self.queue_salida.put((Tarea.OBTENER_IDS_TAREAS, 0, 0))
                case "AA":
                    self.lcd.write("Dispensando comida", line=0)
                    self.queue_salida.put((Tarea.DISPENSAR_COMIDA, 0, 0))
                case _:
                    self.lcd.write("Instruccion no reconocida", line=0)

        except Exception as e:
            self.lcd.write("Instruccion no identificada", line=0)
            print("Error al parsear la instruccion:", e)

    def force_write(self, message: str, line: int = 0):
        self.lcd.write(message, line=line)

    def force_write_rotate(self, message: str, line: int = 0):
        self.lcd.write_rotate(message, line=line)
    
    def force_clear_line(self, line: int = 0):
        self.lcd.write(" " * 16, line=line)

if __name__ == "__main__":
    q = Queue()
    lcd_keyboard = LCDKeyboard(q)
    lcd_keyboard.start()