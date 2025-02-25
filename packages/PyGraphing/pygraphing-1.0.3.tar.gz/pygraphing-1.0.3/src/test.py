from PyGraphing.graph import Graph
from PSVG import Document, Font, Rect, Text, Path
from PyGraphing.series import Line, Curve, ErrorBars
from PyGraphing.icon import Icon
from numpy import array, linspace

from random import random

d = Document(w=800, h=1000)
f = Font('IBM Plex Mono', '300')

g = Graph(f, w=800, h=500, title='hello')
g.plot.background.fill = (10, 100, 200)
g.plot.background.fill_opacity = .05

g.legend.background.active = True
g.legend.background.fill = (200, 100, 10)
g.legend.background.fill_opacity = 0.25

g.frame.border.stroke = (10, 50, 22)
g.frame.border.stroke_width = 1
g.frame.border.stroke_opacity = 1
g.frame.L = False
g.frame.R = False

t = Text(f, fill=g.frame.border.stroke, anchor='middle', baseline='hanging')
g.frame.x_axis.dist2text = 2
g.frame.x_axis.text = t

g.xlabel.text = ' X LABEL MOTHERFUCKER'
g.xlabel.textColor = (55, 75, 201)
g.xlabel.textOpacity = 1
g.xlabel.fill = (123, 231, 10)
g.xlabel.fill_opacity = 1
g.xlabel.background.active = True

g.ylabel.text = ' Y LABEL MOTHERFUCKER'
g.ylabel.textColor = (55, 75, 201)
g.ylabel.textOpacity = 1
g.ylabel.fill = (10, 231, 123)
g.ylabel.fill_opacity = 1
g.ylabel.background.active = True

r = Rect('10%', '10%', '80%', '80%', fill=(175, 125, 25), fill_opacity=0.5,
         stroke=(175, 125, 25), stroke_opacity=1, stroke_width=1, rx=1, ry=1)

_x = linspace(1, 4, 7)
_y = array([random() * 3 + 1 for _ in range(7)])
p = Path(stroke=(99, 175, 25), stroke_width=2, stroke_opacity=1, fill_opacity=0)

s = Line(icon=Icon(r, 10, 10),
         plot=g.plot,
         X=_x,
         Y=_y,
         path=p)

s2 = Curve(icon=None,
           plot=g.plot,
           X=_x,
           Y=_y,
           path=Path(stroke=(175, 175, 25), stroke_width=2, stroke_opacity=1, fill_opacity=.5))

q = ErrorBars(X=_x, Y=_y, E=_y * .2, path=p, plot=g.plot)
q.barwidth = 0.1

g.plot.extrema = 0, 6, -1, 6
for i in range(6):
    g.frame.x_axis.addTick(i, f'{i}')
    g.frame.y_axis.addTick(i, f'{i}')

g.plot.addChild(q)
g.plot.addChild(s2)
g.plot.addChild(s)

g.set_sizes((.1, .1, .8, .8))
d.addChild(g.root)

s = d.root.construct(0)
with open('test.svg', 'w') as file:
    file.write(s)

pass
