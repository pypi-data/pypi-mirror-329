from ..series import Series
from ...icon import Icon
from ...plot import Plot
from numpy import ndarray


class Scatter(Series):
    def __init__(self, X: ndarray, Y: ndarray, icon: Icon, plot: Plot, *args, **kwargs):
        super().__init__(plot=plot, *args, **kwargs)
        self.X = X
        self.Y = Y
        self.icon = icon

    def _process(self):
        x, y = self.plot.transform(self.X, self.Y)
        self._set_icons(x, y)

    def _set_icons(self, x: ndarray, y: ndarray):
        _x = x - self.icon.w / 2
        _y = y - self.icon.h / 2
        _ = [self._set_icon(i, j) for i, j in zip(_x, _y)]

    def _set_icon(self, x: float, y: float):
        icon = self.icon.copy()
        icon.x = x
        icon.y = y

        self.add_child(icon.root)
