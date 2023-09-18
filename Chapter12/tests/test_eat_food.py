import sys
import os

if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# print(sys.path)

def test_hoge():
    assert True

def test_fuga():
    assert False
