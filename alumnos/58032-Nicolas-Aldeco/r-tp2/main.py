import argparse
import time
import os
from rot13 import rot13
from header import make_head, r_body, read_head
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
    mensaje = open(args.message[0], 'r').read()
    if args.cifrado:
        hiloC = ThreadPoolExecutor()
        res = hiloC.submit(rot13, mensaje)
        lectura = res.result()
    else:
        lectura = mensaje
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

# Valido los ingresos
def check_validez(info):
    if info.file[0].find('.ppm') == -1:
        print('ERROR - La extencion del archivo no es ppm')
        exit()
    try:
        with open(info.file[0], 'r') as _:
            pass
    except FileNotFoundError:
        print('ERROR - El archivo de entrada no existe')
        exit()
    try:
        with open(info.message[0], 'r') as _:
            pass
    except FileNotFoundError:
        print('ERROR - El archivo de mensaje no existe')
        exit()
    if info.size[0]%3 != 0:
        print('ERROR - El tamaño de lectura no es multiplo de 3')
        exit()
    cabe = read_head(info.file[0])
    size_ = os.path.getsize(info.message[0]) * 8 * info.interleave[0] + info.offset[0]
    if size_ > cabe[1]*cabe[2]:
        print('ERROR - La imagen no tiene los pixeles suficientes para este mensaje')
        exit()
    return True
# <-~~->


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
        default=[255], metavar=''
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
    args = arg.parse_args()
    if check_validez(args):
        encode(args)
