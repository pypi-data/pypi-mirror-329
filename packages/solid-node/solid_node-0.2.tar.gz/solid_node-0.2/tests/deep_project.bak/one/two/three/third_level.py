from solid_node import Node
from solid2 import cylinder, translate
from .... import TwoCylindersTwice


class ThirdLevel(Node):

    def render(self):
        return [
            TwoCylindersTwice(),
            TwoCylindersTwice().rotate(180, [0, 1, 0]),
        ]
