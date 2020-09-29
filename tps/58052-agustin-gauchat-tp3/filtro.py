# Filtro de Colores RGB y Blanco y Negro, para imagenes ppm#
from concurrent import futures


class Filtro():

    def __init__(self, imagen, filtro, intensidad, bloque):
        self.imagen = imagen
        self.inten = int(intensidad)
        self.cabecera = self.head(imagen)
        self.newImg = bytearray()

        if bloque % 3 != 0:
            self.bloque = bloque - bloque % 3
        else:
            self.bloque = bloque

        if filtro == 'red':
            self.filtro = 0
        elif filtro == 'green':
            self.filtro = 1
        elif filtro == 'blue':
            self.filtro = 2
        elif filtro == 'b&w':
            self.filtro = 3

    # Funcion que lee el bloque, en bytes, que se le envia y devuelve una matriz de pixeles
    def lectura(self, imagen):
        bloq = []
        pix = []
        while True:
            lectura = imagen.read(self.bloque)
            if not lectura:
                break
            for p, b in enumerate(lectura):
                if p % 3 == 0:
                    bloq.append(pix)
                    pix = []
                pix.append(b)
        bloq.pop(0)
        return bloq

    # Filtro de colores e intensidad
    def filter(self, pixel):
        if self.filtro != 3:
            for pos, by in enumerate(pixel):
                if pos == self.filtro:
                    mod = pixel[pos] * self.inten
                    if mod < 256:
                        pixel[pos] = int(mod)
                    else:
                        pixel[pos] = 255
                else:
                    pixel[pos] = 0
        else:
            suma = pixel[0] + pixel[1] + pixel[2]
            newValue = suma/3
            mod = int(newValue * self.inten)
            if mod < 256:
                newValue = mod
            else:
                newValue = 255
            for n in range(3):
                pixel[n] = newValue
        return pixel

    # Cabecera de imagen ppm
    def head(self, file):
        img = open(file, 'rb')
        lines = img.read(100).splitlines()
        comments = []
        header_end = 0
        for line in lines:
            if line == b"P6":
                header_end += len(line) + 1
            elif line[0] == ord("#"):
                comments.append(line)
                header_end += len(line) + 1
            elif len(line.split()) == 2:
                words = line.split()
                width = int(words[0])
                height = int(words[1])
                header_end += len(line) + 1
            else:
                max_c = int(line)
                header_end += len(line) + 1
                break
        header = f'P6\n{width} {height}\n{max_c}\n'
        return header_end, width, height, max_c, comments, bytearray(header, 'utf-8')

    def listtobytes(self, lista):
        byte = bytearray()
        for n in lista:
            byte.append(n)
        return byte

    def main(self):
        hilos = futures.ThreadPoolExecutor(max_workers=6)
        hilosB = futures.ThreadPoolExecutor(max_workers=6)
        bloqF = []
        # Incerto cabecera en nueva imagen
        for by in self.cabecera[-1]:
            self.newImg.append(by)
        # ----
        with open(self.imagen, 'rb') as img:
            img.seek(self.cabecera[0])
            _lec = hilos.submit(self.lectura, img)
            for pix in _lec.result():
                _worker = hilosB.submit(self.filter, pix)
                bloqF.append(_worker.result())
        for pix in bloqF:
            for by in pix:
                self.newImg.append(by)
        return self.newImg


# TESTING#
# if __name__ == "__main__":
#     obj = Filtro('/home/agustin/Computacion II/lab/tps/58052-agustin-gauchat-tp3/dog.ppm', 'b&w', 1, 1000)
#     newImg = open('f_dog.ppm', 'wb')
#     newImg.write(obj.main())
