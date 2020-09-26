import os
from argparse import ArgumentParser
from socketserver import ForkingTCPServer, BaseRequestHandler
from filtro import Filtro
argms = ''


class Handler(BaseRequestHandler):
    def handle(self):
        root = os.getcwd() + argms.root
        receive = self.request.recv(1024).strip()
        listed = receive.decode().split('\r\n')
        for elem in listed:
            if elem.find('GET') != -1:
                _get = elem
        if _get.find('favicon.ico') != -1:
            self.request.sendall(open('favicon.ico', 'rb').read())
        else:
            self.manejador(listed)

    def manejador(self, listaR):
        content = {
            ".txt": " text/plain",
            ".jpg": " image/jpeg",
            ".ppm": " image/x-portable-pixmap",
            ".html": " text/html",
            ".pdf": " application/pdf"
            }
        for exten in content.keys():
            if listaR[0].find(exten) != -1:
                # Ya se que extension tengo, puedo sacar el  'Content-type'
                pass


if __name__ == "__main__":
    # global argms
    arg = ArgumentParser(
        description='Servidor de archivos, e filtro de imagenes',
        usage='server.py -r [ruta de documentos] -p [puerto] -s [bloque de lectura]'
    )
    arg.add_argument(
        '-r', '--root', nargs=1, type=str,
        help='ruta de los archivos', default='/root', metavar=''
    )
    arg.add_argument(
        '-p', '--port', nargs=1, type=int,
        help='puerto para el servidor', default=[8080], metavar=''
    )
    arg.add_argument(
        '-s', '--size', type=int, help='bloque de lectura',
        default=[255], metavar=''
    )

    argms = arg.parse_args()
    with ForkingTCPServer(('0.0.0.0', argms.port[0]), Handler) as server:
        server.serve_forever()
