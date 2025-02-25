from PSVG import Section, Node
from typing import overload


class Icon(Section):
    @overload
    def __init__(self, svg_objects: list[Node], w: float, h: float, x: float = 0, y: float = 0):
        ...

    @overload
    def __init__(self, svg_object: Node, w: float, h: float, x: float = 0, y: float = 0):
        ...

    def __init__(self, svg_objects, w: float, h: float, x: float = 0, y: float = 0):
        super().__init__(w=w, h=h, x=x, y=y)

        if isinstance(svg_objects, list):
            _ = [self.addChild(node) for node in svg_objects]
        else:
            self.addChild(svg_objects)
