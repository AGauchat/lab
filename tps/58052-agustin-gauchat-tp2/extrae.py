#!/usr/bin/python3
import argparse
from frombit import *
from rot13 import *

def readHeader(file):
    image = open(file, "rb").read()
    lines = image.splitlines()
    comments = ""
    header_end = 0
    for line in lines:
        if line == b"P6":
            header_end += len(line) + 1
        elif line[0] == ord("#"):
            comments = line
            header_end += len(line) + 1
        elif len(line.split()) == 2:
            header_end += len(line) + 1
        else:
            header_end += len(line) + 1
            break

    commentsList = comments.split(b" ")

    cifrate = False
    if (commentsList[0] == b"#UMCOMPU2C"): 
        cifrate = True 
    elif (commentsList[0] == b"#UMCOMPU2"): 
        cifrate = False
    else: 
        raise Exception ("La imagen no contiene nada")

    offset = int(commentsList[1])
    interleave = int(commentsList[2])
    mensajeSize = int(commentsList[3])

    body = image[header_end:]
    imageInt = [i for i in body]

    return header_end, cifrate, offset, interleave, mensajeSize, imageInt

try:
    parser = argparse.ArgumentParser(description='Extraer mensaje')
    parser.add_argument('-f', '--file', help='Archivo a procesar')

    args = parser.parse_args()
except:
    print("ERROR - Argumentos incorrectos")
    exit(2)
# args.file = "aa.ppm"

try:
    datos = readHeader(args.file)

    headerFin = datos[0]
    cifrado = datos[1]
    offset = datos[2] * 3
    interleave = datos[3]
    mensajeSize = datos[4]
    imagen = datos[5]
except:
    print("ERROR - No se pudo obtener informacion de la imagen")
    exit(2)

listaBits = []
listabit = []
contadorBits = 0
cont = 0
a = 0
try:
    for i in range((mensajeSize * 8) + 1):
        if i == 0:
            listabit.append(int(imagen[offset] % 2))
        else:
            if cont == 2:
                if (interleave != 1):
                    offset = offset + a + ((interleave - 1) * 3)
                    listabit.append(int(imagen[offset] % 2))
                    a = 0
                    cont = 0
                else:
                    listabit.append(int(imagen[offset + a] % 2))
                    cont = 0

            else:
                a += (3 * interleave) 
                cont += 1
                listabit.append(int(imagen[offset + a] % 2))
        offset += 1
        contadorBits += 1
        if contadorBits == 8:
            listaBits.append(listabit)
            listabit = []
            contadorBits = 0
except:
    print("ERROR - No se pudo completar la extraccion del mensaje")
    exit(2)

mensaje = ""
try:
    for bite in listaBits:
        mensaje += frombits(bite)

    if cifrado:
        mensaje = rot13(mensaje)
except:
    print("ERROR - No se pudo completar el mensaje")
    exit(2)

print(mensaje)