with open("/home/nico98/Compu2/lab/tps/tp1/lista.txt", "r") as texto:
    class History():
        def __init__(self):
            self.numbers = []

        def enteros(self, num):
            try:
                if int(num) > 0:
                    self.numbers.append(int(num))
                    return 'int'
            except:
                return 'not_int'
    record = History()
    for i in texto:
        c = record.enteros(i)
        print(c)
    print('Los numeros en el archivo son:')
    print(record.numbers)