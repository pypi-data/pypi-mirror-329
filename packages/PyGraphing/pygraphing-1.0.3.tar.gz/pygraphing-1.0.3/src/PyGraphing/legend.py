from PSVG import Section, Rect, Text
from .icon import Icon


class Item:
    def __init__(self, icon: Icon, name: Text, left=0, midl=5, rght=0, top=2.5, bot=2.5):
        self.left = left
        self.rght = rght
        self.midl = midl

        self.top = top
        self.bot = bot

        self.icon = icon
        self.text = name

        self.x = 0
        self.y = 0

    @property
    def w(self):
        return self.icon.w + name.width + self.left + self.rght + self.midl

    @property
    def h(self):
        return self.icon.h + self.top + self.bot

    def set(self):
        self.icon.x = self.x + self.left
        self.icon.y = self.y + self.top

        self.text.x = self.x + self.left + self.icon.w + self.midl
        self.text.y = self.icon.y + self.icon.h / 2


class Legend(Section):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._items = []
        self.y0 = 0

        self.background = Rect(active=False)
        self.addChild(self.background)

    def addItem(self, icon: Icon, text: Text, **kwargs):
        self._items.append(Item(icon, text, **kwargs))

    def set(self):
        y = self.y0
        for item in self._items:
            item.y = y
            y += item.h

            self.addChild(item.icon.root)
            self.addChild(item.text)

            item.set()

    @property
    def xywh(self):
        return self.x, self.y, self.w, self.h

    @xywh.setter
    def xywh(self, vals: tuple[float, float, float, float]):
        self.x = vals[0]
        self.y = vals[1]
        self.w = vals[2]
        self.h = vals[3]
