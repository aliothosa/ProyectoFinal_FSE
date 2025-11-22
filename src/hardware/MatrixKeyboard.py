import RPi.GPIO as GPIO
import time
from threading import Thread
from queue import Queue


class MatrixKeyboard(Thread):
    def __init__(self, q: Queue):
        super().__init__(daemon=True)
        self.row_pins = [5, 6, 13, 19]
        self.col_pins = [12, 16, 20, 21]
        self.keys = [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C'],
            ['*', '0', '#', 'D']
        ]
        self._string_output = ""
        self.active = True
        self.output_queue: Queue = q

        GPIO.setmode(GPIO.BCM)

        for pin in self.row_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

        for pin in self.col_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        try:
            while self.active:
                key = self.scan_keypad()
                if key == 'D':  
                    self.output_queue.put(self._string_output)
                    self.clear()
                elif key == 'C':  
                    self.erase_last()
                elif key == '*':
                    self._string_output += ' '
                elif key is not None:
                    self._string_output += key
                
                
                time.sleep(0.05)
        except Exception as e:
            print("Error en el hilo del teclado:", e)

    def clear(self):
        self._string_output = ""
    
    def erase_last(self):
        self._string_output = self._string_output[:-1]

    def get_string(self):
        return self._string_output
    
    def stop(self):
        self.active = False

    def scan_keypad(self):
        for row_index, row_pin in enumerate(self.row_pins):
            GPIO.output(row_pin, GPIO.LOW)

            for col_index, col_pin in enumerate(self.col_pins):
                if GPIO.input(col_pin) == GPIO.LOW:
                    time.sleep(0.02)
                    if GPIO.input(col_pin) == GPIO.LOW:
                        key = self.keys[row_index][col_index]

                        while GPIO.input(col_pin) == GPIO.LOW:
                            time.sleep(0.01)

                        GPIO.output(row_pin, GPIO.HIGH)
                        return key

            GPIO.output(row_pin, GPIO.HIGH)

        return None
