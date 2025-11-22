
import RPi.GPIO as GPIO
from typing import Union
import time

BUZZER_PIN = 26 #ambia si usas otro GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

THE_LICK = ["D5", "E5", "F5", "G5", "E5", "C5", "D5"]

class Buzzer:
    def __init__(self, buzzer_pin=26):
        # Notas en Hz (aprox)
        self.notes = {
            "C5": 523.25,
            "D5": 587.33,
            "E5": 659.25,
            "F5": 698.46,
            "G5": 783.99,
        }
        self.pwm = GPIO.PWM(buzzer_pin, 440)  # freq inicial cualquiera
        self.pwm.start(0)

    def play_sound(self, note:str = "C5", duration:Union[float, int]=1.0):
        try:
            if note in self.notes:
                self.play_tone(self.notes[note], duration if duration > 0 else 1.0)
        finally:
            self.pwm.stop()

    
    def play_tone(self, freq, duration=0.18):
        self.pwm.ChangeFrequency(freq)
        self.pwm.start(50)         # 50% duty
        time.sleep(duration)
        self.pwm.stop()
        time.sleep(0.03)      # pequeño silencio entre notas