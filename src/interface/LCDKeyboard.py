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
            while True:
                self.lcd.write(self.keyboard.get_string(), line=1)
                if not self.queue.empty():
                    self.parse_instruccion(self.queue.get())
                    self.lcd.clear()
                    self.lcd.write("Input Received:\n" + self.keyboard.get_string(), line=0)
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.keyboard.stop()
            self.lcd.clear()
            self.lcd.write("Shutting down...", line=0)
            time.sleep(2)
            self.lcd.clear()

    def parse_instruccion(self, instruction: str):
        pieces = instruction.split(' ')
        if pieces[0] == "A":
            instruction = 'ADD'
            self.lcd.write("Añadiendo instruccion", line=0)
        if pieces[0] == "B":
            instruction = 'DEL'
            self.lcd.write("Borrando instruccion", line=0)
        hora, minuto = pieces[::2]
        print(f"{instruction} || Hora: {hora}, Minuto: {minuto}")

