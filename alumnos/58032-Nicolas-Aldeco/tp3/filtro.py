# Filtro de Colores RGB y Blanco y Negro, para imagenes ppm#
from concurrent import futures


class Filtro():

    def __init__(self, imagen, filtro, intensidad, bloque):
        self.imagen = imagen
        self.inten = intensidad
        self.cabecera = self.head(imagen)

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
        body = []
        pix = []
        lectura = imagen.read(self.bloque)
        if not lectura:
            return None
        for p, b in enumerate(lectura):
            if p % 3 == 0 and p != 0:
                body.append(pix)
                pix = []
            pix.append(b)
        return body

    # Filtro de colores e intensidad
    def filter(self, bloqP):
        bloqF = []
        if self.filtro != 3:
            for pixel in bloqP:
                for pos, by in enumerate(pixel):
                    if pos == self.filtro:
                        mod = pixel[pos] * self.inten
                        if mod < 256:
                            pixel[pos] = int(mod)
                        else:
                            pixel[pos] = 255
                    else:
                        pixel[pos] = 0
                    newPixel = pixel
                for by in newPixel:
                    bloqF.append(by)
            return self.listtobytes(bloqF)
        else:
            for pixel in bloqP:
                suma = pixel[0] + pixel[1] + pixel[2]
                newValue = suma/3
                mod = int(newValue * self.inten)
                if mod < 256:
                    newValue = mod
                else:
                    newValue = 255
                for _ in range(3):
                    bloqF.append(newValue)
            return self.listtobytes(bloqF)

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
        hilos = futures.ThreadPoolExecutor()
        # Incerto cabecera en nueva imagen
        newImg = bytearray()
        for by in self.cabecera[-1]:
            newImg.append(by)
        # ----
        with open(self.imagen, 'rb') as img:
            img.seek(self.cabecera[0])
            while True:
                bloqP = self.lectura(img)
                if not bloqP:
                    break
                for pix in bloqP:
                    for by in pix:
                        newImg.append(by)
                # _worker = hilos.submit(self.filter, bloqP)
                # for by in _worker.result():
                #     newImg.append(by)
        return newImg


# TESTING#
if __name__ == "__main__":
    obj = Filtro('dog.ppm', 'red', 1.3, 100)
    newImg = open('f_dog.ppm', 'wb')
    newImg.write(obj.main())
