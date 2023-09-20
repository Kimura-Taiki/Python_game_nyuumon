import pytest
import random
import numpy as np
from functools import partial
# Gooness of fit test 適合度検定に使うライブラリ
from scipy.stats import chisquare 
from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.scenes.field_wfi import make_dungeon
# from mod.initialize.commethod import pipeline_each

class Test_Tameshi():
    @classmethod
    def setup_class(cls):
        cls.arr = make_dungeon(maze_w=11, maze_h=9)
        print("作った配列は・・・")
        print(cls.arr)

    def test_true(cls):
        assert True