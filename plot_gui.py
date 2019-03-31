from tkinter import *

top = Tk()
btn = Button()
btn.pack()
btn['text'] = '222'
def clicked():
    print('i was clicked')

btn['command'] = clicked

top.mainloop()
