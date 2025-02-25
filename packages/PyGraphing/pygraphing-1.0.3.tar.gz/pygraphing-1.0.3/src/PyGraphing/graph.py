from PSVG import Text, Font, Rect, Section, TextBox
from .plot import Plot
from .legend import Legend
from .frame import Frame

default_font = Font('Arial', '400')


class Graph(Section):
    def __init__(self, font: Font, x: float = 0, y: float = 0, w: float = 0, h: float = 0,
                 title: str = '', title_font: Font = None, subtitle: str = '', subtitle_font: Font = None):
        """
        Graph is an SVG Object representing a generic graph.
        A Graph is made up of several parts: Legend, Plot Area, Frame, Title.

        :param w: width of the Graph object in pixels
        :param h: height of the Graph object in pixels
        :param x: horizontal position of the Graph object in pixels
        :param y: vertical position of the Graph object in pixels
        """
        super().__init__(x=x, y=y, w=w, h=h)

        self.background = Rect(active=False)
        self.addChild(self.background)

        self.font = font

        title = Text(title_font if title_font is not None else font, title)
        self.title = TextBox(title)
        self.addChild(self.title.root)

        subtitle = Text(subtitle_font if subtitle_font is not None else font, subtitle)
        self.subtitle = TextBox(subtitle)
        self.addChild(self.subtitle.root)

        self.label = TextBox(Text(font, ''))
        self.addChild(self.label.root)

        self.xlabel = TextBox(Text(font, ''))
        self.addChild(self.xlabel.root)

        self.ylabel = TextBox(Text(font, ''))
        self.addChild(self.ylabel.root)

        self.legend = Legend()
        self.addChild(self.legend.root)

        self.plot = Plot()
        self.addChild(self.plot.root)

        self.frame = Frame(self)
        self.addChild(self.frame)

    def text(self, **kwargs):
        return Text(self.font, baseline='central', **kwargs)

    def set_sizes(self, xywh=(0, 0, 1, 1)):
        """
        Sets the sizes for the Graph and all of its children.
        ----------------------------------------------------------------------
        """
        self._verify()

        w, h = self.w, self.h
        px = w * xywh[0]
        py = h * xywh[1]
        pw = w * xywh[2]
        ph = h * xywh[3]

        self.plot.xywh = px, py, pw, ph

        if self.title.root.active and self.subtitle.root.active:
            self.title.xywh = px, 0, pw, py / 2
            self.title.alignment = (0, 0)
            self.title.set()

            self.subtitle.xywh = px, py / 2, pw, py / 2
            self.subtitle.set()

        elif self.title.root.active and not self.subtitle.root.active:
            self.title.xywh = px, 0, pw, py
            self.title.set()

        if self.legend.root.active:
            self.legend.xywh = px + pw + 10, py, w - 10 - pw - px, ph

        if self.xlabel.root.active:
            self.xlabel.xywh = px, py + ph, pw, h - py - ph
            self.xlabel.set()

        if self.ylabel.root.active:
            self.ylabel.xywh = 0, py, ph, px
            self.ylabel.root.angle = -90
            self.ylabel.root.xc = self.ylabel.h / 2 - self.ylabel.y
            self.ylabel.root.yc = self.ylabel.w / 2
            self.ylabel.set()

    def _verify(self):
        if self.title.text == '':
            self.title.root.active = False

        if self.subtitle.text == '':
            self.subtitle.root.active = False

        if self.xlabel.text == '':
            self.xlabel.root.active = False

        if self.ylabel.text == '':
            self.ylabel.root.active = False

        if self.label.text == '':
            self.label.root.active = False
