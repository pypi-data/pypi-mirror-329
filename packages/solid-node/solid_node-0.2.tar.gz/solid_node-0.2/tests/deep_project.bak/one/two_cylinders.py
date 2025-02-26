from solid_node import Node
from solid2 import cylinder, translate
from .. import SimpleCylinder


class TwoCylinders(Node):

    def render(self):
        return [
            SimpleCylinder(radius=10, height=5),
            SimpleCylinder(radius=5, height=10),
        ]
