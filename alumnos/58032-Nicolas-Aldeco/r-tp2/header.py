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
