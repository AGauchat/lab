import os


class Respuesta():

    def __init__(self, dicc):
        self.root = os.getcwd() + dicc['root']
        self.port = dicc['port']
        self.size = dicc['size']
        self.ip = dicc['ip']

        self.content = {
            ".txt": " text/plain",
            ".jpg": " image/jpeg",
            ".ppm": " image/x-portable-pixmap",
            ".html": " text/html",
            ".pdf": " application/pdf",
            }

    def Header(self, cType, lenth):
        head = 'HTTP/1.1 200 OK\r\n'
        cont = f'Content-type:{cType}\r\n'
        lent = f'Content-length:{lenth}'
        head += cont + lent + '\r\n\r\n'
        return head.encode('utf8')

    def Icon(self):
        head = self.Header(
            self.content['.ico'], os.stat('favicon.ico').st_size)
        return head

    def error404(self):
        head = b'HTTP/1.1 404 Not Found\r\n\r\n'
        body = open('error404.html', 'rb').read()
        return head+body

    def error500(self):
        head = b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
        body = open('error500.html', 'rb').read()
        return head+body

    def verifArchivo(self, archivo):
        if archivo.find('.') != -1:
            lis = list(archivo.partition('.'))
            nombre = lis[0]
            exten = '.'+lis[2]
            dire = self.root+nombre+exten
        archivoEx = os.path.isfile(dire)
        if archivoEx is False:
            return [404, self.error404()]
        try:
            size = os.stat(dire).st_size
            head = self.Header(self.content[exten], size)
            return [200, head]
        except:
            return [500, self.error500()]
