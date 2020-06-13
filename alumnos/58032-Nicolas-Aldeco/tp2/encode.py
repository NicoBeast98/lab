import os
import argparse
import header
import worker


# Defino los argumentos del programa
def argumentos():
    arg = argparse.ArgumentParser(
        description='''\n
Cifrado de mensajes''', usage='''
procs_ppm.py -f [archivo] -s [size] -m [mensaje] -o [offset] -i [interleave] -e [exit-file]''',
    )
    arg.add_argument(
        '-s', '--size', nargs=1, type=int,
        help='bytes por lectrua (solo multiplos de 3)', metavar='',
        default=[255]
    )
    arg.add_argument(
        '-f', '--file', nargs=1, required=True, type=str,
        help='nombre_archivo.ppm', metavar=''
        )
    arg.add_argument(
        '-m', '--message', nargs=1, required=True, type=str,
        help='mensaje_esteganográfico.[file]', metavar=''
    )
    arg.add_argument(
        '-o', '--offset', nargs=1, required=True, type=int,
        help='offset en pixels del inicio del raster', metavar=''
        )
    arg.add_argument(
        '-i', '--interleave', nargs=1, required=True, type=int,
        help='interleave de modificacion en pixel', metavar=''
        )
    arg.add_argument(
        '-e', '--exit', nargs=1, required=True, type=str,
        help='estego-mensaje', metavar=''
        )

    argums = arg.parse_args()
    info = {
        'size': argums.size[0],
        'file': argums.file[0],
        'message': argums.message[0],
        'offset': argums.offset[0],
        'interleave': argums.interleave[0],
        'exit': argums.exit[0]
    }
    val = check_validez(info)
    if val == 'pass':
        return info
# <-~~->


# Valido los ingresos
def check_validez(info):
    if info['file'].find('ppm') == -1:
        print('ERROR 1 - La extencion del archivo no es ppm')
        exit(1)
    try:
        with open(info['file'], 'r') as _:
            pass
    except FileNotFoundError:
        print('ERROR 2 - El archivo no existe')
        exit(2)
# <-~~->


# Normalizo la longuitud de los bytes
def toNormBytes(byte):
    bStr = bin(byte)
    bStr = bStr.lstrip('0b')
    largo = len(bStr)
    if largo < 8:
        strInv = bStr[::-1]
        emptys = 8 - largo
        for n in range(emptys):
            strInv += '0'
        bStr = strInv[::-1]
    return bStr


def reading(archivo, size):
    while True:
        lec = archivo.read(size).hex()
        if not lec:
            break
        x = ""
        for y in range(size):
            if lec[y*2:y*2+2] != '':
                x += lec[y*2:y*2+2] + " "
        yield x.strip(" ")


def main(head, newHead, info):
    th = []
    rgbColors = ['red', 'green', 'blue']

    msgFile = open(info['message'], 'rb')   # Abro el msg en bytes
    inputFile = open(info['file'], 'rb')     # IO en bytes
    inputFile.seek(head[0])   # Muevo lector al final del head

# Creo una lista con un hilo por cada color
    for color in rgbColors:
        th.append(worker.Hilo(color, info['interleave']))

# Genero un string del mensaje a esconder
    strMsg = ''
    for msg in reading(msgFile, info['size']):
        temp = msg.split(' ')
        for n in range(len(temp)):
            # msgFile en una sola cadea de str
            strMsg += toNormBytes(int(temp[n], base=16))

    with open(info['exit'], 'wb') as exitFile:
        exitFile.write(newHead[1])  # Inserto cabecera
        for lec in reading(inputFile, info['size']):
            lec.split(' ')
        exitFile.write(lec)
    # Close open files
    msgFile.close()
    inputFile.close()


if __name__ == "__main__":

    # info = argumentos()
    # Debug :

    info = {
        'size': 255,
        'file': 'colors.ppm',
        'message': 'mensaje',
        'offset': 1,
        'interleave': 1,
        'exit': 'e_dog.ppm'
    }
    # <-->
    sizeFileMsg = os.path.getsize(info['message'])
    sizeFileImg = os.path.getsize(info['file'])

    if sizeFileMsg > sizeFileImg/(8*info['interleave']):
        raise Exception('No se puede esconder un mensaje tan grande en esta imagen')

    head = header.detHeader(info['file'])
    newHead = header.makeNewHeader(head,
                                   str(info['offset']),
                                   str(info['interleave']),
                                   str(sizeFileMsg)
                                   )
    main(head, newHead, info)
