import threading


class Hilo(threading.Thread):
    def __init__(self, color, intLeave):
        if color == 'red':
            self.colorByte = 0
        elif color == 'green':
            self.colorByte = 1
        elif color == 'blue':
            self.colorByte = 2
        else:
            raise Exception('Uso erroneo de clase Hilo')
        self.intLeave = intLeave

    def run(self, msgBytes, bloqLec):
        pass
