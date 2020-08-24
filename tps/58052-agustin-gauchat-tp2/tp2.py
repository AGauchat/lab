#!/usr/bin/python3
import os
import argparse
import array
import time
import threading
from frombit import frombits
from tobit import tobits
from mensaje import mensa
from rot13 import *

#0-------------argumentos----------------------0
try:
    # Argumentos
    parser = argparse.ArgumentParser(description='Tp2 - procesa ppm')
    parser.add_argument('-s', '--size', type=int, help='Bloque de lectura')
    parser.add_argument('-f', '--file', help='Archivo a procesar')
    parser.add_argument('-m', '--message', help='Mensaje Esteganográfico')
    parser.add_argument('-c', '--cifrado', action="store_true", help='cifrar el mensaje')
    parser.add_argument('-p', '--pixels', type=int, help='offset en pixels del inicio del raster')
    parser.add_argument('-i', '--interleave', type=int, help='interleave de modificacion en pixel')
    parser.add_argument('-o', '--output', help='estego-mensaje')

    args = parser.parse_args()
except:
    print("ERROR - Argumentos invalidos")
    exit(2)
    
#0-----------------------------------0

class Esteganografia():
    def __init__(self):
        self.a = 0
        self.cont = 0
        self.mens = ""
        self.sis = 0
        self.offs = 0
        self.header = ""
        self.body = ""
        self.imageInt = []

    def volv(self):
        self.cont = 0

    #0---------------mensaje--------------------0
    def MensajeBit(self):
        try:
            self.mens = mensa(args.message, args.cifrado)[0]
            self.sis = mensa(args.message, args.cifrado)[1]
            self.offs = args.pixels * 3
        except:
            print("ERROR - No se encontro el mensaje")
            exit(2)


    #0-----------------------------------0

    #0------------primeros pasos imagen-----------------------0
    def ImagenArreglo(self):
        try:
            print("Se esta leyendo el archivo")

            #Abro la imagen y la leo
            imagen = open(args.file, "rb").read()

            #Fuera comentarios
            for num in range(imagen.count(b"\n# ")):
                com1 = imagen.find(b"\n# ")
                com2 = imagen.find(b"\n", com1 + 1)
                imagen = imagen.replace(imagen[com1:com2], b"")

            finHeader = imagen.find(b"\n", imagen.find(b"\n", imagen.find(b"\n") + 1) + 1) + 1

            #Guardo el header y el body
            self.header = ""

            for letra in imagen[:finHeader].decode():
                if (letra == "6" and args.cifrado == True):
                    self.header += "6\n#UMCOMPU2" + "C" + " " + str(args.pixels) + " " + str(args.interleave) + " " + str(self.sis)
                elif (letra == "6"):
                    self.header += "6\n#UMCOMPU2 " + str(args.pixels) + " " + str(args.interleave) + " " + str(self.sis) + " "
                else:
                    self.header += letra

            # for i in imagen[:finHeader].decode():
            #     if i == "6":
            #         if len(str(self.sis)) >= 3:
            #             self.header += "6\n#UMCOMPU2" + " " + str(self.offs) + " " + "2" + " " + str(self.sis)
            #         else:
            #             self.header += "6\n#UMCOMPU2" + " " + str(self.offs) + " " + "2" + " " + str(self.sis) + " "
            #     else:
            #         self.header += i

            self.body = imagen[finHeader:]

            #Pixeles a int
            self.imageInt = [i for i in self.body]
        except:
            print("ERROR - No se encontro la imagen")
            exit(2)


        #0-----------------------------------0

    #0-------------modificar bits----------------------0
    def ModifBits(self):
        try:
            for i in range(len(self.mens)):
                if i == 0:
                    bit = tobits(str(self.imageInt[self.offs]), self.mens[i])
                    bitas = frombits(bit)
                    self.imageInt[self.offs] = int(bitas)
                else:
                    if self.cont == 2:
                        if (args.interleave != 1):
                            self.offs = self.offs + self.a + ((args.interleave - 1) * 3)
                            self.a = 0
                            bit = tobits(str(self.imageInt[self.offs]), self.mens[i])
                            bitas = frombits(bit)
                            self.imageInt[self.offs] = int(bitas)
                            self.volv()
                        else:
                            bit = tobits(str(self.imageInt[self.offs + self.a]), self.mens[i])
                            bitas = frombits(bit)
                            self.imageInt[self.offs + self.a] = int(bitas)
                            self.volv()

                    else:
                        self.a += (3 * args.interleave) 
                        self.cont += 1
                        bit = tobits(str(self.imageInt[self.offs + self.a]), self.mens[i])
                        bitas = frombits(bit)
                        self.imageInt[self.offs + self.a] = int(bitas)
                self.offs += 1
        except:
            print("ERROR - No se pudo completar la nueva imagen")
            exit(2)


    #0-----------------------------------0

    #0--------------guardo la imagen---------------------0
    def Guardar(self):
        try:
            imagenMensaje = array.array('B', [i for i in self.imageInt])

            with open(args.output, "wb", os.O_CREAT) as x:
                    x.write(bytearray(self.header, 'ascii'))
                    imagenMensaje.tofile(x)
                    x.close()
        except:
            print("ERROR - Error al guardar la imagen")
            exit(2)

    #0-----------------------------------0

    def Hilos(self):
        try:
            h1 = threading.Thread(target=self.MensajeBit())
            h2 = threading.Thread(target=self.ImagenArreglo())
            h3 = threading.Thread(target=self.ModifBits())
            h4 = threading.Thread(target=self.Guardar())

            h1.start()
            h2.start()
            h3.start()
            h4.start()

            h1.join()
            h2.join()
            h3.join()
            h4.join()
        except:
            print("ERROR - No se pudo iniciar el programa")
            exit(2)

obj = Esteganografia()

obj.Hilos()
