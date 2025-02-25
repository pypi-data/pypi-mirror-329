from PSVG import Section, Rect
from numpy import ndarray, array
from warnings import warn
from NumpyTransforms.Affine import Affine


class Plot(Section):
    def __init__(self):
        super().__init__()
        self.xmin, self.ymin, self.xmax, self.ymax = 0, 0, 1, 1
        self.background = Rect()
        self.background.active = False
        self.addChild(self.background)

    @property
    def extrema(self):
        return self.xmin, self.xmax, self.ymin, self.ymax

    @extrema.setter
    def extrema(self, vals: tuple[float, float, float, float]):
        self.xmin = vals[0]
        self.xmax = vals[1]
        self.ymin = vals[2]
        self.ymax = vals[3]

    def cart2pixel_x(self, x: ndarray) -> ndarray:
        """
        Retrieves the pixel coordinates for the horizontal (x) axis from the array of cartessian coordinates x
        :param x: array of Cartessian x values to be converted
        :return: array of pixel x values
        """
        if self.xmax != self.xmin:
            return self.w * ((x - self.xmin) / (self.xmax - self.xmin))
        else:
            warn('You cannot normalize a plot with xmin and xmax being the same value.')
            return array([])

    def cart2pixel_y(self, y: ndarray) -> ndarray:
        """
        Retrieves the pixel coordinates for the vertical (y) axis from the array of cartessian coordinates y
        :param y: array of Cartessian y values to be converted
        :return: array of pixel y values
        """
        if self.ymin != self.ymax:
            return self.h * (1 - (y - self.ymin) / (self.ymax - self.ymin))
        else:
            warn('You cannot normalize a plot with ymin and ymax being the same value.')
            return array([])

    def c2px(self, x: float) -> float:
        """
        Convenience function for a single value evaluation of cart2pixel_x
        """
        x = self.cart2pixel_x(array([x]))
        if len(x) == 1:
            return x[0]
        else:
            return 0

    def c2py(self, y: float) -> float:
        """
        Convenience function for a single value evaluation of cart2pixel_y
        """
        y = self.cart2pixel_x(array([y]))
        if len(y) == 1:
            return y[0]
        else:
            return 0

    def transform(self, x: ndarray, y: ndarray):
        affine = Affine()
        affine.translate(-self.w * self.xmin / (self.xmax - self.xmin),
                         self.h * self.ymin / (self.ymax - self.ymin) + self.h)
        affine.scale(self.w / (self.xmax - self.xmin), -self.h / (self.ymax - self.ymin))

        return affine(x, y)
