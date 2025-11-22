from RPLCD.i2c import CharLCD

class LCD:
    def __init__(self, address=0x27, port=1, cols=16, rows=2):
        self.lcd = CharLCD('PCF8574', address, port=port, cols=cols, rows=rows)

    def clear(self):
        self.lcd.clear()

    def write(self, text, line=0):
        if line < 0 or line >= self.lcd.rows:
            raise ValueError("Line number out of range")
        self.lcd.cursor_pos = (line, 0)
        self.lcd.write_string(text.ljust(self.lcd.cols)[:self.lcd.cols])
