from ..plot import Plot
from PSVG import G


class Series(G):
    def __init__(self, plot: Plot, *args, **kwargs):
        super().__init__()
        self.plot = plot

    def _process(self):
        pass

    def construct(self, depth):
        self._process()
        return super().construct(depth)
