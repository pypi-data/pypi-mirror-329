from .scatter import Scatter, Icon, Plot
from numpy import ndarray, arange, array


class GroupedScatter(Scatter):
    def __init__(self, X: ndarray, Y: ndarray, icon: Icon, plot: Plot, *args, **kwargs):
        super().__init__(X, Y, icon, plot, *args, **kwargs)

        self.bw = .8

    def _process(self):
        x = []
        y = []

        unique_x = list(set(self.X))
        unique_x.sort()

        for i in unique_x:
            _x, _y = self._bar(i)
            x += _x.tolist()
            y += _y.tolist()

        x, y = array(x), array(y)
        x, y = self.plot.transform(x, y)
        self._set_icons(x, y)

    def _bar(self, i):
        y = self.Y[self.X == i]
        n = len(y)
        dx = self.bw / (n + 2)
        x = arange(1, n + 1)

        x = i - self.bw / 2 + x * dx

        return x, y
