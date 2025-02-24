from NaxToPy import N2PLog

# Method used to transform a point to isoparametric coordinates --------------------------------------------------------
def transform_isoparametric(point, quad, tol: float = 0.01): 

    """
    Transforms a 3D point to isoparametric coordinates within a quadrilateral. Even though it is a 2D transformation, 
    the points can be introduced either in 3D or 2D format.

    Args:
        point -> 3D point (x, y, z).
        quad -> list of four 3D points defining the quadrilateral.
        tol: float = 1e-4 -> tolerance used to avoid bad approximations.

    Returns:
        u, v: float -> isoparametric coordinates of the point within the quadrilateral.

    Calling example: 
        >>> u, v = transform_isoparametric(point, vertices)
    """

    # Coefficients a and b are defined
    a0 = 0.25*((quad[0][0] + quad[1][0]) + (quad[2][0] + quad[3][0]))
    a1 = 0.25*((quad[1][0] - quad[0][0]) + (quad[2][0] - quad[3][0]))
    a2 = 0.25*((quad[2][0] + quad[3][0]) - (quad[0][0] + quad[1][0]))
    a3 = 0.25*((quad[0][0] - quad[1][0]) + (quad[2][0] - quad[3][0]))

    b0 = 0.25*((quad[0][1] + quad[1][1]) + (quad[2][1] + quad[3][1]))
    b1 = 0.25*((quad[1][1] - quad[0][1]) + (quad[2][1] - quad[3][1]))
    b2 = 0.25*((quad[2][1] + quad[3][1]) - (quad[0][1] + quad[1][1]))
    b3 = 0.25*((quad[0][1] - quad[1][1]) + (quad[2][1] - quad[3][1]))

    # x0 and y0 are defined 
    x0 = point[0] - a0
    y0 = point[1] - b0
    
    # Coefficients A, B and C are defined 
    A = a3*b2 - a2*b3
    B = (x0*b3 + a1*b2) - (y0*a3 + a2*b1)
    C = x0*b1 - y0*a1
    
    # v is obtained 
    if abs(A) < tol: 
        if abs(B) < tol: # A = 0 and B = 0
            N2PLog.Error.E510()
            return[None, None], [None, None] 
        vResults = [-C/B, -C/B]
    elif abs(B) < tol: 
        vResults = [(-C/A)**0.5, -((-C/A)**0.5)] # A != 0 and B = 0
    else: # A != 0 and B != 0
        disc = B**2 - 4*A*C 
        if disc < 0: 
            N2PLog.Error.E510()
            return[None, None], [None, None] 
        vResults = [(-B + disc**0.5)/(2*A), (-B - disc**0.5)/(2*A)]
    # u is obtained 
    uResults = [None, None]
    for i, j in enumerate(vResults): 
        denom = a1 + a3*j 
        if abs(denom) < tol and abs(a1*b3) > tol and abs(a3*b1) > tol: 
            u = (y0*a3 + a1*b2)/(a3*b1 - a1*b3)
            j = x0/a2 
            vResults[i] = j 
            uResults[i] = u 
        elif abs(denom) < tol and abs(a3*b1) < tol: 
            u = (y0*a2 - b2*x0)/(b3*x0 - a2*b1)
            j = x0/a2 
            vResults[i] = j 
            uResults[i] = u 
        else: 
            uResults[i] = (x0 - a2*j)/(denom)
    results1 = [uResults[0], vResults[0]]
    results2 = [uResults[1], vResults[1]]
    allResults = [results1, results2]

    def value_detection(pair, tol): 
        return all(-1 - tol <= i <= 1 + tol for i in pair)
    result = None 
    for i in allResults: 
        if value_detection(i, 2*tol): 
            result = result or i 
            break 
    return result[0], result[1]
# ----------------------------------------------------------------------------------------------------------------------

# Method used to transform a point to barycentric coordinates ----------------------------------------------------------
def transform_barycentric(point, nodes): 

    """
    Transforms a 3D point to barycentric coordinates within a triangle.

    Args:
        point -> 1D ndarray of shape (3,) representing the 3D point in the triangle.
        nodes -> 2D ndarray of shape (3, 3) representing the coordinates of the triangle's three corners.

    Returns:
        alpha, beta, gamma: float -> barycentric coordinates of the point within the triangle.

    Calling example: 
        >>> alpha, beta, gamma = transform_barycentric(point, vertices)
    """

    det = (nodes[1][1] - nodes[2][1])*(nodes[0][0] - nodes[2][0]) + (nodes[2][0] - nodes[1][0])*(nodes[0][1] - nodes[2][1])
    alpha = ((nodes[1][1] - nodes[2][1])*(point[0] - nodes[2][0]) + (nodes[2][0] - nodes[1][0])*(point[1] - nodes[2][1]))/det
    betha = ((nodes[2][1] - nodes[0][1])*(point[0] - nodes[2][0]) + (nodes[0][0] - nodes[2][0])*(point[1] - nodes[2][1]))/det
    gamma = 1 - alpha - betha

    return alpha, betha, gamma
# ----------------------------------------------------------------------------------------------------------------------

# Method used to interpolate -------------------------------------------------------------------------------------------
def interpolation(point, vertices, values, tol: float = 0.01): 
    
    """
    Performs 3D interpolation within a triangle or quadrilateral.

    Args:
        point -> 1D ndarray of shape (3,) representing the 3D point in the shape.
        vertices -> 2D ndarray of shape (n, 3) representing the coordinates of the shape's corners (n = 3 for a 
        triangle, n = 4 for a quadrilateral).
        values -> 2D ndarray of shape (n, 6) representing the values at the shape's corners.

    Returns:
        interpolatedValue: float -> interpolated value at the given point as a 1D ndarray of shape (6,).

    Calling example: 
        >>> interpolatedForces = interpolation(pointCoordElem, cornerCoordElem, values)
    """

    n = vertices.shape[0]

    # CTRIA3
    if n == 3:
        alpha, beta, gamma = transform_barycentric(point, vertices)
        interpolatedValue = (alpha * values[0] + beta * values[1] + gamma * values[2])

    # CQUAD4
    elif n == 4:
        u, v = transform_isoparametric(point, vertices, tol)
        f00 = values[0] * 0.25 * (1 - u) * (1 - v)
        f01 = values[1] * 0.25 * (1 + u) * (1 - v)
        f10 = values[2] * 0.25 * (1 + u) * (1 + v)
        f11 = values[3] * 0.25 * (1 - u) * (1 + v)

        interpolatedValue = f00 + f01 + f10 + f11
    else: 
        N2PLog.Error.E511()
    return interpolatedValue
# ----------------------------------------------------------------------------------------------------------------------