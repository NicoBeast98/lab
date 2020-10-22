import asyncio as asy
from argparse import ArgumentParser
from server_tools import ServerTools



if __name__ == "__main__":
    arg = ArgumentParser(
        description='Servidor asincronico de multimedias',
        usage='server.py -r [ruta de documentos] -p [puerto] -s [bloque de lectura] -i [direccion ip]'
    )
    arg.add_argument(
        '-r', '--root', nargs=1, type=str,
        help='ruta de los archivos', default=['/root'], metavar=''
    )
    arg.add_argument(
        '-p', '--port', nargs=1, type=int,
        help='puerto para el servidor', default=[8080], metavar=''
    )
    arg.add_argument(
        '-s', '--size', type=int, help='bloque de lectura',
        default=[255], metavar=''
    )
    arg.add_argument(
        '-i', '--ip', type=str, help='direccion ip',
        default=['localhost'], metavar=''
    )

    argms = arg.parse_args()
    serverTools = ServerTools(argms)
