    # 改行を半角4つにするためのコメント欄だよ

# # import 雑記.輸入
# from 雑記.輸入 import yunyuu1
# import 雑記.輸入
# print("ここは雑記だよー")
# 雑記.輸入.yunyuu1()
# yunyuu1()
# 雑記.輸入.yunyuu2()
# yunyuu2()

# # Enum型要素追加のテスト
# from enum import Enum
# class Nizi(Enum):
#     RED = 1
#     ORANGE = 2
#     YELLOW = 3
#     GREEN = 4
#     BLUE = 5
#     INDIGO = 6
#     VIOLET = 7

# for col in Nizi:
#     print(col)

# # 参考サイト
# # https://www.sejuku.net/blog/24122
# gogyou = {}
# gogyou[Nizi.RED] = "朱雀"
# gogyou[Nizi.YELLOW] = "白虎"
# gogyou[Nizi.GREEN] = "青龍"
# gogyou[Nizi.BLUE] = "玄武"
# gogyou[Nizi.GREEN] = "蒼龍"
# print([gogyou[col] for col in Nizi if col in gogyou.keys()])

# import random
# random.seed(0)
# for i in range(10):
#     # random.seed(0)
#     print(random.randint(0, 99))


import numpy as np
from scipy import linalg
from scipy.stats import chisquare

# χ二乗検定を試してみる
# 参考 https://toukei.link/programmingandsoftware/statistics_by_python/chisqtest_by_python/
# wiki https://ja.wikipedia.org/wiki/%E3%82%AB%E3%82%A4%E4%BA%8C%E4%B9%97%E6%A4%9C%E5%AE%9A

a = np.arange(12).reshape((3, 4))
print(a[1, :])
a[:, 0::4-1] = 0
print(a)


# titleのmake_dungeon
    dungeon = put_event(make_dungeon(MAZE_W, MAZE_H))
    put_protag(dungeon)
    floor = 0
    floor += 1
    if floor > fl_max:
        fl_max = floor
    welcome = 15
    pl_lifemax = 300
    pl_life = pl_lifemax
    pl_str = 100
    food = 300
    potion = 0
    blazegem = 0
    scene_change(Idx.FIELD_WFI)
    pygame.mixer.music.load("Chapter12/sound/ohd_bgm_field.ogg")
    pygame.mixer_music.play(-1)

# on_stairsのmake_dungeon
    global floor, fl_max, welcome, dungeon
    draw_dungeon(screen, fontS)
    pygame.draw.rect(screen, BLACK, [0, 0, 880, 720])
    floor += 1
    if floor > fl_max:
        fl_max = floor
    welcome = 15
    dungeon = put_event(make_dungeon(MAZE_W, MAZE_H))
    put_protag(dungeon)
