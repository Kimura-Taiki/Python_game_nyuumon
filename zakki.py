    # 改行を半角4つにするためのコメント欄だよ

def f(*args):
  return args

print(f(tmr=4))

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
