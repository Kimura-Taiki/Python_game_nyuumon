import pytest
import numpy as np
from functools import partial
# Gooness of fit test 適合度検定に使うライブラリ
from scipy.stats import chisquare 
from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.scenes.field_wfi import set_wall, set_random_room, set_pillar_wall, MAZE_SPACE, MAZE_WALL, MAZE_ROOM
from mod.initialize.commethod import pipeline_each

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
        assert np.count_nonzero(cls.arr == MAZE_WALL) == 3

    def test_is_wall(cls):
        assert cls.arr[2][3] == MAZE_WALL

    def test_is_not_wall(cls):
        assert cls.arr[0][2] == 0

class Test_SetRandomRoom():
    @classmethod
    def setup_class(cls):
        cls.arr = pipeline_each(np.zeros((9, 9)), 
                                [partial(set_random_room, x=i, y=j) for j in range(9) for i in range(9)])
        print("作った配列は・・・")
        print(cls.arr)

    def test_chi(cls):
        obs = np.array([np.count_nonzero(cls.arr == MAZE_ROOM), np.count_nonzero(cls.arr == MAZE_SPACE)])
        print(obs)
        exp = np.array([16, 65])
        chi = chisquare(f_obs=obs, f_exp=exp)
        assert 0.05 < chi.pvalue

class Test_SetPillerWall():
    @classmethod
    def setup_class(cls):
        cls.arr = np.count_nonzero(
            pipeline_each(np.zeros((180, 7)), 
                          [partial(set_pillar_wall, x=i, y=j) for j in range(1, 180, 3) for i in range(2, 7, 3)]
                          ) == MAZE_WALL, axis=0)
        print("作った配列は・・・")
        print(cls.arr)

    def test_no_make_2nd_piller_left_wall(cls):
        assert cls.arr[4] == 0

    def test_chi(cls):
        obs = np.concatenate([cls.arr[1:4], cls.arr[5:]])
        print(obs)
        exp = np.array([15, 30, 15, 40, 20])
        chi =chisquare(f_obs=obs, f_exp=exp)
        assert 0.05 < chi.pvalue
