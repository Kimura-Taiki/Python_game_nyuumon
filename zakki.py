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
a[1, :] = 0
print(a)
