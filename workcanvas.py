import Tkinter
import Queue
from PIL import Image, ImageDraw, ImageTk

def get_pt(event, waiting_clicks, waiting_func):
    if waiting_clicks > 0:
        x, y = event.x, event.y
        clickstack.put((x, y))
        waiting_clicks -= 1
        if waiting_clicks == 0:
            waiting_func()


def drawline(waiting_clicks, waiting_func):
    def draw():
        src = clickstack.get_nowait()
        dst = clickstack.get_nowait()
        print src, dst

    waiting_clicks = 2
    waiting_func = draw

root = Tkinter.Tk()

width, height = 512, 512
canvas = Tkinter.Canvas(width=width, height=height)
linebutton = Tkinter.Button(root, text="linha", command=drawline)
rotatebutton = Tkinter.Button(root, text="rotacao", command=drawline)
mirrorbutton = Tkinter.Button(root, text="espelhar", command=drawline)
movebutton = Tkinter.Button(root, text="translacao", command=drawline)
canvas.pack()
linebutton.pack()
rotatebutton.pack()
mirrorbutton.pack()
movebutton.pack()

clickstack = Queue.Queue()
waiting_clicks = 0
waiting_func = None
image = Image.new('1', (width, height), '#cdcdcd')
image_draw = ImageDraw.Draw(image)
canvas._image_tk = ImageTk.PhotoImage(image)
canvas._image_id = canvas.create_image(0, 0, image=canvas._image_tk, anchor='nw')
canvas.tag_bind(canvas._image_id, "<Button-1>", lambda e: get_pt(e, waiting_clicks, waiting_func))

root.mainloop()
