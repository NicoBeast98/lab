#!/usr/bin/python3
import argparse
import multiprocessing as mp

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
        '-f','--file',nargs=1,required=True,type=str,help='nombre_archivo.ppm',metavar=''
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
        '-s','--size',nargs=1,type=int,help='cantidad de bytes por lectrua',metavar='',default=256
    )
    argums = arg.parse_args()
    info = {
        'file':argums.file[0],'red':argums.red,'blue':argums.blue,'green':argums.green,'size':argums.size
    }
    return info

def main(dicc_datos):
    size = dicc_datos['size']
    cola = mp.Queue()
    for color in ['red','green','blue']:
        procces = []
        procces.append(
            mp.Process(
                target=color_mang,args=(color,dicc_datos[color],cola,),name=color
            )
        )
    with open(dicc_datos['file'], 'rb') as img:
        # como puedo leer y tratar los datos en binario?



def color_mang(color, factor, cola):
    return 0

    



if __name__ == "__main__":
    dicc_datos = argumentos()
    main(dicc_datos)
    

