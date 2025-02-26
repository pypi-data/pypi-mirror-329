import cadquery as cq

def cube(size, center=False):
    """
    Create a cube. The `size` parameter can be a single number to create a cube with equal dimensions, or a vector of
    three numbers to specify the length, width, and height individually. If `center` is True, the cube will be centered
    at the origin; otherwise, the cube will be in the positive quadrant.
    """
    if isinstance(size, (list, tuple)):
        length, width, height = size
    else:
        length = width = height = size
    cube = cq.Workplane("XY").box(length, width, height, centered=(center, center, center))
    return cube

def sphere(r):
    """
    Creates a sphere of radius `r`.
    """
    sphere = cq.Workplane("XY").sphere(r)
    return sphere

def cylinder(h, r1, r2=None, center=False):
    """
    Creates a cylinder or a cone. `h` is the height, `r1` and `r2` are the radii at the two ends. If `r1` equals `r2`,
    a cylinder is created; if not, a cone is created. If `center` is true, the cylinder or cone is centered along the
    z-axis; otherwise, it starts from the origin.
    """
    if r2 is None:
        r2 = r1
    cylinder = cq.Workplane("XY").circle(r1).workplane(offset=h).circle(r2).loft(combine=True, centered=(center, center, center))
    return cylinder

def polyhedron(points, faces):
    """
    Creates a custom polyhedron. `points` is a list of vertices, and `faces` is a list of faces. Each face is a list of
    indices into the `points` list.
    """
    polyhedron = cq.Workplane("XY")
    for face in faces:
        vertices = [points[i] for i in face]
        polyhedron = polyhedron.polyline(vertices).close().extrude(1)  # Assumes thickness of 1
    return polyhedron
