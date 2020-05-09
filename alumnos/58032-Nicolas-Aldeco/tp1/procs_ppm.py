#!/usr/bin/python3
import argparse
import multiprocessing as mp
import array as arr


# Defino los argumentos del programa
def argumentos():
    arg = argparse.ArgumentParser(
        description='''\n
        ~Procesamiento de imagenes PPM: 
Esta herramienta esta destinada para separar una imagen
de extension .ppm en sus colores RGB basicos, separando
por cada color una imagen de distinta intensidad
        ''',
        usage='procs_ppm.py -f [archivo] -r [red] -b [blue] -g [green] -s [size]'
    )
    arg.add_argument(
        '-f','--file',nargs=1,required=False,type=str,help='nombre_archivo.ppm',metavar=''
        )
    arg.add_argument(
        '-r','--red',nargs=1,type=float,help='intensidad de rojo',metavar='',default=0
    )
    arg.add_argument(
        '-g','--green',nargs=1,type=float,help='intensidad de verde',metavar='',default=0
    )
    arg.add_argument(
        '-b','--blue',nargs=1,type=float,help='intensidad de azul',metavar='',default=0
    )
    arg.add_argument(
        '-s','--size',nargs=1,type=int,help='bytes por lectrua',metavar='',default=255
    )
    argums = arg.parse_args()
    info = {
        'file':argums.file[0],'red':argums.red,'blue':argums.blue,'green':argums.green,'size':argums.size[0]
    }
    return info

# *~Defino a los procesos hijos~*
def color_mang(color, datos, cola):
    name = datos['file'].split('.')
    inten = datos[color]
    new = name[0]+'_'+color+'.ppm'
    with open(new, 'wb') as img:
        while True:
            line = cola.get()
            img.write(filter(color, line, inten))
#~---------------------------~

# Funcion que determina las caracteristicas de la imagen
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
    img.close()
    return [pos, n_array]
#~-----------------------------------------------------~

# Filtro los distintos canales de color
def filter(color, line, inten):
    if line.find(b'P6') != -1:
        return line
    else:
        if color == 'red':
            return line
        if color == 'green':
            return line
        if color == 'blue':
            return line
#~-----------------------------------~

# *~~~> Funcion principal del programa <~~~*
def main(dicc_datos):
    colors = ['red','green','blue']
    procces = []
# Creo una cola por proceso
    cola = {
        'red' : mp.SimpleQueue(),
        'green' : mp.SimpleQueue(),
        'blue' : mp.SimpleQueue(),
    }
# Creo 3 procesos, uno por cada canal de color
    for color in colors:
        procces.append(
            mp.Process(
                target=color_mang,args=(color,dicc_datos,cola[color]),name=color
            )
        )
# La funcion det_img separa la cabecera de la imagen del resto
    detalles = det_img(dicc_datos)
    for c in colors:
        cola[c].put(detalles[1])
# Empiezo a leer la imagen que se paso
    with open(dicc_datos['file'], 'rb') as img:
        img.seek(detalles[0])
# Empiezo los 3 procesos
        for i in range(3):
            procces[i].start()
        while True:
            line = img.read(dicc_datos['size'])
            for c in colors:
                cola[c].put(line)
            if line.__sizeof__() < dicc_datos['size']:
                for c in colors:
                    cola[c].put(line)
                break
    for i in range(3):
        procces[i].terminate()
    print('end')
#~----------------------------------~


if __name__ == "__main__":
    # dicc_datos = argumentos()
    dicc_datos = {
        'file':'dog.ppm','red':2,'blue':0,'green':0,'size':250
    }
    main(dicc_datos)
