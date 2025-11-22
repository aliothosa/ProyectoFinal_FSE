import sys
import termios
import tty
from queue import Queue
from threading import Thread
class KeyboardListener:
    def __init__(self):
        self.running = True
        self.q = Queue()

    def start(self):
        print("Escuchando teclado (Ctrl+C para salir)...")
        old_settings = termios.tcgetattr(sys.stdin)

        try:
            tty.setraw(sys.stdin)
            while self.running:
                char = sys.stdin.read(1)   # Lee 1 tecla

                if char == "\x03":  # ctr + c
                    break
                else:
                    self.q.put(char)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            print("\nModo normal restaurado.")

def print_str(char:str):
    sys.stdout.write('\r\x1b[2K')
    sys.stdout.flush()
    print(self.q, end='', flush=True)
    print("".join(self.q),end='\n', flush=True)
    self.q.clear()

class KeyboardWatch(Thread):
    def __init__(self, queue:Queue):
        super().__init__()
        self.queue = queue
        self.running = True

    def run(self):
        while self.running:
            char = self.queue.get()
            if char is None:
                break
            print_str(char, end='', flush=True)

if __name__ == "__main__":
    listener = KeyboardListener()
    try:
        listener.start()
    except KeyboardInterrupt:
        print("\nInterrupción por teclado recibida. Saliendo...")
