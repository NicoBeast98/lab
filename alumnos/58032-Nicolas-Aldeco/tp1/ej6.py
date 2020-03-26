class List():
    def __init__(self):
        self.lista = []

    def make_list(self, string):
        aux = ''
        for i in string:
            try:
                if int(i):
                    aux += i
            except:
                if i == ',':
                    self.lista.append(int(aux))
                    aux = ''
                else:
                    continue

    def order_list(self):
        for i in range(1, len(self.lista)):
            for j in range(0, len(self.lista)-i):
                if(self.lista[j+1] > self.lista[j]):
                    aux = self.lista[j]
                    self.lista[j] = self.lista[j+1]
                    self.lista[j+1] = aux


use = List()
print('Ingrese una lista de numeros:')
ingreso = input('>')
ingreso += ','
use.make_list(ingreso)
use.order_list()
print(use.lista)
