import pytest
import random
import numpy as np
from functools import partial
# Gooness of fit test 適合度検定に使うライブラリ
from scipy.stats import chisquare 
from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.scenes.field_wfi import dig_tunnel, make_dungeon, MAZE_ROOM, MAZE_SPACE, MAZE_WALL
# from mod.initialize.commethod import pipeline_each

class Test_DigTunnel():
    @classmethod
    def setup_class(cls):
        s, w, r = MAZE_SPACE, MAZE_WALL, MAZE_ROOM
        cls.maze = np.array([
            [s, s, s, s, s, s, s, s, s],
            [r, s, r, r, r, r, r, w, r],
            [w, w, w, w, w, w, w, w, w]])
        cls.dgn = np.full((3*3, 9*3), 7)
        for i in range(1, 9, 3):
            dig_tunnel(dgn=cls.dgn, maze=cls.maze, x=i, y=1, dx=0, dy=0)
            dig_tunnel(dgn=cls.dgn, maze=cls.maze, x=i, y=1, dx=1, dy=0)
            dig_tunnel(dgn=cls.dgn, maze=cls.maze, x=i, y=1, dx=0, dy=1)
            dig_tunnel(dgn=cls.dgn, maze=cls.maze, x=i, y=1, dx=-1, dy=0)
            dig_tunnel(dgn=cls.dgn, maze=cls.maze, x=i, y=1, dx=0, dy=-1)
    
    def test_digsum(cls):
        assert np.count_nonzero(cls.dgn == 0) == 8
        assert np.count_nonzero(cls.dgn == 9) == 0
        assert np.count_nonzero(cls.dgn == 7) == 9*27-8


class Test_MakeDungeon():
    @classmethod
    def setup_class(cls):
        random.seed(0)
        cls.arr = make_dungeon(maze_w=11, maze_h=9)
        print("作った配列は・・・")
        cls.dgn = ""
        for j in cls.arr:
            for i in j:
                cls.dgn += ("**" if i == 9 else "  ")
            cls.dgn += "\n"
        print(cls.dgn)
    def test_true(cls):
        mock = """******************************************************************
******************************************************************
******************************************************************
******      ******      ******      ******************************
******                              ********              ********
******      ******      ******      ********  ********************
********************  **********************  ********************
********************  **********************  ********************
********************  **********************  ********************
******      ******      ******      ********  ********************
******                                                    ********
******      ******      ******      ******************************
******************      ******************************************
******************      ******************************************
******************      ******************************************
********************  ********************************************
********                          **********              ********
********  **********  **********  **********  **********  ********
********  **********  **********  ********      ********  ********
********  **********  **********  ********      ********  ********
********  **********  **********  ********      ********  ********
******      ******      ********  **********  **********  ********
******      ******      ********              **********  ********
******      ******      ******************************************
******************************************************************
******************************************************************
******************************************************************
"""
        assert cls.dgn == mock