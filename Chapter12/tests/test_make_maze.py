import pytest
import numpy as np
from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.scenes.field_wfi import set_wall

# 試しにnumpyも導入してみたよ
# 参考 https://avinton.com/academy/python-numpy-tutorial-japanese/

class Test_SetWall():
    @classmethod
    def setup_class(cls):
        cls.arr = np.zeros((3,5))
        cls.arr = set_wall(mz=cls.arr, x=3, y=2)
        cls.arr = set_wall(mz=cls.arr, x=0, y=0)
        cls.arr = set_wall(mz=cls.arr, x=1, y=0)
        cls.arr = set_wall(mz=cls.arr, x=1, y=0)
        print("作った配列は・・・")
        print(cls.arr)

    @classmethod
    def teardown_class(cls):
        cls.arr = []
        print("ティアーダウンしたよ")
    
    def test_wall_sum(cls):
        assert np.sum(cls.arr) == 3

    def test_is_wall(cls):
        assert cls.arr[2][3] == 1

    def test_is_not_wall(cls):
        assert cls.arr[0][2] == 0