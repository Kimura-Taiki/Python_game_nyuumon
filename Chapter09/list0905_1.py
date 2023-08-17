import tkinter

neko = [
    [1, 0, 0, 0, 0, 0, 7, 7],
    [0, 2, 0, 0, 0, 0, 7, 7],
    [0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 3, 4, 5, 6]
]

def draw_neko():
    for y in range(10):
        for x in range(8):
            if neko[y][x]:
                cvs.create_image(x*72+60, y*72+60, image=img_neko[neko[y][x]], tag="NEKO")

def drop_neko():
    for y in range(8, -1, -1):
        for x in range(8):
            if neko[y][x] != 0 and neko[y+1][x] == 0:
                neko[y+1][x] = neko[y][x]
                neko[y][x] = 0

def game_main():
    drop_neko()
    cvs.delete("NEKO")
    draw_neko()
    root.after(100, game_main)

root = tkinter.Tk()
root.title("ネコを落下させる")
# root.resizable(False, False)
cvs = tkinter.Canvas(root, width=912, height=768)
cvs.pack()

bg = tkinter.PhotoImage(file="Chapter09/neko_bg.png")
img_neko = [
    None,
    tkinter.PhotoImage(file="Chapter09/neko1.png"),
    tkinter.PhotoImage(file="Chapter09/neko2.png"),
    tkinter.PhotoImage(file="Chapter09/neko3.png"),
    tkinter.PhotoImage(file="Chapter09/neko4.png"),
    tkinter.PhotoImage(file="Chapter09/neko5.png"),
    tkinter.PhotoImage(file="Chapter09/neko6.png"),
    tkinter.PhotoImage(file="Chapter09/neko_niku.png")
]

cvs.create_image(456, 384, image=bg)
game_main()
root.mainloop()