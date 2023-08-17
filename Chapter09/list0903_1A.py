import tkinter

old_x = 0
old_y = 0

def mouse_move(e):
    global old_x, old_y
    mouse_x = e.x
    mouse_y = e.y
    if mouse_x < 24 or mouse_x >= 24+72*8 or mouse_y < 24 or mouse_y >= 24+72*10:
        return
    cursor_x = int((mouse_x-24)/72)
    cursor_y = int((mouse_y-24)/72)
    if cursor_x != old_x or cursor_y != old_y:
        cvs.delete("CURSOR")
        cvs.create_image(cursor_x*72+60, cursor_y*72+60, image=cursor, tag="CURSOR")
    old_x = cursor_x
    old_y = cursor_y

root = tkinter.Tk()
root.title("カーソルの表示")
# root.resizable(False, False) # ここを無効化するとcvs.pack()で都合良い大きさになる
root.bind("<Motion>", mouse_move)
cvs = tkinter.Canvas(root, width=912, height=768)
cvs.pack()

bg = tkinter.PhotoImage(file="Chapter09/neko_bg.png")
cursor = tkinter.PhotoImage(file="Chapter09/neko_cursor.png")
cvs.create_image(456, 384, image=bg)
root.mainloop()