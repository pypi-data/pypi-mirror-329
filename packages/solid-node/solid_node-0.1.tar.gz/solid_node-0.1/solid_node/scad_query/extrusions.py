def linear_extrude(profile, height, center=False):
    """
    Extrudes a 2D profile into a 3D shape. If `center` is True, the extrusion will be centered along the z-axis.
    """
    if center:
        extrude = profile.extrude(height / 2).translate((0, 0, -height / 2))
    else:
        extrude = profile.extrude(height)
    return extrude

def rotate_extrude(profile):
    """
    Rotates a 2D profile around the Z-axis to create a 3D shape. In CadQuery, this is equivalent to a revolve operation.
    """
    revolve = profile.revolve()
    return revolve
