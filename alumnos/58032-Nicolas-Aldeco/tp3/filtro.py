# Filtro de Colores RGB y Blanco y Negro, para imagenes ppm#
from concurrent.futures import ThreadPoolExecutor


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
        while True:
            lectura = imagen.read(self.bloque)
            if not lectura:
                break
            for p, b in enumerate(lectura):
                if p % 3 == 0 and p != 0:
                    body.append(pix)
                    pix = []
                pix.append(b)
            return body

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
            return pixel
        else:
            suma = pixel[0] + pixel[1] + pixel[2]
            newValue = suma/3
            mod = newValue * self.inten
            if mod < 256:
                newValue = int(mod)
            else:
                newValue = 255
            for n in range(3):
                pixel[n] = int(newValue)
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
        return header_end, width, height, max_c, comments, bytearray(header, 'utf8')

    def listtobytes(self, lista):
        byte = bytearray()
        for n in lista:
            byte.append(n)
        return byte

    def main(self):
        hilos = ThreadPoolExecutor()
        newImg = []
        # Incerto cabecera de imagen:
        for by in self.cabecera[5]:
            newImg.append(by)
        print(newImg)
        with open(self.imagen, 'rb') as img:
            img.seek(self.cabecera[0])
            bloqF = []
            while True:
                try:
                    for pixel in self.lectura(img):
                        _worker = hilos.submit(self.filter, pixel)
                        newPix = _worker.result()
                        for n in range(3):
                            bloqF.append(newPix[n])
                    # print(bloqF)
                except:
                    break
            print('out')


        # for pos, pix in enumerate(listPixels):
        #     listPixels[pos] = self.filter(pix)
        # newBody = []
        # for pix in listPixels:
        #     for j in pix:
        #         newBody.append(j)
        # newBytes = self.listtobytes(newBody)
        # newImg.write(newBytes)


# TESTING#
if __name__ == "__main__":
    obj = Filtro('dog.ppm', 'b&w', 1.3, 255)
    # newImg = open('f_dog.ppm', 'wb')
    # newImg.write(b'P6\n# Imagen ppm\n200 298\n255\n')
    obj.main()
