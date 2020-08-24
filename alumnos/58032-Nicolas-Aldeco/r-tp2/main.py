import argparse
import time
import os
from rot13 import rot13
from header import make_head, r_body
from bytes_decoder import tobits, listtobytes
from concurrent.futures import ThreadPoolExecutor


# Trabajo de hilos
def worker(byte, bit):
    if (byte % 2 == 0) and (bit == 1):
        byte += 1
        # Sumo uno al byte
    elif (byte % 2 != 0) and (bit == 0):
        byte -= 1
        # Resto un al byte
    else:
        pass
        # No modifico el byte
    return byte


def encode(args):
    start = time.time()
    msgSize = os.path.getsize(args.message[0])
    imagen = open(args.file[0], 'rb')
    raster = r_body(imagen)
    imagen.seek(raster)
    body = []
    pix = []
    # Leo el body de la imagen por bloques
    while True:
        lectura = imagen.read(args.size[0])
        for p, b in enumerate(lectura):
            if p % 3 == 0:
                body.append(pix)
                pix = []
            pix.append(b)
        if not lectura:
            break
    body.pop(0)
    # Cifrado rot13
    if args.cifrado:
        hiloC = ThreadPoolExecutor()
        res = hiloC.submit(rot13, open(args.message[0], 'r').read())
        lectura = res.result()
    else:
        lectura = open(args.message[0], 'r').read()
    print(f'Mensaje >> {lectura}')
    msgBits = tobits(lectura)
    hilos = ThreadPoolExecutor(max_workers=3)
    with open(args.output[0], 'wb') as encodeImg:
        encodeImg.write(
            make_head(
                args.file[0], args.cifrado, args.offset[0], args.interleave[0],
                msgSize)
        )
        color = 'red'
        for pos, pix in enumerate(body):
            if pos >= args.offset[0]:
                if pos % args.interleave[0] == 0:
                    if color == 'red':
                        _workR = hilos.submit(worker, pix[0], msgBits[0])
                        body[pos][0] = _workR.result()
                        color = 'green'
                    elif color == 'green':
                        _workG = hilos.submit(worker, pix[1], msgBits[0])
                        body[pos][1] = _workG.result()
                        color = 'blue'
                    elif color == 'blue':
                        _workB = hilos.submit(worker, pix[2], msgBits[0])
                        body[pos][2] = _workB.result()
                        color = 'red'
                    msgBits.pop(0)
            if msgBits == []:
                break
        # Junto el body en uno nuevamente
        newBody = []
        for pix in body:
            for j in pix:
                newBody.append(j)
        # Lo escribo en la imagen
        encodeImg.write(listtobytes(newBody))
    end = time.time() - start
    print(f'Tiempo de ejecucion: {end} segundos')


if __name__ == "__main__":
    arg = argparse.ArgumentParser(
        description='Cifrado LSB'
    )
    arg.add_argument(
        '-f', '--file', nargs=1, required=True, type=str, help='imagen.ppm',
        metavar=''
    )
    arg.add_argument(
        '-m', '--message', nargs=1, required=True, type=str, help='mensaje',
        metavar=''
    )
    arg.add_argument(
        '-o', '--output', nargs=1, required=True, type=str, help='salida.ppm',
        metavar=''
    )
    arg.add_argument(
        '-s', '--size', nargs=1, type=int, help='tamano bloque de lectura',
        default=[256], metavar=''
    )
    arg.add_argument(
        '-e', '--offset', nargs=1, type=int,
        help='defase en comienzo de mensaje',
        default=[1], metavar=''
    )
    arg.add_argument(
        '-i', '--interleave', nargs=1, type=int,
        help='intervalo entre pixeles',
        default=[1], metavar=''
    )
    arg.add_argument(
        '-c', '--cifrado', action='store_true',
        help='aplicar cifrado rot13 al mensaje'
    )
    test = argparse.Namespace(cifrado=False, file=['dog.ppm'], interleave=[1], message=['manel'], offset=[1], output=['test.ppm'], size=[255])
    encode(test)
