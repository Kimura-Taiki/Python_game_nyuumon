print("共通変数")
a = 1
b = 2
c = 3

def kyoutuu():
    print("共通変数側のa={}, b={}, c={}".format(a, b, c))

class K():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

k = K(1, 2)