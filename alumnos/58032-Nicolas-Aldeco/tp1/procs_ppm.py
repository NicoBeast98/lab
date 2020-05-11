#! /usr/bin/python3
import argparse
import multiprocessing as mp
import os
import array

# Defino los argumentos del programa
def argumentos():
    arg = argparse.ArgumentParser(
        description='''\n
        ~Procesamiento de imagenes PPM: 
Esta herramienta esta destinada para separar una imagen
de extension .ppm en sus colores RGB basicos, separando
por cada color una imagen de distinta intensidad.'''
        ,epilog='''\n
-> ATENCION -> 
Si vuelve a correr el programa con una imagen ya utilizada
anteriormente, esta se vera afectada.
        ''',
        usage='procs_ppm.py -f [archivo] -r [red] -b [blue] -g [green] -s [size]',

    )
    arg.add_argument(
        '-f','--file',nargs=1,required=True,type=str,help='nombre_archivo.ppm',metavar=''
        )
    arg.add_argument(
        '-r','--red',nargs=1,type=float,help='intensidad de rojo',metavar='',default=[1]
    )
    arg.add_argument(
        '-g','--green',nargs=1,type=float,help='intensidad de verde',metavar='',default=[1]
    )
    arg.add_argument(
        '-b','--blue',nargs=1,type=float,help='intensidad de azul',metavar='',default=[1]
    )
    arg.add_argument(
        '-s','--size',nargs=1,type=int,help='bytes por lectrua (solo multiplos de 3)',metavar='',default=[255]
    )
    argums = arg.parse_args()
    info = {
        'file':argums.file[0],'red':argums.red[0],'blue':argums.blue[0],'green':argums.green[0],'size':argums.size[0]
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
    for col in ['red','green','blue']:
        if info[col] < 0:
            print('ERROR 3 - La intensidad no puede ser negativa')
            exit(3)
    if info['size']%3 != 0:
        print('ERROR 4 - El tamaño de lectura no es multiplo de 3')
        exit(4)
    return 'pass'
# <-~~->


# *~Defino a los procesos hijos~*
def color_mang(color, datos, cola):
    name = datos['file'].split('.')
    inten = datos[color]
    new = name[0]+'_'+color+'.ppm'
    if color == 'red':
        n_color = 0
    elif color == 'green':
        n_color = 1
    elif color == 'blue':
        n_color = 2
    with open(new, 'wb') as img:
        img.write(cola.get())
        while True:
            line = cola.get()
            listed = (str(line).lstrip('b\'').rstrip('\'')).split(" ")
            for x in range(len(listed)):
                if x%3 == n_color:
                    if len(listed[x]) == 1:
                        listed[x] = '0'+listed[x]
                    if listed[x] == '':
                        listed[x] = '00'
                    listed[x] = int(ord(bytes.fromhex(listed[x])) * inten)
                    if listed[x] > 255:
                        listed[x] = 255
                else:
                    listed[x] = 0
            nueva = array.array('B', listed)
            nueva.tofile(img)
            if len(listed) < datos['size']:
                break
    exit(1)

# <-~~->

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

# Funcion que determina la cabecera de la imagen
def det_img(info):
    with open(info['file'], 'rb') as img:
        info = img.read(100)
        header = bytearray(info)
        pos = header.find(b'255\n')
        pos += 4
        n_array = bytearray()
        cutted = header.split(b'\x0A')
        if cutted[1].startswith(b'\x23\x20'):
            cutted.pop(1)
        for _ in range(3):
            n_array += bytes(cutted[_]) + b'\x0A'
    return [pos, n_array]
# <-~~->


# Funcion principal del programa
def main(dicc_datos):
    colors = ['red','green','blue']
    procces = []
# Creo procesos por cada color y a cada uno le asigno una cola
    cola = {
        'red' : mp.Queue(),
        'green' : mp.Queue(),
        'blue' : mp.Queue(),
    }
    for color in colors:
        procces.append(
            mp.Process(
                target=color_mang,args=(color,dicc_datos,cola[color]),name=color
            )
        )
    for i in range(3):
        procces[i].start()
# <-~~->
    detalles = det_img(dicc_datos)

    for color in colors:
        cola[color].put(detalles[1])

    with open(dicc_datos['file'], "rb") as archivo:
        archivo.seek(detalles[0])
        while True:
            for x in reading(archivo, dicc_datos['size']):
                for color in colors:
                    cola[color].put(x.encode('ascii'))
            if procces[0].exitcode is None : pass
            elif procces[1].exitcode is None: pass
            elif procces[2].exitcode is None: pass
            else: break
    for i in range(3):
        procces[i].terminate()
    print('[done]')
    exit(0)
# <-~~->

if __name__ == "__main__":
    dicc_datos = argumentos()
    main(dicc_datos)
