import os


class ServerTools():

    def __init__(self, dicc):
        self.root = os.getcwd() + dicc['root']
        self.port = dicc['port']
        self.size = dicc['size']
        self.ip = dicc['ip']
        self.lista = ''

        # Tipos de contenido aceptados:
        self.content = {
            ".txt": " text/plain",
            ".jpg": " image/jpeg",
            ".ppm": " image/x-portable-pixmap",
            ".html": " text/html",
            ".pdf": " application/pdf",
            ".ico": " image/x-ico",
            ".mp4": " video/mp4",
            ".aac": " audio/aac",
            }

    def makeHeader(self, cType, lenth):
        head = 'HTTP/1.1 200 OK\r\n'
        cont = f'Content-type:{cType}\r\n'
        lent = f'Content-length:{lenth}'
        head += cont + lent + '\r\n\r\n'
        return head.encode('utf8')

    def responseIcon(self):
        head = self.makeHeader(
            self.content['.ico'], os.stat('favicon.ico').st_size)
        return head

    # Respuesta de errores.
    # 400 Bad Request
    def response400(self):
        head = b'HTTP/1.1 400 Bad Request\r\n\r\n'
        body = open('errors/error400.html', 'rb').read()
        return head+body

    # 404 Not Found
    def response404(self):
        head = b'HTTP/1.1 404 Not Found\r\n\r\n'
        body = open('errors/error404.html', 'rb').read()
        return head+body

    # 415 Unsopported Media Type
    def response415(self):
        head = b'HTTP/1.1 415 Unsupported Media Type\r\n\r\n'
        body = open('errors/error415.html', 'rb').read()
        return head+body

    # 500 Internal Server Error
    def response500(self):
        head = b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
        body = open('errors/error500.html', 'rb').read()
        return head+body

    def parseGet(self, byts):
        lista = []
        for elem in byts.split(b'\r\n'):
            lista.append(elem.decode('utf-8'))
        return lista

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_size(self):
        return self.size

    def get_root(self):
        return self.root

    def fileLookUp(self, get):
        if get.find('.') != -1:
            sp = list(get.partition('.'))
            name = sp[0]
            exten = '.'+sp[2]
            absDir = self.root+name+exten
        else:
            # La peticion es erronea
            return [400, self.response400()]
        extenV = exten in self.content
        if extenV is False:
            # La extension del archivo no esta soportda
            return [415, self.response415()]
        # Verifico el que archivo exista
        fileEx = os.path.isfile(absDir)
        if fileEx is False:
            return [404, self.response404()]
        try:
            size = os.stat(absDir).st_size
            head = self.makeHeader(self.content[exten], size)
            return [200, head]
        except:
            # Error en el servidor
            return [500, self.response500()]

    def listDirInIndex(self):
        lista = self.rDirList(os.listdir(path=self.root), self.root)
        # print(lista)
        body = f'''
<!DOCTYPE html>
<html>
    <head>
        <title>My Web Server</title>
        <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
        <meta content="utf-8" http-equiv="encoding">
    </head>
    <body>
        <h1 style='font-style: italic; color:navy;'>Bienvenidos!</h1>
        <h2>Estos son los archivos disponibles en el directorio raiz:</h2>
        <div>
            {lista}
        </div>
    </body>
</html>'''
        with open(self.root + '/index.html', 'w') as index:
           index.write(body)
#        return 0

    def rDirList(self, ldir, dir):
        ldir.sort(key=lambda elem: elem.find('.') == -1)
        for elem in ldir:
            rDir = dir.replace(self.root, '')
            if elem.find('.') != -1:
                self.lista += f'\n<ul><a href=\'{rDir}/{elem}\'>{elem}</a></ul>'
            else:
                self.lista += f'<ul>\\{elem}'
                self.rDirList(os.listdir(dir+'/'+elem), dir+'/'+elem)
        self.lista += '</ul>'
        return self.lista + '</ul>'
