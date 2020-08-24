import argparse
from bytes_decoder import frombits
from header import read_head
from rot13 import rot13


def pix_parity(pix):
    if pix % 2 == 0:
        return 0
    else:
        return 1


def decode(img):
    header = read_head(img)
    raster = header[0]
    coments = header[-1]
    for comment in coments:
        temp = comment.decode()
        if temp.find('#UMCOMPU2') != -1:
            head = temp
    try:
        head.split('#UMCOMPU2')
    except:
        raise Exception('ERROR - No se puede extraer mensaje, falta comentario')

    sep = head.split(' ')
    # Cifrado rot13
    cif = False
    if sep[0].find('-C') != -1:
        cif = True
    offset = int(sep[1])
    intleave = int(sep[2])
    l_total = int(sep[3])

    msgB = []
    with open(img, 'rb') as file:
        # Me muevo al incio del body
        file.seek(raster)
        bodyPix = []
        body = file.read()
        pix = []
        for p, b in enumerate(body):
            if p % 3 == 0:
                bodyPix.append(pix)
                pix = []
            pix.append(b)
        bodyPix.pop(0)

        color = 'red'
        for pos, pix in enumerate(bodyPix):
            if pos >= offset:
                if pos % intleave == 0:
                    if color == 'red':
                        msgB.append(pix_parity(pix[0]))
                        color = 'green'
                    elif color == 'green':
                        msgB.append(pix_parity(pix[1]))
                        color = 'blue'
                    elif color == 'blue':
                        msgB.append(pix_parity(pix[2]))
                        color = 'red'
                if len(msgB) == l_total*8:
                    break
    mensaje = frombits(msgB)
    if cif:
        des = rot13(mensaje)
        print(f'Mensaje: {mensaje}')
        print(f'Mensaje [rot13 - decode]: {des}')
    else:
        print(f'Mensaje: {mensaje}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", nargs=1, type=str, required=True
    )
    args = parser.parse_args()
    decode(args.file[0])
