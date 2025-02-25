from ...icon import Icon
from ...plot import Plot
from numpy import ndarray
from .scatter import Scatter
from PSVG import Path


class ErrorTop(Scatter):
    def __init__(self, X: ndarray, Y: ndarray, E: ndarray, path: Path, plot: Plot, *args, **kwargs):
        icon = Icon(Path(), 0, 0)
        icon.root.active = False
        super().__init__(X=X, Y=Y, icon=icon, plot=plot, *args, **kwargs)

        self.path = path
        self.E = E
        self.barwidth = 10

    def _process(self):
        w = self.plot.c2px(self.barwidth)

        x = self.plot.cart2pixel_x(self.X)
        b = self.plot.cart2pixel_y(self.Y)
        t = self.plot.cart2pixel_y(self.Y + self.E)

        _ = [self._set_path(w, i, j, k) for i, j, k in zip(x, b, t)]

    def _set_path(self, bw: float, x: float, e1: float, e2: float):
        path = self.path.copy()
        path.points = [('M', x - bw, e2),
                       ('L', x + bw, e2),
                       ('M', x, e2),
                       ('L', x, e1)]

        self.add_child(path)
