import os


class ServerTools():

    def __init__(self, argms):
        self.root = os.getcwd() + argms.root[0]
        self.port = argms.port[0]
        self.size = argms.size[0]
        self.ip = argms.ip[0]

        self.prot_ip = 'IPv4'
        if argms.ip[0].find(':') != -1:
            self.prot_ip = 'IPv6'

        # Tipos de contenido aceptados:
        self.content = {
            ".txt": " text/plain",
            ".jpg": " image/jpeg",
            ".ppm": " image/x-portable-pixmap",
            ".html": " text/html",
            ".pdf": " application/pdf",
            ".ico": " image/x-ico",
            ".mp4": " video/mp4",
            ".aac": " audio/aac"
            }

    # Respuesta de errores.
    # 400 Bad Request
    def response400(self):
        head = b'HTTP/1.1 400 Bad Request\r\n\r\n'
        body = open('errors/error400.html', 'rb').read()
        return head+body

    # 404 Not Found
    def response404(self):
        head = b'HTTP/1.1 404 Not Found\r\n\r\n'
        body = open('errors/error400.html', 'rb').read()
        return head+body

    # 415 Unsopported Media Type
    def response415(self):
        head = b'HTTP/1.1 415 Unsupported Media Type\r\n\r\n'
        body = open('errors/error400.html', 'rb').read()
        return head+body

    # 500 Internal Server Error
    def response500(self):
        head = b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
        body = open('errors/error400.html', 'rb').read()
        return head+body
