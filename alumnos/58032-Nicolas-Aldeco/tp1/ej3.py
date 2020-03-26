import os


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


num = '0'
play = History()
while num != 'exit':
    print('Ingrese numeros enteros para que los almacene')
    print('cuando termine ingrese \'exit\'')
    num = input('>')
    if num != 'exit':
        state = play.enteros(num)
        print(state)
        input()
    os.system('clear')
print('Los enteros ingresados fueron:')
print(play.numbers)
