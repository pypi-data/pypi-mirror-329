from solid_node import Node
from solid2 import cylinder, translate
from ... import TwoCylinders


class TwoCylindersTwice(Node):

    def render(self):
        return [
            TwoCylinders(),
            TwoCylinders().rotate(180, [1, 0, 0]),
        ]
