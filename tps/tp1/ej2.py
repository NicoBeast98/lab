class Adder():
    def adderv2(self, num, times):
        res = 0
        for x in range(times):
            ones = '1'*times
            res += num*(int(ones))
            times -= 1
        return(res)


use = Adder()
n = int(input('Numbero >'))
t = int(input('Veces >'))
ans = use.adderv2(n, t)
print(ans)
