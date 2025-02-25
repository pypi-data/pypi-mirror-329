from PSVG import G, Path, Text
from .data_sturctures import Tree
from collections import namedtuple
from numpy import array

Point = namedtuple('Point', ('x', 'y'))
Test = namedtuple('Test', ('n1', 'n2', 'pt', 'pred'))


class Frame(G):
    def __init__(self, graph):
        super().__init__(0, 0)
        self.border = Path(fill_opacity=0)
        self.x_axis = Axis(graph.text())
        self.y_axis = Axis(graph.text())

        self.plot = graph.plot

        self.L, self.R, self.T, self.B = True, True, True, True

    def points(self):
        p = self.plot
        return {1: Point(p.x, p.y),
                2: Point(p.x, p.y + p.h),
                3: Point(p.x + p.w, p.y + p.h),
                4: Point(p.x + p.w, p.y),
                5: Point(p.x - self.y_axis.tick_length, p.y),
                6: Point(p.x - self.y_axis.tick_length, p.y + p.h),
                7: Point(p.x, p.y + p.h + self.x_axis.tick_length),
                8: Point(p.x + p.w, p.y + p.h + self.x_axis.tick_length)}

    def _set_border(self):
        b = Border(self)
        self.border.points = b.get_pts()
        self.add_child(self.border)

    def _add_label(self, text: Text, label: str, x: float, y: float):
        if text is not None:
            text = text.copy()
            text.text = label
            text.x = x
            text.y = y

            self.add_child(text)

    def _set_x_axis(self):
        ax = self.x_axis
        if not ax.active:
            return

        ticks, labels = ax.getTicks()

        if ticks is not None:
            ticks = self.plot.cart2pixel_x(ticks) + self.plot.x
            y = self.plot.y + self.plot.h
            for x, label in zip(ticks, labels):
                self._add_label(ax.text, label, x, y + ax.tick_length + ax.dist2text)
                self.border.points.append(('M', x, y))
                self.border.points.append(('L', x, y + ax.tick_length))

    def _set_y_axis(self):
        ax = self.y_axis
        if not ax.active:
            return

        ticks, labels = ax.getTicks()
        if ticks is not None:
            ticks = self.plot.cart2pixel_y(ticks) + self.plot.y
            x = self.plot.x
            for y, label in zip(ticks, labels):
                self._add_label(ax.text, label, x - ax.tick_length - ax.dist2text, y)
                self.border.points.append(('M', x, y))
                self.border.points.append(('L', x - ax.tick_length, y))

    def construct(self, depth):
        self._set_border()
        self._set_x_axis()
        self._set_y_axis()

        return super().construct(depth)


class Axis:
    def __init__(self, text: Text):
        self.tick_length = 4
        self.dist2text = 11
        self._ticks = {}
        self.text = text
        self.active = True

    def addTick(self, pos: float, label: str):
        self._ticks[pos] = label

    def getTicks(self):
        ticks = list(self._ticks.items())
        if ticks:
            ticks.sort()
            pos, lab = zip(*ticks)
            pos = array(pos)
            return pos, lab

        return None, None


class Border(Tree):
    def __init__(self, frame: Frame):
        super().__init__()
        self.frame = frame

        #  5---1------------4
        #      |            |
        #      |            |
        #      |            |
        #  6---2------------3
        #      |            |
        #      7            8

    def _connect(self):
        """
        Tests conditions to determine what nodes should be connected
        """
        f = self.frame
        p = f.points()
        y_ticks, _ = f.y_axis.getTicks()
        if y_ticks is None:
            y_ticks = [None, None]
        x_ticks, _ = f.x_axis.getTicks()
        if x_ticks is None:
            x_ticks = [None, None]

        tests = [Test(1, 2, p[1], f.L),
                 Test(2, 3, p[2], f.B),
                 Test(3, 4, p[3], f.R),
                 Test(4, 1, p[4], f.T),
                 Test(5, 1, p[5], y_ticks[-1] == f.plot.ymax),
                 Test(6, 2, p[6], y_ticks[0] == f.plot.ymin),
                 Test(7, 2, p[7], x_ticks[0] == f.plot.xmin),
                 Test(8, 3, p[8], x_ticks[-1] == f.plot.xmax)]

        for t in tests:
            if t.pred:
                n1 = self.addNode(t.n1, p[t.n1])
                n2 = self.addNode(t.n2, p[t.n2])
                self.drawEdge(n1, n2, is_directed=False)

    def get_pts(self):
        self._connect()
        self._nodes = {node: False for node in self.nodes}

        for node, is_marked in self._nodes.items():
            if not is_marked:
                self._DFS(node, 'M')

        if self.frame.L and self.frame.B and self.frame.R and self.frame.T:
            self._pts.append(('L', self.n_4.value[0], self.n_4.value[1]))
            self._pts.append(('L', self.n_3.value[0], self.n_3.value[1]))
            self._pts.append(('L', self.n_2.value[0], self.n_2.value[1]))
            self._pts.append(('L', self.n_1.value[0], self.n_1.value[1]))

        return self._pts

    def _DFS(self, node, letter='L'):
        self._nodes[node] = True
        self._pts.append((letter, node.value[0], node.value[1]))
        for n in node.neighbors:
            if not self._nodes[n]:
                self._DFS(n)
                self._pts.append(('L', node.value[0], node.value[1]))

        pass
