import math

def ToBinaryIn(num):
    if num == 0:
        return 0
    
    return ToBinaryIn(num - math.pow(2, math.floor(math.log2(num))))

def ToBinary(num):
    return str(ToBinaryIn(num))

print(ToBinary(5))