import argparse
import os
# from concurrent import futures [Hilos]
from rot13 import rot13
from header import make_head


class Main():
    def __init__(self, arg):
        self.file = arg.file[0]
        self.message = arg.message[0]
        self.output = arg.output[0]
        self.size = arg.size[0]
        self.offset = arg.offset[0]
        self.interleave = arg.interleave[0]
        self.cifrado = arg.cifrado

    def encode(self):
        msgSize = os.path.getsize(self.message)
        if self.cifrado:
            lectura = rot13(open(self.message, 'r').read())
        else:
            lectura = open(self.message, 'r').read()
        print(lectura)
        with open(self.output, 'wb') as encodeImg:
            encodeImg.write(
                make_head(
                    self.file, self.cifrado, self.offset, self.interleave,
                    msgSize)
            )


if __name__ == "__main__":
    arg = argparse.ArgumentParser(
        description='Cifrado LSB'
    )
    arg.add_argument(
        '-f', '--file', nargs=1, required=True, type=str, help='imagen.ppm', metavar=''
    )
    arg.add_argument(
        '-m', '--message', nargs=1, required=True, type=str, help='mensaje', metavar=''
    )
    arg.add_argument(
        '-o', '--output', nargs=1, required=True, type=str, help='salida.ppm', metavar=''
    )
    arg.add_argument(
        '-s', '--size', nargs=1, type=int, help='tamano bloque de lectura', default=[256], metavar=''
    )
    arg.add_argument(
        '-e', '--offset', nargs=1, type=int, help='defase en comienzo de mensaje', default=[1], metavar=''
    )
    arg.add_argument(
        '-i', '--interleave', nargs=1, type=int, help='intervalo entre pixeles', default=[1], metavar=''
    )
    arg.add_argument(
        '-c', '--cifrado', action='store_true', help='aplicar cifrado rot13 al mensaje'
    )
    obj = Main(arg.parse_args())
    obj.encode()
