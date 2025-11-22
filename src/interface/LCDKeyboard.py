from src.hardware.LCD import LCD
from src.hardware.MatrixKeyboard import MatrixKeyboard
from queue import Queue
from threading import Thread
import time

class LCDKeyboard(Thread):
    def __init__(self):
        super().__init__()
        self.lcd = LCD()
        self.queue = Queue()
        self.keyboard = MatrixKeyboard(self.queue)
        self.keyboard.start()

    def run(self):
        try:
            self.lcd.write("Ingrese instruccion:", line=0)
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
            self.lcd.write("Shutting down...", line=1)
            time.sleep(2)
            self.lcd.clear()

    def parse_instruccion(self, instruction: str):
        try:
            pieces = instruction.strip().upper().split()
            if len(pieces) < 3:
                raise ValueError("Formato esperado: <A|B> HH MM (ej: 'A 12 30')")

            accion = pieces[0]
            hora = pieces[1]
            minuto = pieces[2]

            if accion == "A":
                tipo = "ADD"
                self.lcd.write("Añadiendo instruccion", line=0)
            elif accion == "B":
                tipo = "DEL"
                self.lcd.write("Borrando instruccion", line=0)
            else:
                raise ValueError("Accion desconocida, usa A o B")

            print(f"{tipo} || Hora: {hora}, Minuto: {minuto}")

        except Exception as e:
            self.lcd.write("Instruccion no identificada", line=0)
            print("Error al parsear la instruccion:", e)


if __name__ == "__main__":
    lcd_keyboard = LCDKeyboard()
    lcd_keyboard.start()