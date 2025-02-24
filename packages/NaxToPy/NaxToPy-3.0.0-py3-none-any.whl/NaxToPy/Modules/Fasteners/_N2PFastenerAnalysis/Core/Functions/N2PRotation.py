from NaxToPy.Core.Classes.N2PElement import N2PElement 
from NaxToPy import N2PLog
import numpy as np 

# Method used to rotate a 2D tensor ------------------------------------------------------------------------------------
def rotate_tensor2D(fromSystem: list, toSystem: list, planeNormal: list, tensor: list) -> list: 

    """
    Method used to a 2D tensor from one coordinate system to another. 
    
    Args: 
        fromSystem: list -> original system.
        toSystem: list -> destination system. 
        planeNormal: list -> rotation plane. 
        tensor: list -> tensor to rotate. 

    Returns: 
        rotatedTensor: list 

    Calling example: 
        >>> forcesRot = rotate_tensor2D(elementSystem, materialSystem, elementSystem[6:9], forces)
    """

    tensor = np.array(tensor) 
    alpha = angle_between_2_systems(fromSystem, toSystem, planeNormal) 
    # Definition of the rotation matrix 
    c = np.cos(alpha) 
    s = np.sin(alpha) 
    R = np.array([[c**2, s**2, 2*s*c], [s**2, c**2, -2*s*c], [-s*c, s*c, c**2 - s**2]])
    shape = tensor.shape 
    tensorReshaped = tensor.reshape((-1, 3)).T 
    rotatedTensor = np.matmul(R, tensorReshaped).T 
    return rotatedTensor.reshape(shape).tolist() 
# ----------------------------------------------------------------------------------------------------------------------

# Method used to rotate a vector (1D tensor) ---------------------------------------------------------------------------
def rotate_vector(vector: list, fromSystem: list, toSystem: list) -> np.ndarray: 

    """
    Method used to rotate a vector from a coordinate system to another.

    Args:
        vector: list -> vector to be rotated. 
        fromSystem: list -> original system. 
        toSystem: list -> destination system. 

    Returns:
        rotatedVector: ndarray 

    Calling example: 
        >>> transformedNode = rotate_vector(nodeVector, globalSystem, elementSystem)
    """

    # Verify if every input has a length which is a multiple of three 
    if len(vector) %3 != 0 or len(fromSystem) %3 != 0 or len(toSystem) %3 != 0: 
        N2PLog.Error.E512()
        return None 
    vectorSegments = [vector[i: i + 3] for i in range(0, len(vector), 3)]
    transformedSegments = [] 
    # Vectors are reshaped into matrices 
    matrixCurrent = np.array(fromSystem).reshape(3, -1) 
    matrixNew = np.array(toSystem).reshape(3, -1) 
    for i in vectorSegments: 
        i = np.array(i).reshape(-1, 3) 
        matrixRotation = np.linalg.inv(matrixCurrent) @ matrixNew 
        transformedSegments.append((matrixRotation @ i.T).T)
    rotatedVector = np.concatenate(transformedSegments).reshape(-1) 
    return rotatedVector 
# ----------------------------------------------------------------------------------------------------------------------

# Method used to project a vector --------------------------------------------------------------------------------------
def project_vector(vector: list, fromSystem: list, toSystem: list) -> np.ndarray: 

    """
    Method used to project a vector from a coordinate system to another.

    Args:
        vector: list -> vector to be projected.  
        fromSystem: list -> original system. 
        toSystem: list -> destination system. 

    Returns:
        projectedVector: ndarray 

    Calling example: 
        >>> forces = project_vector(elementForces, firstSystem, secondSystem)
    """

    fromSystem = np.array(fromSystem).reshape(3, -1)
    toSystem = np.array(toSystem).reshape(3, -1)
    vector = np.array(vector) 
    fromSystem = fromSystem/np.linalg.norm(fromSystem, axis = 1, keepdims = True)
    toSystem = toSystem/np.linalg.norm(toSystem, axis = 1, keepdims = True)

    M = np.matmul(fromSystem, toSystem.T)
    projectedVector = np.matmul(M, vector.reshape((-1, 3)).T).T

    return projectedVector.reshape(vector.shape)
# ----------------------------------------------------------------------------------------------------------------------

# Method used to obtain the angle between two systems ------------------------------------------------------------------
def angle_between_2_systems(fromSystem: list, toSystem: list, planeNormal: list) -> float:

    """
    Method used to return the rotation angle, in radians, between two coordinate systems, given also the rotation plane. 
    Args:
        fromSystem: list -> first system. 
        toSystem: list -> second system. 
        planeNormal: list -> rotation plane. 

    Returns:
        alpha: float -> angle, in radians, that the two systems form.

    Calling example: 
        >>> alpha = angle_between_2_systems(system1D, materialSystem, materialSystem[6:9])
    """

    fromSystem = np.array(fromSystem).reshape(3, -1)
    toSystem = np.array(toSystem).reshape(3, -1)
    planeNormal = np.array(planeNormal)

    fromSystem = fromSystem / np.linalg.norm(fromSystem, axis = 1, keepdims = True)
    toSystem = toSystem / np.linalg.norm(toSystem, axis = 1, keepdims = True)
    planeNormal = planeNormal / np.linalg.norm(planeNormal)

    toX = toSystem[0]
    projToX = toX - np.dot(toX, planeNormal) * planeNormal

    cosX = np.dot(fromSystem[0], projToX)
    if cosX > 1:
        cosX = 1
    elif cosX < -1:
        cosX = -1

    alpha = np.arccos(cosX)

    cosY = np.dot(fromSystem[1], projToX)
    if cosY < 0:
        alpha = - alpha

    return alpha
# ----------------------------------------------------------------------------------------------------------------------

# Method used to transforme a reference frame as a list into a matrix --------------------------------------------------
def sysToMat(system: list): 

    """
    Method used to transform a reference frame as a list of nine floats into a 3x3 matrix. 

    Args: 
        system: list 
    
    Returns: 
        matrix: np.ndarray 

    Calling example: 
        >>> sysToMat(point.ElemSystemArray)
    """
    
    matrix = np.array([system[0:3], system[3:6], system[6:9]])
    return matrix 
# ----------------------------------------------------------------------------------------------------------------------

# Method used to multiply several matrices together --------------------------------------------------------------------
def matMul(matrices: list): 

    """
    Method used to multiply several matrices without doing it manually. 

    Args: 
        matrices: list -> list of np.ndarrays that are the matrices to be multiplied. 

    Returns: 
        product: np.ndarray -> final result 

    Calling example: 
        >>> A = np.ndarray([[2, 4], [-1, 3]])
        >>> B = np.ndarray([[1, 0], [-5, 2]])
        >>> C = np.ndarray([[-3, -1], [0, 2]])
        >>> matMul([A, B, C]) 
    """
    
    product = matrices[0]
    for i in matrices[1:]: 
        product = np.matmul(product, i) 
    return product 
# ----------------------------------------------------------------------------------------------------------------------

# Method used to determine if a point is inside an element or not ------------------------------------------------------
def point_in_element(point: np.ndarray, element: N2PElement, tol: float = 0.01): 

    """
    Method used to determine if a point is inside an element or not, with a certain tolerance. This is done using the 
    auxiliary functions point_in_quad and point_in_tria. 

    Args: 
        point: np.ndarray 
        element: N2PElement -> only "CQUAD4" and "CTRIA3" elements are supported. 
        tol: float = 0.01 -> must be positive. 
    
    Returns: 
        True or False 

    Calling example: 
        >>> point = np.ndarray([0, 1, 0])
        >>> element = model.get_elements(1000) 
        >>> point_in_element(point, element) 
    """
    
    if element.TypeElement == "CQUAD4": 
        return point_in_quad(point, element, tol) 
    elif element.TypeElement == "CTRIA3": 
        return point_in_tria(point, element = element, tol = tol) 
    else: 
        N2PLog.Error.E532(element) 
        return 0 
# ----------------------------------------------------------------------------------------------------------------------

# Method used to determine if a point is inside a CQUAD4 or not --------------------------------------------------------
def point_in_quad(point: np.ndarray, element: N2PElement, tol: float = 0.01): 

    """
    Method used to determine if a point is inside a CQUAD4 element or not, with a certain tolerance. This is done using 
    the auxiliary function point_in_tria. In order to determine if the point is inside a CQUAD4 element or not, the 
    element is split in two triangles. The point will be inside the quadrilateral if it is inside one of the two 
    triangles. 

    Args: 
        point: np.ndarray 
        element: N2PElement 
        tol: float = 0.01 -> must be positive. 
    
    Returns: 
        True or False 

    Calling example: 
        >>> point = np.ndarray([0, 1, 0])
        >>> element = model.get_elements(1000) 
        >>> point_in_element(point, element) 
    """

    nodes = element.Nodes 
    p1 = np.array(nodes[0].GlobalCoords)
    p2 = np.array(nodes[1].GlobalCoords)
    p3 = np.array(nodes[2].GlobalCoords)
    p4 = np.array(nodes[3].GlobalCoords)
    if point_in_tria(point, p1, p2, p3, tol = tol): 
        return True 
    elif point_in_tria(point, p1, p3, p4, tol = tol): 
        return True 
    else: 
        return False 
# ----------------------------------------------------------------------------------------------------------------------
    
# Method used to determine if a point is inside a CTRIA3 nor not -------------------------------------------------------
def point_in_tria(point: np.ndarray, p1: np.ndarray = None, p2: np.ndarray = None, p3: np.ndarray= None, element: N2PElement= None, tol: float = 0.01): 

    """
    Method used to determine if a point is inside a CTRIA3 element (or a triangle defined by its vertices) or not, with 
    a certain tolerance. This is done using the auxiliary function barycentric_coords. In order to determine if the 
    point is inside the triangle or not, its barycentric coordinates are determined. The point will be in the triangle 
    if all of them are positive and their sum is approximately equal to one (within the aforementioned tolerance). 

    Args: 
        point: np.ndarray 
        p1: np.ndarray = None 
        p2: np.ndarray = None 
        p3: np.ndarray = None 
        element: N2PElement = None 
        tol: float = 0.01 

    Returns: 
        True or False 

    Calling example: 
        >>> point = np.ndarray([0, 1, 0])
        >>> element = model.get_elements(1000) 
        >>> point_in_element(point, element = element) 
    """
    
    if element: 
        nodes = element.Nodes 
        p1 = np.array(nodes[0].GlobalCoords)
        p2 = np.array(nodes[1].GlobalCoords)
        p3 = np.array(nodes[2].GlobalCoords)
    coords = barycentric_coords(point, p1, p2, p3)
    if all(coords > np.array([0, 0, 0])) and abs(sum(coords) - 1) < tol: 
        return True 
    else: 
        return False 
# ----------------------------------------------------------------------------------------------------------------------

# Method used to obtain the barycentric coordinates --------------------------------------------------------------------
def barycentric_coords(point: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray): 

    """
    Method used to determine the barycentric coordinates of a point with respect to a triangle with vertices (a, b, c). 
    The barycentric coordinates are defined as 
        alpha = Area of the BCP triangle / Area of the ABC triangle 
        beta = Area of the ACP triangle / Area of the ABC triangle 
        gamma = Area of the ABP triangle / Area of the ABC triangle 
    Take note that this method should only be used within the point_in_tria one, as the barycentric coordinates may be 
    defined in an incorrect order. 

    Args: 
        point: np.ndarray 
        a: np.ndarray -> first vertex of the triangle 
        b: np.ndarray -> second vertex of the triangle 
        c: np.ndarray -> third vertex of the triangle 

    Returns: 
        alpha, beta, gamma: barycentric coordinates 

    Calling example: 
        >>> point = np.ndarray([2, 0, 1])
        >>> a, b, c = np.ndarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
        >>> barycentric_coords(point, a, b, c) 
    """

    ab = b - a 
    ac = c - a 
    pc = c - point 
    pb = b - point 
    pa = a - point 
    A0 = np.linalg.norm(np.cross(ab, ac)) 
    Apcb = np.linalg.norm(np.cross(pc, pb)) 
    Apca = np.linalg.norm(np.cross(pc, pa)) 
    Apba = np.linalg.norm(np.cross(pb, pa))
    alpha = Apcb / A0 
    beta = Apca / A0 
    gamma = Apba/ A0
    return alpha, beta, gamma 
# ----------------------------------------------------------------------------------------------------------------------

# Method used to project a point into the plane of an element ----------------------------------------------------------
def project_point(point: np.ndarray, element: N2PElement): 

    """
    Method used to project a point into an element. This is done simply by projecting the point into the plane defined 
    by the three first nodes in the element, so a point cannot be projected into an element with less than three nodes 
    (such as a CFAST).

    Args: 
        point: np.ndarray 
        element: N2PElement 
    
    Returns: 
        projection: np.ndarray 

    Calling example: 
        >>> point = np.ndarray([0, 1, 0])
        >>> element = model.get_elements(1000) 
        >>> point_in_element(point, element = element) 
    """

    nodes = element.Nodes 
    if len(nodes) < 3: 
        N2PLog.Error.E533(element) 
    p1 = np.array(nodes[0].GlobalCoords)
    p2 = np.array(nodes[1].GlobalCoords)
    p3 = np.array(nodes[2].GlobalCoords)
    v1 = p2 - p1 
    v2 = p3 - p1 
    n = np.cross(v1,v2) 
    A, B, C = n 
    D = -(A * p1[0] + B * p1[1] + C * p1[2])
    d = (A * point[0] + B * point[1] + C * point[2] + D) / (A**2 + B**2 + C**2)
    projection = point - d*n  
    return projection 
# ----------------------------------------------------------------------------------------------------------------------

# Method used to do the necessary transformations to later interpolate adequately -------------------------------------- 
def transformation_for_interpolation(cornerPoints: np.ndarray, centroid: np.ndarray, point: np.ndarray, elementSystem = np.ndarray, 
                                     globalSystem = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
    
    """
    Method used to transform the nodes of an element and a point in it from the global system to the element system of 
    the element centered in the centroid.

    Args:
        cornerPoints: ndarray -> nodes of the element to be transformed.
        centroid: ndarray -> centroid of the element.
        point: ndarray -> point to be transformed.
        elementSystem: ndarray -> element coordinate system 
        globalSystem: list = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] -> global coordinate system 

    Returns:
        transformedNodes, transformedPoint

    Calling example: 
        >>> cornerCoordElem, pointCoordElem = transformation_for_interpolation(cornerCoordsGlobal, centroid, 
                                                                               boxPoints, elementSystemBoxPoint)
    """

    # Definition of the nodes and point with regards to the Global Refererence frame located in the centroid
    nodesVector = [i - centroid for i in cornerPoints]
    pointVector = point - centroid 

    # Transformation from the Global Reference Frame to the Element System with regards to the centroid.
    transformedNodes = [rotate_vector(i, globalSystem, elementSystem) for i in nodesVector]
    transformedNodes = np.array([i.tolist() for i in transformedNodes])

    transformedPoint = rotate_vector(pointVector, globalSystem, elementSystem)

    return transformedNodes, transformedPoint
# ----------------------------------------------------------------------------------------------------------------------