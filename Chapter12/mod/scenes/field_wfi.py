def eat_food(food, pl_life, pl_lifemax):
    if food > 0:
        food -= 1
        pl_life = pl_life+1 if pl_life<pl_lifemax else pl_lifemax
    else:
        pl_life = pl_life-5 if pl_life>5 else 0
    return food, pl_life

from random import seed, randint
from functools import partial
import numpy as np
from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(dirname(__file__))))
from mod.initialize.commethod import pipeline_each

# -------------------------------- make_maze系統 --------------------------------

MAZE_SPACE = 0
MAZE_WALL = 1
MAZE_ROOM = 2

def set_wall(mz, x, y): #壁を作る
    mz[y][x] = MAZE_WALL
    return mz

def set_random_room(mz, x, y): #20%の確率で部屋を作る
    if mz[y][x] == MAZE_SPACE and randint(0, 99) < 20:
        mz[y][x] = MAZE_ROOM
    return mz

XP = [ 0, 1, 0,-1]
YP = [-1, 0, 1, 0]
def set_pillar_wall(mz, x, y): #柱の隣に壁を作る
    r = randint(0, 3) if x==2 else randint(0, 2)# １列目は四方に、２列目以降は左以外に壁を作る
    mz[y+YP[r]][x+XP[r]] = MAZE_WALL
    return mz

def make_maze(maze_w, maze_h): # ダンジョンの元となる迷路の自動生成
    maze = np.zeros((maze_h, maze_w))
    maze[0::maze_h-1, :] = MAZE_WALL
    maze[:, 0::maze_w-1] = MAZE_WALL
    maze[2:maze_h-2:2, 2:maze_w-2:2] = MAZE_WALL
    return pipeline_each(maze, 
                         [partial(set_pillar_wall, x=i, y=j) for j in range(2, maze_h-2, 2) for i in range(2, maze_w-2, 2)]+ #柱から上下左右の壁
                         [partial(set_random_room, x=i, y=j) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]) #部屋

# -------------------------------- make_dungeon系統 --------------------------------

def dig_tunnel(dgn, maze, x, y, dx, dy):
    if (maze[y][x] == MAZE_SPACE or maze[y][x] == MAZE_ROOM) and (maze[y+dy][x+dx] == MAZE_SPACE or maze[y+dy][x+dx] == MAZE_ROOM):
        dgn[y*3+1+dy][x*3+1+dx] = 0
    return dgn

def make_dungeon(maze_w, maze_h): # ダンジョンの自動生成
    maze = make_maze(maze_w, maze_h) # 元となる迷路を作る
    DUNGEON_W = maze_w*3
    DUNGEON_H = maze_h*3
    # 迷路からダンジョンを作る
    def dig_dot(dgn, x, y):
        dgn[y][x] = 0
        return dgn
    def dig_room(dgn, x, y):
        return pipeline_each(dgn, [partial(dig_dot, x=i, y=j) for j in range(y*3, y*3+3) for i in range(x*3, x*3+3)])
    # return pipeline_each([[9]*DUNGEON_W for j in range(DUNGEON_H)], 
    return pipeline_each(np.full((DUNGEON_H, DUNGEON_W), 9), 
                         [partial(dig_tunnel, maze=maze, x=i, y=j, dx=0, dy=0) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_tunnel, maze=maze, x=i, y=j, dx=0, dy=-1) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_tunnel, maze=maze, x=i, y=j, dx=0, dy=1) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_tunnel, maze=maze, x=i, y=j, dx=-1, dy=0) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_tunnel, maze=maze, x=i, y=j, dx=1, dy=0) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_room, x=i, y=j) for j in range(1, maze_h-1) for i in range(1, maze_w-1) if maze[j][i] == 2])
