from functools import cache

from pyglet.shapes import Circle, Rectangle
from pyglet.text import Label


@cache
def makeCircle(x, y, r, color):
    return Circle(x, y, r, color=color)


@cache
def makeRectangle(x, y, w, h, color):
    return Rectangle(x, y, w, h, color=color)


@cache
def makeLabel(text, x, y, color=None, **kw):
    if color is None:
        color = [0, 0, 0]
    return Label(text, x=x, y=y, color=color, **kw)
