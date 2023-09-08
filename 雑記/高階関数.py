print("高階関数だよ")

def a():
    print("Aだよ")

def b():
    print("Bだよ")

def c():
    print("Cだよ")

fs = [a, b, c]

for f in fs:
    f()