from ...icon import Icon
from ...plot import Plot
from numpy import ndarray
from .scatter import Scatter
from PSVG import Path
from NumpyTransforms.Bezier import interpolate as bezier


class Curve(Scatter):
    def __init__(self, X: ndarray, Y: ndarray, path: Path, plot: Plot, icon: Icon | None = None, *args, **kwargs):
        if icon is None:
            icon = Icon(Path(), 0, 0)
            icon.root.active = False

        super().__init__(X=X, Y=Y, icon=icon, plot=plot, *args, **kwargs)
        self.path = path

    def _process(self):
        x, y = self.plot.transform(self.X, self.Y)

        self.path.points = path_points(x, y)
        self.add_child(self.path)

        self._set_icons(x, y)

    @staticmethod
    def _path_points(x, y):
        yield 'M', x[0], y[0]

        for _x, _y in zip(x[1:], y[1:]):
            yield 'L', x, y


def path_points(x: ndarray, y: ndarray, fill_line=None) -> list[tuple]:
    """
    returns a list that defines the bezier form of the chromatogram
    :param x: x values (time)
    :param y: y values (response)
    :param fill_line: value at which to define a baseline for the curve to fill to
    """
    ax, bx = bezier(x)
    ay, by = bezier(y)

    if fill_line is not None:
        return list(_fill(fill_line, x, y, ax, ay, bx, by))
    else:
        return list(_no_fill(x, y, ax, ay, bx, by))


def _meat(x, y, ax, ay, bx, by):
    n = len(x)
    for i in range(n - 1):
        if i == 0:
            yield 'C', ax[i], ay[i]
        else:
            yield '', ax[i], ay[i]

        yield '', bx[i], by[i]
        yield '', x[i + 1], y[i + 1]


def _fill(fill_line, x, y, ax, ay, bx, by):
    yield 'M', x[0], fill_line
    yield 'L', x[0], y[0]

    for i in _meat(x, y, ax, ay, bx, by):
        yield i

    yield 'L', x[-1], fill_line
    yield 'Z', '', ''


def _no_fill(x, y, ax, ay, bx, by):
    yield 'M', x[0], y[0]

    for i in _meat(x, y, ax, ay, bx, by):
        yield i
