import tkinter
key = 0
def key_down(e):
    global key
    key = e.keycode

def main_proc():
    label["text"] = key
    root.after(100, main_proc)

root = tkinter.Tk()
root.title("リアルタイムキー入力")
root.bind("<KeyPress>", key_down)
label = tkinter.Label(font=("Times New Roman", 80))
label.pack()
main_proc()
root.mainloop()

"""
主なキーコード(Mac)
←       8124162
↑       8320768
→       8189699
↓       8255233
Space   32
Return  2359309
A~Z     65~90
a~z     97~122
0~9     48~57
"""