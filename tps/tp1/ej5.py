def fibo(n, a=0, b=1):
    while n != 0:
        return fibo(n-1, b, a+b)
    return a


for i in range(0, 10):
    print(fibo(i))

'''
        Este programa contiene 2 partes, una funcion que genera un termino
    de la serie de fibonacci y la segunda imprime los terminos
    de la serie hasta el decimo termino.
        La funcion fibo es recursiva ya que se llama a si misma, esta recibe
    un numero 'n' que es el termino de la serie que queremos calcular.
        El bucle 'for' le envia a la funcion fibo el termino que quiere
    calcular y luego imprime el valor que le devuelve la funcion.
'''
