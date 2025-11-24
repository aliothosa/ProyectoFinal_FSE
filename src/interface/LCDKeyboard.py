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
        self.queue_entrada = Queue()
        self.keyboard = MatrixKeyboard(self.queue)
        self.keyboard.start()
        self.active = True

    def run(self):
        try:
            while self.active:
                if not self.queue_entrada.empty():
                    message, line, rotate = self.queue_entrada.get()
                    if rotate:
                        self.lcd.write_rotate(message, line=line)
                    else:
                        self.lcd.write(message, line=line)

                self.lcd.write(self.keyboard.get_string(), line=1)
                if not self.queue.empty():
                    self.parse_instruccion(self.queue.get())
                    self.lcd.write(" "*16, line=1)
                    self.lcd.clear()
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
            if len(pieces) == 1 and pieces[0] in ['BA', '#', 'AA']:
                match pieces[0]:
                    case "BA":
                        self.queue_salida.put((Tarea.BORRAR_TODAS_LAS_TAREAS, 0, 0))
                    case "AA":
                        self.queue_salida.put((Tarea.DISPENSAR_COMIDA, 0, 0))
                    case "#":
                        self.queue_salida.put((Tarea.OBTENER_IDS_TAREAS, 0, 0))

            elif len(pieces) == 2 and pieces[0] == 'BB':
                hora = pieces[1]
                if not hora.isdigit() or not (0 <= int(hora) <= 23):
                    self.lcd.write_rotate("Hora invalida, usa 00-23", line=0)
                    return
                
                self.queue_salida.put((Tarea.BORRAR_TAREAS_HORA, int(hora), 0))

            elif len(pieces) == 3 and pieces[0] in ['A', 'B']:
                hora = pieces[1]
                if not hora.isdigit() or not (0 <= int(hora) <= 23):
                    self.lcd.write_rotate("Hora invalida, usa 00-23", line=0)
                    return
                
                minuto = pieces[2]
                if not minuto.isdigit() or not (0 <= int(minuto) <= 59):
                    self.lcd.write_rotate("Minuto invalido, usa 00-59", line=0)
                    return
                
                match pieces[0]:
                    case "A":
                        self.queue_salida.put((Tarea.AGREGAR_TAREA, int(hora), int(minuto)))
                    case "B":
                        self.queue_salida.put((Tarea.ELIMINAR_TAREA, int(hora), int(minuto)))
            else:
                self.lcd.write_rotate("Instruccion no reconocida", line=0)
                return
            
        except Exception as e:
            self.lcd.write_rotate("Instruccion no identificada", line=0)
            
            print("Error al parsear la instruccion:", e)
            
    def stop(self):
        self.active = False
        self.keyboard.stop()
        self.keyboard.join()

    def post_write(self, message: str, line: int = 0):
        self.queue_entrada.put((message, line, False))
    
    def clear(self):
        self.lcd.clear()

    def post_write_rotate(self, message: str, line: int = 0):
        self.queue_entrada.put((message, line, True))
    
    def force_clear_line(self, line: int = 0):
        self.lcd.write(" " * 16, line=line)
    
    def sleep(self, duration: float):
        time.sleep(duration)

if __name__ == "__main__":
    q = Queue()
    lcd_keyboard = LCDKeyboard(q)
    lcd_keyboard.start()