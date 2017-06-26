import numpy as np
from PIL import ImageTk


def clear(pilimage, canvas):
    pixels = pilimage.load()

    for i in range(pilimage.size[0]):
        for j in range(pilimage.size[1]):
            pixels[i, j] = 255

    canvas._image_tk = ImageTk.PhotoImage(pilimage)
    canvas.itemconfigure(canvas._image_id, image=canvas._image_tk)


def piltomatrix(pilimage):
    list_x = []
    list_y = []
    pixels = pilimage.load()

    for i in range(pilimage.size[0]):
        for j in range(pilimage.size[1]):
            if pixels[i, j] != 255:
                list_x.append(j)
                list_y.append(i)

    matrix = np.matrix([list_x, list_y, [0] * len(list_x)])
    return matrix


def move(pilimage, canvas, mvx, mvy):
    matrix = piltomatrix(pilimage)
    transformation = np.matrix([[1, 0, mvx],
                               [0, 1, mvy],
                               [0, 0, 1]])
    results = transformation * matrix
    clear(pilimage, canvas)
    pixels = pilimage.load()

    for column in xrange(results.shape[1]):
        ptx = results[0, column]
        pty = results[1, column]
        pixels[ptx, pty] = 0

    canvas._image_tk = ImageTk.PhotoImage(pilimage)
    canvas.itemconfigure(canvas._image_id, image=canvas._image_tk)
