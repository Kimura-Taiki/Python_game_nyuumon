import tkinter
key = 0
def key_down(e):
    global key
    key = e.keycode
    print("KEY:"+str(key))

root = tkinter.Tk()
root.title("キーコードを取得")
root.bind("<KeyPress>", key_down)
root.mainloop()

"""
bind()で取れる主なイベント
<KeyPress>      キーを押した
<Key>           同上
<Motion>        マウスポインタを動かした
<ButtonPress>   マウスボタンをクリックした
<Button>        同上
<Button-1>      左クリック
<Button-2>      中央クリック
<Button-3>      右クリック
"""