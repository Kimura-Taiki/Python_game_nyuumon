def f1(x=1, y=2):
  return x, y
def f2(d=(1,2)):
  return d
def f3(d=[1,2]):
  return d
def f4():
  return 1, 2
def f5():
  return (1, 2)
def f6():
  return [1, 2]
print(type(f1()))
print(type(f2()))
print(type(f3()))
print(type(f4()))
print(type(f5()))
print(type(f6()))
