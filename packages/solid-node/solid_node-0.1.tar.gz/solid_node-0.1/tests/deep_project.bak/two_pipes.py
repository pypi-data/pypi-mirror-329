from solid_node import Node
from solid2 import cylinder, translate
from simple_pipe import SimplePipe


class TwoPipes(Node):

    def render(self):
        return [
            SimplePipe(),
            SimplePipe().translate(100, 0, 0),
        ]
