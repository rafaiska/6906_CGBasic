import Tkinter
from PIL import Image, ImageDraw, ImageTk

def paint_img(event, canvas):
    x, y = event.x, event.y
    image_draw.ellipse((x-5, y-5, x+5, y+5), fill='black')
    canvas._image_tk = ImageTk.PhotoImage(image)
    canvas.itemconfigure(canvas._image_id, image=canvas._image_tk)

root = Tkinter.Tk()

width, height = 800, 600
canvas = Tkinter.Canvas(width=width, height=height)
canvas.pack()

image = Image.new('RGB', (width, height), '#cdcdcd')
image_draw = ImageDraw.Draw(image)
canvas._image_tk = ImageTk.PhotoImage(image)
canvas._image_id = canvas.create_image(0, 0, image=canvas._image_tk, anchor='nw')
canvas.tag_bind(canvas._image_id, "<Button-1>", lambda e: paint_img(e, canvas))

root.mainloop()
