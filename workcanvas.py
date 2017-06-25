import Tkinter
import Queue
import math
from PIL import Image, ImageDraw, ImageTk

CANVASWIDTH = 512
CANVASHEIGHT = 512

class WaitingEv(object):
    def __init__(self):
        self.clickstack = None
        self.waiting_clicks = 0
        self.waiting_func = None
        self.canvas = None
        self.img = None

    def set_waitingf(self, waiting_clicks, waiting_func):
        self.waiting_clicks = waiting_clicks
        self.waiting_func = waiting_func
        self.clickstack = Queue.Queue()

    def call_waitingf(self):
        self.waiting_func(self.clickstack, self.canvas, self.img)
        self.waiting_func = None

    def new_click(self, x, y):
        if self.waiting_clicks > 0:
            self.clickstack.put((x, y))
            self.waiting_clicks -= 1
            if self.waiting_clicks == 0:
                self.call_waitingf()


def get_pt(event, eventmng):
    click_x, click_y = event.x, event.y
    eventmng.new_click(click_x, click_y)


def _drawline(clickstack, canvas, img):
    src = clickstack.get_nowait()
    dst = clickstack.get_nowait()
    image_draw = ImageDraw.Draw(img)
    image_draw.line([src, dst], fill='black', width=1)
    canvas._image_tk = ImageTk.PhotoImage(img)
    canvas.itemconfigure(canvas._image_id, image=canvas._image_tk)


def _drawrect(clickstack, canvas, img):
    vx1 = clickstack.get_nowait()
    vx2 = clickstack.get_nowait()
    image_draw = ImageDraw.Draw(img)
    image_draw.rectangle([vx1, vx2], outline='black')
    canvas._image_tk = ImageTk.PhotoImage(img)
    canvas.itemconfigure(canvas._image_id, image=canvas._image_tk)


def _drawtrian(clickstack, canvas, img):
    vx1 = clickstack.get_nowait()
    vx2 = clickstack.get_nowait()
    vx3 = clickstack.get_nowait()
    image_draw = ImageDraw.Draw(img)
    image_draw.polygon([vx1, vx2, vx3], outline='black')
    canvas._image_tk = ImageTk.PhotoImage(img)
    canvas.itemconfigure(canvas._image_id, image=canvas._image_tk)


def _drawcircle(clickstack, canvas, img):
    center = clickstack.get_nowait()
    crange = clickstack.get_nowait()
    radius = math.sqrt(math.pow(crange[0] - center[0], 2) +
                       math.pow(crange[1] - center[1], 2))
    radius = int(radius)
    vx1 = (center[0] + radius, center[1] + radius)
    vx2 = (center[0] - radius, center[1] - radius)
    print vx1, vx2
    image_draw = ImageDraw.Draw(img)
    image_draw.ellipse([vx2, vx1], outline='black')
    canvas._image_tk = ImageTk.PhotoImage(img)
    canvas.itemconfigure(canvas._image_id, image=canvas._image_tk)

def main():
    root = Tkinter.Tk()
    eventmng = WaitingEv()

    canvas = Tkinter.Canvas(width=CANVASWIDTH, height=CANVASHEIGHT)
    eventmng.canvas = canvas
    linebutton = Tkinter.Button(root, text="linha",
                                command=lambda: eventmng.set_waitingf(
                                    2, _drawline))
    rectbutton = Tkinter.Button(root, text="retangulo",
                                command=lambda: eventmng.set_waitingf(
                                    2, _drawrect))
    trianbutton = Tkinter.Button(root, text="triangulo",
                                 command=lambda: eventmng.set_waitingf(
                                     3, _drawtrian))
    circlebutton = Tkinter.Button(root, text="circulo",
                                  command=lambda: eventmng.set_waitingf(
                                      2, _drawcircle))
    # rotatebutton = Tkinter.Button(root, text="rotacao", command=drawline)
    # scalebutton = Tkinter.Button(root, text="espelhar", command=drawline)
    # movebutton = Tkinter.Button(root, text="translacao", command=drawline)
    canvas.pack()
    linebutton.pack()
    rectbutton.pack()
    trianbutton.pack()
    circlebutton.pack()
    # rotatebutton.pack()
    # scalebutton.pack()
    # movebutton.pack()

    image = Image.new('1', (CANVASWIDTH, CANVASHEIGHT), '#cdcdcd')
    eventmng.img = image
    canvas._image_tk = ImageTk.PhotoImage(image)
    canvas._image_id = canvas.create_image(0, 0, image=canvas._image_tk, anchor='nw')
    canvas.tag_bind(canvas._image_id, "<Button-1>", lambda e: get_pt(e, eventmng))

    root.mainloop()

if __name__ == "__main__":
    main()
