from enum import Enum

class TemplateColor(Enum):
    NAME = (1, "赤" ,[255, 0, 0])
    ADRESS = (2 , "緑", [0, 255, 0])
    TEL = (3 , "青", [0, 0, 255])
    
    def __init__(self, id, color_name, rgb) -> None:
        super().__init__()
        self.id = id
        self.color_name = color_name
        self.rgb = rgb

print("zzz")
print(TemplateColor.NAME.rgb)

print(TemplateColor)
for area in TemplateColor:
    area_name = area.name  # NAME , ADDRESS , TEL
    aera_rgb = area.rgb
    print(area) # rgb値を与えたら値が返ってくる素晴らしい処理


# # 関数の処理時間を計測
# from functools import wraps
# import time

# # 関数を受け取る関数を定義
# # 内部の関数を返却する
# def time_measurement(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         exe = func(*args, **kwargs)
#         end = time.time()
#         print(f"time_measurement: {end - start}")
#         return exe
#     return wrapper

# # @をつけて呼び出す（デコレータ）と、呼び出し先の関数の引数に入る
# @time_measurement
# def func(num):
#     res = 0
#     for n in range(num):
#         res += n
#     return res

# func(10000000) # time_measurement: 0.48942112922668457
