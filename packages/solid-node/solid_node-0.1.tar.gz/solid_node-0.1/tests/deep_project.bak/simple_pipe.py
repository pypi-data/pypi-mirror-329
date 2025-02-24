from solid_node import Node
from solid2 import cylinder


class SimplePipe(Node):

    def render(self):
        return cylinder(r=10, h=100) - cylinder(r=8, h=100)
