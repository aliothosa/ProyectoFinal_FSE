from RPLCD.i2c import CharLCD
import time

class LCD:
    def __init__(self, address=0x27, port=1, cols=16, rows=2):
        self.cols = cols      # <-- guardas los valores aquí
        self.rows = rows
        self.lcd = CharLCD('PCF8574', address, port=port, cols=cols, rows=rows)

    def clear(self):
        self.lcd.clear()
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(" " * 16)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(" " * 16)
        self.lcd.home()

    def write(self, text, line=0):
        if line < 0 or line >= self.rows:   # <-- usas tus propios valores
            raise ValueError("Line number out of range")

        self.lcd.cursor_pos = (line, 0)
        text = text.ljust(self.cols)[:self.cols]  # <-- longitud máxima
        self.lcd.write_string(text)
    
    def write_rotate(self, text, line=0, delay=0.3):
        if line < 0 or line >= self.rows:
            raise ValueError("Line number out of range")

        padding = " " * self.cols
        scroll_text = padding + text + padding

        for i in range(len(scroll_text) - self.cols + 1):
            frame = scroll_text[i:i + self.cols]

            self.lcd.cursor_pos = (line, 0)
            self.lcd.write_string(frame)

            time.sleep(delay)
