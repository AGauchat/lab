#!/usr/bin/python3
from socketserver import ForkingTCPServer
import socketserver
import os
from os import remove
import argparse
from filtro import *

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        dic={"txt":" text/plain","jpg":" image/jpeg","ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}
        self.data = self.request.recv(1024)
        encabezado = self.data.decode().splitlines()[0]
        archivo = "." + encabezado.split()[1]

        # print(encabezado)
        # print(archivo)

        if archivo.find('favicon.ico') != -1:
            self.request.sendall(open('/home/agustin/Computacion II/lab/tps/58052-agustin-gauchat-tp3/favicon.ico', 'rb').read())
        else:
            try:
                if archivo == './':
                    archivo = '/home/agustin/Computacion II/lab/tps/58052-agustin-gauchat-tp3/index.html'
                    extension = 'html'
                else:
                    extension = archivo.split('.')[2]

                    if archivo.find("ppm") != -1:
                        extension = "ppm"
                        color = archivo.split("?")[1].split("=")[0]
                        intensidad = archivo.split("?")[1].split("=")[1]
                        archivo = archivo.split("?")[0]
                        
                        imagen = Filtro(archivo, color, str(intensidad), 255).main()

                        image = open("/home/agustin/Computacion II/lab/tps/58052-agustin-gauchat-tp3/temp.ppm", "wb")
                        image.write(imagen)
                        image.close

                        archivo = '/home/agustin/Computacion II/lab/tps/58052-agustin-gauchat-tp3/temp.ppm'
                    else:
                        archivo = '/home/agustin/Computacion II/lab/tps/58052-agustin-gauchat-tp3/' + archivo.split("/")[1]

                fd = os.open(archivo, os.O_RDONLY)
                body = os.read(fd, os.path.getsize(archivo))
                os.close(fd)

                if archivo.find("ppm") != -1:
                    remove('/home/agustin/Computacion II/lab/tps/58052-agustin-gauchat-tp3/temp.ppm')

                header = bytearray("HTTP/1.1 200 OK\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
                self.request.sendall(header)
                self.request.sendall(body)
    
            except:
                archivo = '/home/agustin/Computacion II/lab/tps/58052-agustin-gauchat-tp3/404error.html'
                extension = 'html'
                    
                fd = os.open(archivo, os.O_RDONLY)
                body = os.read(fd, os.path.getsize(archivo))
                os.close(fd)
                header = bytearray("HTTP/1.1 404 Not Found\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
                self.request.sendall(header)
                self.request.sendall(body)


# socketserver.ForkingTCPServer.allow_reuse_address = True
# server =  socketserver.TCPServer(("0.0.0.0", 8080), Handler)
# server.serve_forever()

parser = argparse.ArgumentParser(description='Tp3 - Servidor', usage='./server.py -r [ruta de documentos] -p [puerto] -s [bloque de lectura]')
parser.add_argument('-r', '--root', type=str, help='Ruta', default='/root')
parser.add_argument('-p', '--port', type=int, nargs=1, help='Puerto', default=[8081])
parser.add_argument('-s', '--size', type=int, help='Bloque de lectura', default=[255])

args = parser.parse_args()

with ForkingTCPServer(('0.0.0.0', args.port[0]), Handler) as server:
    server.allow_reuse_address = True
    server.serve_forever()