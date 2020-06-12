#! /usr/bin/python3
def detHeader(img):
    with open(img, 'rb') as img:
        info = img.read(100)
        header = bytearray(info)
        n_array = bytearray()
        cutted = header.split(b'\x0A')
        for n in range(3):
            n_array += bytes(cutted[n]) + b'\x0A'
        raster = len(n_array)
    return [raster, n_array]


def makeNewHeader(lista, offSet, intLeave, lenBmsg):
    tag = ('#UMCOMPU2 '+offSet+' '+intLeave+' '+lenBmsg).encode('ascii')
    newRaster = lista[0] + len(tag)
    newHead = bytearray()
    enListed = lista[1].split(b'\x0A')
    enListed.pop(len(enListed)-1)   # Elimino un \x0A de mas
    for n, by in enumerate(enListed):
        temp = by.decode()
        temp = temp.encode('ascii')
        if n == 1:
            newHead += tag + b'\x0A'
        newHead += temp + b'\x0A'
    return [newRaster, newHead]
