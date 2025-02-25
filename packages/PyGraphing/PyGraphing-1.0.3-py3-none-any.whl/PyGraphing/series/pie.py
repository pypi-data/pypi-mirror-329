# from ..plot import Plot
# from PSVG import Section
# from PSVG.Draw import Generic_Path, PartialCircle
# from math import pi
#
#
# class Pie(Section):
#     def __init__(self, plot: Plot):
#         super().__init__(0, 0)
#         self.plot = plot
#         self._chunks = []
#         self._values = []
#
#     def add_chunk(self, value: float, path: Generic_Path):
#         self._chunks.append(path)
#         self._values.append(value)
#
#     def _process(self):
#         n = len(self._values)
#         x = self.plot.w / 2
#         y = self.plot.h / 2
#         r = 0.45 * min([self.plot.w, self.plot.h])
#
#         theta = 0
#         total = sum(self._values)
#         for i in range(n):
#             chunk = self._chunks[i]
#             value = self._values[i]
#             theta2 = value * 2 * pi / total
#
#             wedge = PartialCircle(x, y, r, theta, theta2)
#             theta += theta2
#             wedge.inherit(chunk)
#
#             self.add_child(wedge)
#
#     def construct(self):
#         self._process()
#         return super().construct()
