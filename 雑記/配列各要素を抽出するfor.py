print("配列各要素を抽出するfor.py です")
li = [[1, 2]]
for a, b, in li:
    print("a="+str(a)+" : b="+str(b))

def f():
    return "B", 80

print(list(f()))