class Adder():
    def adder(self, num):
        return(num + num*11 + num*111)


uso = Adder()
value = int(input('Numero >'))
ans = uso.adder(value)
print(ans)