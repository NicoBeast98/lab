import os
from argparse import ArgumentParser
from socketserver import ForkingTCPServer, BaseRequestHandler
from filtro import Filtro
argms = ''


class Handler(BaseRequestHandler):
    def handle(self):
        # Variables
        root = os.getcwd() + argms.root[0]
        content = {
            ".txt": " text/plain",
            ".jpg": " image/jpeg",
            ".ppm": " image/x-portable-pixmap",
            ".html": " text/html",
            ".pdf": " application/pdf",
            ".ico": " image/x-ico",
            ".mp4": " video/mp4",
            ".aac": " audio/aac"
            }
        # <-->
        self.data = self.request.recv(1024)
        encabezado = self.data.decode().split()
        _get = encabezado[1]
        # Mando el favicon.ico
        if _get.find('favicon.ico') != -1:
            icon = open('favicon.ico', 'rb')
            size = os.stat('favicon.ico').st_size
            self.request.sendall(self.makeHeader(content['.ico'], size))
            self.request.sendall(icon.read())
            exit()
        # <-->
        # Si ingreso al la raiz, mando el index
        if _get == '/' or _get == '/index.html' or _get == '/index':
            index = open('index.html', 'rb')
            size = os.stat('index.html').st_size
            self.request.sendall(self.makeHeader(content['.html'], size))
            self.request.sendall(index.read())
            exit()
        # Manejo si la peticion es correcta
        dicFile = self.fileLookUp(_get, root, content)
        if dicFile['nice'] is True:
            self.request.sendall(dicFile['head'])
            file = dicFile['file']
            while True:
                lec = file.read(argms.size[0])
                if not lec:
                    break
                self.request.sendall(lec)
            if os.path.isfile('temp.ppm'):
                os.remove('temp.ppm')
            exit()
        else:
            self.request.sendall(dicFile['errorNameH'])
            self.request.sendall(open(dicFile['errorFile'], 'rb').read())
            exit()

    def makeHeader(self, cType, lenth):
        head = 'HTTP/1.1 200 OK\r\n'
        cont = f'Content-type:{cType}\r\n'
        lent = f'Content-length:{lenth}'
        head += cont + lent + '\r\n\r\n'
        return head.encode('utf8')

    def fileLookUp(self, get, root, content):
        diccGood = {
            'nice': True,
            'file': None,
            'head': None
        }
        diccBad = {
            'nice': False,
            'errorNameH': None,
            'errorFile': None
        }
        if get.find('.') != -1:
            var = ''
            sp = list(get.partition('.'))
            name = sp[0]
            temp = sp[2].split('?')
            if len(temp) > 1:
                exten = '.'+temp[0]
                var = temp[1]
            exten = '.'+temp[0]
            absDir = root+name+exten
        else:
            # La peticion es erronea
            diccBad['errorNameH'] = b'HTTP/1.1 400 Bad Request\r\n\r\n'
            diccBad['errorFile'] = 'errors/error400.html'
            return diccBad
        extenV = exten in content
        if extenV is False:
            # La extension del archivo no esta soportda
            diccBad['errorNameH'] = b'HTTP/1.1 415 Unsupported Media Type\r\n\r\n'
            diccBad['errorFile'] = 'errors/error415.html'
            return diccBad
        # Verifico el que archivo exista
        fileEx = os.path.isfile(absDir)
        if fileEx is False:
            diccBad['errorNameH'] = b'HTTP/1.1 404 Not Found\r\n\r\n'
            diccBad['errorFile'] = 'errors/error404.html'
            return diccBad
        try:
            size = os.stat(absDir).st_size
            if exten == '.ppm':
                if var != '':
                    # ppm con filtro
                    chs = var.split('=')
                    f = chs[0]
                    i = float(chs[1])
                    imgFilter = Filtro(absDir, f, i, argms.size[0])
                    with open('temp.ppm', 'wb') as temp:
                        temp.write(imgFilter.main())
                        temp.close()
                    diccGood['file'] = open('temp.ppm', 'rb')
                    diccGood['head'] = self.makeHeader(content['.ppm'], os.stat('temp.ppm').st_size)
                    return diccGood
                else:
                    # ppm sin modificar
                    diccGood['file'] = open(absDir, 'rb')
                    diccGood['head'] = self.makeHeader(content['.ppm'], size)
                    return diccGood
            else:
                diccGood['file'] = open(absDir, 'rb')
                diccGood['head'] = self.makeHeader(content[exten], size)
                return diccGood
        except:
            diccBad['errorNameH'] = b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
            diccBad['errorFile'] = 'errors/error500.html'
            return diccBad


if __name__ == "__main__":
    arg = ArgumentParser(
        description='Servidor de archivos, e filtro de imagenes',
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
    with ForkingTCPServer((argms.ip[0], argms.port[0]), Handler) as server:
        server.allow_reuse_address = True
        server.serve_forever()
