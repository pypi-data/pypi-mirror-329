from ..series import Series
from PSVG import Rect
from ...plot import Plot
from numpy import ndarray


class PlotRect(Series):
    def __init__(self, plot: Plot, rect: Rect, x: ndarray, y: ndarray, **kwargs):
        super().__init__(plot, **kwargs)

        self.X = x
        self.Y = y
        self.rect = rect

    def _process(self):
        x, y = self.plot.transform(self.X, self.Y)

        self.rect.x = x.min()
        self.rect.y = y.min()
        self.rect.w = x.max() - x.min()
        self.rect.h = y.max() - y.min()

        self.add_child(self.rect)
