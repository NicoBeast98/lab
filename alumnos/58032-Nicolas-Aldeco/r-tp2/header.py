import os


def r_body(img):
    # Determino inicio del body
    lec = img.read(100)
    raster = lec.find(b'\n255') + 5
    return(raster)


def make_head(img, cifrado, offset, interleave, l_total):
    # Creo la nueva cabecera
    head = '#UMCOMPU2'
    if cifrado:
        head += '-C'
    head += (' {off} {inter} {l_t}\n').format(
        off=str(offset), inter=str(interleave), l_t=str(l_total)
        )
    encodeHead = head.encode('utf-8')
    # Leo cabecera de la imagen y armo nueva
    imagen = open(img, "rb").read(100)
    listed = imagen.split(b'\x0A')
    new = b''
    for pos, elem in enumerate(listed):
        if pos != len(listed)-1:
            if pos == 1:
                new += encodeHead
            new += elem + b'\n'
    return new

def readHeader(file):
    img = open(file, 'rb')
    lines = img.read().splitlines()
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

    return header_end, width, height, max_c, comments
