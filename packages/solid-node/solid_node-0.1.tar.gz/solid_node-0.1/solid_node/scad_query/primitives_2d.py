import cadquery as cq

def circle(r, center=False):
    """
    Creates a circle of radius `r`. If `center` is True, the circle will be centered at the origin;
    otherwise, the circle will be in the positive quadrant.
    """
    if center:
        circle = cq.Workplane("XY").circle(r)
    else:
        circle = cq.Workplane("XY").moveTo(r, r).circle(r)
    return circle

def square(size, center=False):
    """
    Creates a square. The `size` parameter can be a single number to create a square with equal sides, or a vector of
    two numbers to specify the width and height individually. If `center` is True, the square will be centered
    at the origin; otherwise, the square will be in the positive quadrant.
    """
    if isinstance(size, (list, tuple)):
        width, height = size
    else:
        width = height = size
    if center:
        square = cq.Workplane("XY").rect(width, height)
    else:
        square = cq.Workplane("XY").moveTo(width / 2, height / 2).rect(width, height)
    return square

def polygon(points):
    """
    Creates a polygon defined by `points`, which is a list of vertices.
    """
    polygon = cq.Workplane("XY").polyline(points).close()
    return polygon
