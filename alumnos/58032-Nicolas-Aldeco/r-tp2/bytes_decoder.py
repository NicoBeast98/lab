class Decoder():
    def __init__(self, mensaje):
        if mensaje is bytes:
            # Pasar bytes a string
            return str(mensaje)
        else:
            # Pasar string a bytes
            bStr = bin(byte)
            bStr = bStr.lstrip('0b')
            largo = len(bStr)
            if largo < 8:
                strInv = bStr[::-1]
                emptys = 8 - largo
                for n in range(emptys):
                    strInv += '0'
                bStr = strInv[::-1]
            return bStr

e = Decoder(b'hola')
print(e)
