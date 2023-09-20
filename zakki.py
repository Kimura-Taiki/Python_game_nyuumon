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
l = [[0, 1, 0], [1, 0, 1], [1, 1, 1]]
print(type(l))
print(np.sum(l))
print(sum(sum(i) for i in l))