import Tkinter
import Queue
import math
from PIL import Image, ImageDraw, ImageTk
import transformation

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

def _zoom(clickstack, canvas, img):
    vx1 = clickstack.get_nowait()
    vx2 = clickstack.get_nowait()
    transformation.zoom(img, canvas, vx1, vx2)


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
    image_draw = ImageDraw.Draw(img)
    image_draw.ellipse([vx2, vx1], outline='black')
    canvas._image_tk = ImageTk.PhotoImage(img)
    canvas.itemconfigure(canvas._image_id, image=canvas._image_tk)


def _clear(img, canvas):
    transformation.clear(img, canvas)


def _move(img, canvas):
    def press(xtext, ytext):
        top.destroy()
        transformation.move(img, canvas, int(xtext), int(ytext))

    top = Tkinter.Toplevel(width=300, height=300)
    top.title('Translacao')

    msg = Tkinter.Message(top, text='Coordenadas de Translacao:')
    msg.pack()

    xlabel = Tkinter.Label(top, text='X:')
    xentry = Tkinter.Entry(top)
    xentry.insert(0, '0')
    ylabel = Tkinter.Label(top, text='Y:')
    yentry = Tkinter.Entry(top)
    yentry.insert(0, '0')

    xlabel.pack()
    xentry.pack()
    ylabel.pack()
    yentry.pack()

    button = Tkinter.Button(
        top, text="Transladar", command=lambda: press(
            xentry.get(), yentry.get()))
    button.pack()


def _scale(img, canvas):
    def press(xtext, ytext):
        top.destroy()
        transformation.scale(img, canvas, float(xtext), float(ytext))

    top = Tkinter.Toplevel(width=300, height=300)
    top.title('Mudanca de Escala')

    msg = Tkinter.Message(top, text='Taxas de Transformacao:')
    msg.pack()

    xlabel = Tkinter.Label(top, text='X:')
    xentry = Tkinter.Entry(top)
    xentry.insert(0, '1.0')
    ylabel = Tkinter.Label(top, text='Y:')
    yentry = Tkinter.Entry(top)
    yentry.insert(0, '1.0')

    xlabel.pack()
    xentry.pack()
    ylabel.pack()
    yentry.pack()

    button = Tkinter.Button(
        top, text="Mudar Escala", command=lambda: press(
            xentry.get(), yentry.get()))
    button.pack()


def _rotate(img, canvas):
    def press(atext):
        top.destroy()
        transformation.rotate(img, canvas, float(atext))

    top = Tkinter.Toplevel(width=300, height=300)
    top.title('Rotacao')

    msg = Tkinter.Message(top, text=('Angulo em graus (angulos negativos '
                                     'para giro anti-horario):'))
    msg.pack()

    alabel = Tkinter.Label(top, text='X:')
    aentry = Tkinter.Entry(top)
    aentry.insert(0, '0.0')

    alabel.pack()
    aentry.pack()

    button = Tkinter.Button(
        top, text="Rotacionar", command=lambda: press(
            aentry.get()))
    button.pack()


def main():
    root = Tkinter.Tk()
    root.title('Trabalho de CG')
    eventmng = WaitingEv()

    canvas = Tkinter.Canvas(width=CANVASWIDTH, height=CANVASHEIGHT)
    eventmng.canvas = canvas
    image = Image.new('1', (CANVASWIDTH, CANVASHEIGHT), '#ffffff')
    eventmng.img = image
    drawpane = Tkinter.Frame(root)
    transpane = Tkinter.Frame(root)
    clearbutton = Tkinter.Button(drawpane, text="limpar",
                                 command=lambda: _clear(image, canvas))
    linebutton = Tkinter.Button(drawpane, text="linha",
                                command=lambda: eventmng.set_waitingf(
                                    2, _drawline))
    rectbutton = Tkinter.Button(drawpane, text="retangulo",
                                command=lambda: eventmng.set_waitingf(
                                    2, _drawrect))
    zoombutton = Tkinter.Button(transpane, text="zoom",
                                command=lambda: eventmng.set_waitingf(
                                    2, _zoom))
    trianbutton = Tkinter.Button(drawpane, text="triangulo",
                                 command=lambda: eventmng.set_waitingf(
                                     3, _drawtrian))
    circlebutton = Tkinter.Button(drawpane, text="circulo",
                                  command=lambda: eventmng.set_waitingf(
                                      2, _drawcircle))
    rotatebutton = Tkinter.Button(transpane, text="rotacao",
                                  command=lambda: _rotate(image, canvas))
    scalebutton = Tkinter.Button(transpane, text="escala",
                                 command=lambda: _scale(image, canvas))
    movebutton = Tkinter.Button(transpane, text="translacao",
                                command=lambda: _move(image, canvas))
    canvas.pack(side=Tkinter.TOP)
    transpane.pack(side=Tkinter.BOTTOM)
    drawpane.pack(side=Tkinter.BOTTOM)
    clearbutton.pack(side=Tkinter.RIGHT)
    linebutton.pack(side=Tkinter.RIGHT)
    rectbutton.pack(side=Tkinter.RIGHT)
    zoombutton.pack(side=Tkinter.RIGHT)
    trianbutton.pack(side=Tkinter.RIGHT)
    circlebutton.pack(side=Tkinter.RIGHT)
    rotatebutton.pack(side=Tkinter.RIGHT)
    scalebutton.pack(side=Tkinter.RIGHT)
    movebutton.pack(side=Tkinter.RIGHT)

    canvas._image_tk = ImageTk.PhotoImage(image)
    canvas._image_id = canvas.create_image(0, 0, image=canvas._image_tk, anchor='nw')
    canvas.tag_bind(canvas._image_id, "<Button-1>", lambda e: get_pt(e, eventmng))

    root.mainloop()

if __name__ == "__main__":
    main()
