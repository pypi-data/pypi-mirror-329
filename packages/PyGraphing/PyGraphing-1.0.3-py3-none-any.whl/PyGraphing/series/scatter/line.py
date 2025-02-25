from ...icon import Icon
from ...plot import Plot
from numpy import ndarray
from .scatter import Scatter
from PSVG import Path


class Line(Scatter):
    def __init__(self, X: ndarray, Y: ndarray, path: Path, plot: Plot, icon: Icon | None = None, *args, **kwargs):
        if icon is None:
            icon = Icon(Path(), 0, 0)
            icon.root.active = False

        super().__init__(X=X, Y=Y, icon=icon, plot=plot, *args, **kwargs)
        self.path = path

    def _process(self):
        x, y = self.plot.transform(self.X, self.Y)
        self.path.points = list(self._path_points(x, y))
        self.add_child(self.path)

        self._set_icons(x, y)

    @staticmethod
    def _path_points(x, y):
        yield 'M', x[0], y[0]

        for _x, _y in zip(x[1:], y[1:]):
            yield 'L', _x, _y
