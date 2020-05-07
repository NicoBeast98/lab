#!/usr/bin/python3
import argparse
import multiprocessing as mp
import array as arr

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

def main(dicc_datos):
    colors = ['red','green','blue']
    procces = []
    cola = {
        'red' : mp.SimpleQueue(),
        'green' : mp.SimpleQueue(),
        'blue' : mp.SimpleQueue(),
    }
    for color in colors:
        procces.append(
            mp.Process(
                target=color_mang,args=(color,dicc_datos,cola[color]),name=color
            )
        )
    detalles = det_img(dicc_datos)
    line = detalles[1]
    with open(dicc_datos['file'], 'rb') as img:
        img.seek(detalles[0])
        for i in range(3):
            procces[i].start()
        while True:
            for __ in colors:
                cola[__].put(line)
            line = img.read(dicc_datos['size'])
    for i in range(3):
        procces[i].terminate

def color_mang(color, datos, cola):
    name = datos['file'].split('.')
    inten = datos[color]
    new = name[0]+'_'+color+'.ppm'
    with open(new, 'wb') as img:
        while True:
            line = cola.get()
            img.write(filter(color, line, inten))

def det_img(info):
    with open(info['file'], 'rb') as img:
        info = img.read(100)
        header = bytes(info)
        pos = header.find(b'255\n')
        pos += 8
        new = str(info)
        new = new.lstrip('b\'')
        nuevos_det = ''
        for elem in range(pos):
            nuevos_det += new[elem]
        encode = bytes(nuevos_det.encode('utf-8')) # se concatena mal
    img.close()
    return [pos, encode]

def filter(color, line, iten):
    n_line = b''
    if line.find(b'P6') != -1:
        return line
    else:
        if color == 'red':
            n_line += arr.array('B', line)
            return n_line
        if color == 'green':
            n_line += arr.array('B', line)
            return n_line
        if color == 'blue':
            n_line += arr.array('B', line)
            return n_line



if __name__ == "__main__":
    # dicc_datos = argumentos()
    dicc_datos = {
        'file':'dog.ppm','red':2,'blue':0,'green':0,'size':250
    }
    main(dicc_datos)
