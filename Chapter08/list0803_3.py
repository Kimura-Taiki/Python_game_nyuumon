import tkinter

key = ""
def key_down(e):
    global key
    key = e.keysym
def key_up(e):
    global key
    key = ""

cx = 400
cy = 300
def main_proc():
    global cx, cy
    if key == "Up":
        cy -= 20
    if key == "Down":
        cy += 20
    if key == "Left":
        cx -= 20
    if key == "Right":
        cx += 20
    canvas.coords("MYCHR", cx, cy)  # 既に配置した画像を別の位置に置き直す命令
    root.after(100, main_proc)

root = tkinter.Tk()
root.title("キャラクターの移動")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=600, bg="lightgreen")
canvas.pack()
img = tkinter.PhotoImage(file="Chapter08/mimi.png")
canvas.create_image(cx, cy, image=img, tag="MYCHR")
main_proc()
root.mainloop()