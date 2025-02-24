from __future__ import annotations
from NaxToPy.Core.Classes.N2PNastranInputData import * 
from NaxToPy.Core.Classes.N2PAbaqusInputData import * 
from NaxToPy.Core.N2PModelContent import N2PModelContent 
from NaxToPy.Core.Classes.N2PElement import N2PElement
from NaxToPy.Core.Classes.N2PNode import N2PNode
import numpy as np
from NaxToPy import N2PLog
from NaxToPy.Modules.Fasteners._N2PFastenerAnalysis.Core.Functions.N2PRotation import * 
from NaxToPy.Modules.Fasteners._N2PFastenerAnalysis.Core.Functions.N2PInterpolation import interpolation
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from NaxToPy.Modules.Fasteners.Joints.N2PJoint import N2PJoint
    from NaxToPy.Modules.Fasteners.Joints.N2PBolt import N2PBolt

class N2PPlate: 

    """
    Class that represents a single plate. 

    Attributes: 
        id: int -> internal ID. 
        global_id: list[int] -> list of the global IDs of the N2PElements that make up the N2PPlate. 
        solver_id: list[int] -> list of the solver IDs of the N2PElements that make up the N2PPlate. 
        plate_central_cell_solver_id: int -> solver ID of one N2PElement that could represent the entire N2PPlate. 
        cards: list[N2PCard] -> list of the N2PCards of the N2PElements that make up the N2PPlate. It could contain 
        nulls/nones, like when dealing with .op2 files. 
        joint: N2PJoint -> N2PJoint associated to the N2PPlate. Several N2PPlates will be associated to the same 
        N2PJoint. 
        element_list: list[N2PElement] -> list of N2PElements associated to the N2PPlate. 
        bolt_element_list: dict[str, N2PElement] -> dictionary in the form 
        {CFAST A: N2PElement 1, CFAST B: N2PElement 2}, representing corresponding to the A and B CFASTs associated to 
        the plate. If one of the CFAST is not present, 0 is displayed. 
        attachment_id: int -> ID that the plate receives when it goes through get_attachments
        intersection: list[float] -> intersection point between the N2PPlate and its N2PBolt. 
        distance: float -> distance from the N2PPlate's edge and its N2PBolt. 
        normal: list[float] -> perpendicular direction to the N2PPlate. 
        no_adjacents: bool = False -> internal flag showing if there are not enough adjacent elements in the bypass 
        loads calculations. 
        switched_bolt_elements: bool = False -> internal flag showing if the CFASTs have been switched, which must be 
        considered to calculate the 1D forces. 
        self._projection_tolerance: float = 0.01 -> internal indicator of the projection tolerance used in the 
        obtention of the bypass box. 
        bearing_force: dict[int, list[float]] -> dictionary in the form {Load Case ID: [FX, FY, FZ]} corresponding to 
        Altair's 1D force.
        translational_fastener_forces: dict[int, list[list[float]]] -> dictionary in the form 
        {Load Case ID: [[FX, FY, FZ], [FX, FY, FZ]]} corresponding to the 1D forces that each the N2PElements 
        associated to the N2PBolt associated to the N2PPlate experience. 
        nx_bypass: dict[int, float] -> dictionary in the form {Load Case ID: Nx} corresponding to the bypass force in 
        the x axis. 
        nx_total: dict[int, float] -> dictionary in the form {Load Case ID: Nx} corresponding to the total force in the
        x axis. 
        ny_bypass: dict[int, float] -> dictionary in the form {Load Case ID: Ny} corresponding to the bypass force in 
        the y axis. 
        ny_total: dict[int, float] -> dictionary in the form {Load Case ID: Ny} corresponding to the total force in the
        y axis. 
        nxy_bypass: dict[int, float] -> dictionary in the form {Load Case ID: Nxy} corresponding to the bypass force in 
        the xy axis. 
        nxy_total: dict[int, float] -> dictionary in the form {Load Case ID: Nxy} corresponding to the total force in 
        the xy axis. 
        mx_total: dict[int, float] -> dictionary in the form {Load Case ID: Mx} corresponding to the total moment in 
        the x axis. 
        my_total: dict[int, float] -> dictionary in the form {Load Case ID: My} corresponding to the total moment in 
        the y axis. 
        mxy_total: dict[int, float] -> dictionary in the form {Load Case ID: Mxy} corresponding to the total moment in 
        the xy axis. 
        bypass_max: dict[int, float] -> dictionary in the form {Load Case: N} corresponding to the maximum bypass force. 
        bypass_min: dict[int, float] -> dictionary in the form {Load Case: N} corresponding to the minimum bypass force. 
        box_dimension: float -> dimension of the box used in the bypass calculations. 
        box_system: list[float] -> box coordinate system used in the bypass calculations. 
        box_points: dict[int, np.array] -> dictionary in the form {1: coords, 2: coords, ..., 8: coords} including each 
        point's coordinates that was used for the bypass calculations. 
        box_elements: dict[int, N2PElement] -> dictionary in the form {1: N2PElement 1, 2: N2PElement 2, ..., 
        8: N2PElement 8} including the element in which each point is located. 
        box_fluxes: dict[dict[int, list[float]]] -> dictionary in the form 
        {Load Case ID: {1: [FXX, FYY, FXY, MXX, MYY, MXY], 2: [], ..., 8: []}} including fluxes associated to each 
        box point. 
    """

    __slots__ = ("__info__", 
                 "__input_data_father__", 
                 "_id", 
                 "_global_id", 
                 "_solver_id", 
                 "_plate_central_cell_solver_id", 
                 "_cards", 
                 "_joint", 
                 "_element_list", 
                 "_bolt_element_list", 
                 "_bolt_direction", 
                 "_cfast_factor", 
                 "_attachment_id", 
                 "_intersection", 
                 "_distance", 
                 "_normal", 
                 "_no_adjacents", 
                 "_projection_tolerance", 
                 "_bearing_force", 
                 "_translational_fastener_forces", 
                 "_nx_bypass", 
                 "_nx_total", 
                 "_ny_bypass", 
                 "_ny_total", 
                 "_nxy_bypass", 
                 "_nxy_total", 
                 "_mx_total", 
                 "_my_total", 
                 "_mxy_total", 
                 "_bypass_max", 
                 "_bypass_min", 
                 "_bypass_sides", 
                 "_box_dimension", 
                 "_box_system", 
                 "_box_points", 
                 "_box_elements", 
                 "_box_fluxes")

    # N2PPlate constructor    ------------------------------------------------------------------------------------------
    def __init__(self, info, input_data_father): 

        self.__info__ = info 
        self.__input_data_father__ = input_data_father 

        self._id: int = int(self.__info__.ID)
        self._global_id: list[int] = list(self.__info__.GlobalIds)
        self._solver_id: list[int] = list(self.__info__.SolverIds)
        self._plate_central_cell_solver_id: int = int(self.__info__.PlateCentralCellSolverId)
        if self._plate_central_cell_solver_id not in self._solver_id: 
            self._solver_id.append(self._plate_central_cell_solver_id)
        self._cards: list[N2PCard] = [self.__input_data_father__._N2PNastranInputData__dictcardscston2p[i] for i in self.__info__.Cards if self.__info__.Cards[0] is not None]

        self._joint: N2PJoint = None 
        self._element_list: list[N2PElement] = None 
        self._bolt_element_list: dict[str, N2PElement] = None
        self._bolt_direction: dict[str, str] = None 
        self._cfast_factor: dict[str, int] = None 

        self._attachment_id: int = self.ID 

        self._intersection: list[float] = None 
        self._distance: float = None 
        self._normal: list[float] = None 

        self._no_adjacents: bool = False 
        self._projection_tolerance: float = 0.01

        self._bearing_force: dict[int, list[float]] = {} 
        self._translational_fastener_forces: dict[int, list[list[float]]] = {}
        self._nx_bypass: dict[int, float] = {}
        self._nx_total: dict[int, float] = {}
        self._ny_bypass: dict[int, float] = {}
        self._ny_total: dict[int, float] = {}
        self._nxy_bypass: dict[int, float] = {}
        self._nxy_total: dict[int, float] = {}
        self._mx_total: dict[int, float] = {}
        self._my_total: dict[int, float] = {}
        self._mxy_total: dict[int, float] = {}
        self._bypass_max: dict[int, float] = {}
        self._bypass_min: dict[int, float] = {}
        self._bypass_sides: dict[int, list[float]] = {}
        self._box_dimension: float = None
        self._box_system: list[float] = None 
        self._box_points: dict[int, np.array] = {}
        self._box_elements: dict[int, N2PElement] = {} 
        self._box_fluxes: dict[dict[int, list[float]]] = {}
    # ------------------------------------------------------------------------------------------------------------------
        
    # Getters ----------------------------------------------------------------------------------------------------------
    @property 
    def ID(self) -> int: 

        """
        Property that returns the id attribute, that is, the internal identificator. 
        """

        return self._id
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def GlobalID(self) -> list[int]: 

        """
        Property that returns the global_id attribute, that is, the global identificator. 
        """
        
        return self._global_id
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def SolverID(self) -> list[int]: 

        """
        Property that returns the solver_id attribute, that is, the solver IDs of the N2PElements that make up the 
        plate. 
        """
        
        return self._solver_id
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def PlateCentralCellSolverID(self) -> int: 

        """
        Property that returns the plate_central_cell_solver_id attribute, that is, the solver ID of one representative 
        N2PElement that makes up the plate. 
        """
        
        return self._plate_central_cell_solver_id
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Cards(self) -> list[N2PCard]: 

        """
        Property that returns the cards attribute, that is, the list of the N2PCards associated with the N2PPlate's 
        N2PElements. 
        """
        
        return self._cards
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Joint(self) -> N2PJoint:

        """
        Property that returns the joint attribute, that is, the N2PJoint associated to the plate. 
        """

        return self._joint
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Bolt(self) -> N2PBolt:

        """
        Property that returns the bolt attribute, that is, the N2PBolt associated to the plate. 
        """
    
        return self.Joint.Bolt
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def ElementList(self) -> list[N2PElement]: 

        """
        Property that returns the element_list attribute, that is, the list of N2PElements that make up the plate. 
        """
        
        return self._element_list
    # ------------------------------------------------------------------------------------------------------------------
    
    @property
    def BoltElementList(self) -> dict[str, N2PElement]: 

        """
        Property that returns the bolt_element_list attribute, that is, the dictionary of the CFAST that are joined to 
        the plate. 
        """
        
        return self._bolt_element_list
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def BoltDirection(self) -> dict[str, str]: 

        """
        Property that returns the bolt_direction attribute, that is, the dictionary of the orientation of the CFASTs 
        that are joined to the plate. 
        """

        return self._bolt_direction
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def CFASTFactor(self) -> dict[str, int]: 

        """
        Property that returns the cfast_factor attribute, that is, the dictionary of the factor (0, +1 or -1) which 
        should be included in the exported results of the PAG forces. 
        """

        return self._cfast_factor
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def ElementIDList(self) -> list[int]: 

        """
        Property that returns the list of the IDs of the N2PElements that make up a plate. 
        """
        
        return [j.ID for j in self.ElementList]
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def ElementInternalIDList(self) -> list[int]: 

        """
        Property that returns the unique internal ID of the N2PElements that make up the plate.  
        """

        return [j.InternalID for j in self.ElementList]
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def NodeList(self) -> list[N2PNode]: 

        """
        Property that returns the list of N2PNodes that make up the plate. 
        """
        
        return [j.Nodes for j in self.ElementList]
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def PartID(self) -> list[str]: 

        """
        Property that returns the part ID of eache element that makes up the plate. 
        """

        return [j.PartID for j in self.ElementList]
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def AttachmentID(self) -> int: 

        """
        Property that returns the attachment_id attribute, that is, the plate's internal ID when it goes through the 
        get_attachments() function.
        """
        
        return self._attachment_id
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Intersection(self) -> list[float]: 

        """
        Property that returns the intersection attribute, that is, the point where the bolt pierces the plate. 
        """
    
        return self._intersection
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Distance(self) -> list[float]: 

        """
        Property that returns the distance attribute, that is, the distance between the bolt and the plate's edge. 
        """
        
        return self._distance
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Normal(self) -> list[float]: 

        """
        Property that returns the normal attribute, that is, the direction perpendicular to the plate's plane. 
        """
        
        return self._normal
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BearingForce(self) -> dict[int, list[float]]: 

        """
        Property that returns the bearing_force attribute, that is, the 1D force that the plate experiences.
        """

        return self._bearing_force
    # ------------------------------------------------------------------------------------------------------------------
    
    @property
    def TranslationalFastenerForces(self) -> dict[int, list[list[float]]]: 

        """
        Property that returns the translational_fastener_forces attribute, that is, the 1D force that each fastener 
        experiences. 
        """

        return self._translational_fastener_forces
    # ------------------------------------------------------------------------------------------------------------------
    
    @property
    def NxBypass(self) -> dict[int, float]: 

        """
        Property that returns the nx_bypass attribute, that is, the bypass load that the plate experiences in the 
        x-axis. 
        """

        return self._nx_bypass
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def NxTotal(self) -> dict[int, float]: 

        """
        Property that returns the nx_total attribute, that is, the total load that the plate experiences in the x-axis. 
        """

        return self._nx_total
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def NyBypass(self) -> dict[int, float]: 

        """
        Property that returns the ny_bypass attribute, that is, the bypass load that the plate experiences in the 
        y-axis. 
        """

        return self._ny_bypass
    # ------------------------------------------------------------------------------------------------------------------
    
    @property
    def NyTotal(self) -> dict[int, float]: 

        """
        Property that returns the ny_total attribute, that is, the total load that the plate experiences in the y-axis. 
        """

        return self._ny_total
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def NxyBypass(self) -> dict[int, float]: 

        """
        Property that returns the nxy_bypass attribute, that is, the bypass load that the plate experiences in the 
        xy-axis. 
        """

        return self._nxy_bypass
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def NxyTotal(self) -> dict[int, float]: 

        """
        Property that returns the nxy_total attribute, that is, the total load that the plate experiences in the 
        xy-axis. 
        """

        return self._nxy_total
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def MxTotal(self) -> dict[int, float]: 

        """
        Property that returns the mx_total attribute, that is, the total moment that the plate experiences in the 
        x-axis. 
        """

        return self._mx_total
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def MyTotal(self) -> dict[int, float]: 

        """
        Property that returns the my_total attribute, that is, the total moment that the plate experiences in the 
        y-axis. 
        """

        return self._my_total
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def MxyTotal(self) -> dict[int, float]: 

        """
        Property that returns the mxy_total attribute, that is, the total moment that the plate experiences in the 
        xy-axis. 
        """

        return self._mxy_total
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def BypassMax(self) -> dict[int, float]: 

        """
        Property that returns the bypass_max attribute, that is, the maximum bypass load that the plate experiences. 
        """

        return self._bypass_max
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def BypassMin(self) -> dict[int, float]: 

        """
        Property that returns the bypass_min attribute, that is, the minimum bypass load that the plate experiences. 
        """

        return self._bypass_min
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BypassSides(self) -> dict[int, list[float]]: 

        """
        Property that retuns the bypass_sides attribute, that is, the bypass loads in the north, south, east and west 
        sides of the box. 
        """

        return self._bypass_sides
    # ------------------------------------------------------------------------------------------------------------------
    
    @property
    def BoxDimension(self) -> float: 

        """
        Property that returns the box_dimension attribute, that is, the length of the side of the box that is used in 
        the bypass loads calculation. 
        """
        
        return self._box_dimension
    # ------------------------------------------------------------------------------------------------------------------
    
    @property
    def BoxSystem(self) -> list[float]: 

        """
        Property that returns the box_system attribute, that is, the reference frame of the box used in the bypass 
        loads calculation. 
        """
        
        return self._box_system
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BoxPoints(self) -> dict[int, np.array]: 

        """
        Property that returns the box_points attribute, that is, the coordinates of each point that makes up the box 
        used in the bypass loads calculation. 
        """
        
        return self._box_points
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BoxElements(self) -> dict[int, np.array]: 

        """
        Property that returns the box_elements attribute, that is, the N2PElement associated to each point that makes 
        up the box used in the bypass loads calculations.
        """
        
        return self._box_elements
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BoxFluxes(self) -> dict[dict[int, list[float]]]: 

        """
        Property that returns the box_fluxes attribute, that is, the fluxes (in every direction) that every point that 
        makes up the box used in the bypass loads calculation experience. 
        """
        
        return self._box_fluxes
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to obtain the box used in the bypass loads calculations ----------------------------------------------
    def get_box_PAG(self: N2PPlate, model: N2PModelContent, domain: list, materialFactor: float = 4.0, areaFactor: float = 2.5, maxIterations: int = 200, projTol: float = 0.01, 
                    increaseTol: float = 10): 

        """
        Method used to obtain a plate's bypass box. 

        Args: 
            model: N2PModelContent 
            domain: list -> list of all CQUAD4 and CTRIA3 elements in the model, as obtained in get_bypass_loads_PAG. 
            materialFactor: float = 4.0 
            areaFactor: float = 2.5 
            maxIterations: int = 200 
            projTol: float = 0.01 
            increaseTol: float = 10 -> percentage that the projection tolerance increases if a point has not been 
            found. By default, it is 10%, so the projection tolerance would be multiplied by 1.1. 

        Calling example: 
            >>> myPlate.get_box_PAG(model, domain) 
        """
    
        supportedElements = ["CQUAD4", "CTRIA3"]
        boxDimension = 0.4*areaFactor*materialFactor*self.Joint.Diameter 
        boxSemiDiag = 0.5*boxDimension*(2**0.5)
        boltElement = self.ElementList[0]

        intersectionPlate = np.array(self.Intersection)
        self._box_dimension = boxDimension 

        # Box reference frame is defined
        boxSystem = self.ElementList[0].MaterialSystemArray
        xBox = np.array(boxSystem[0:3])
        yBox = np.array(boxSystem[3:6])
        self._box_system = [float(i) for i in boxSystem] 
        # The box's boundary is created
        boxPoints = {1: intersectionPlate - 0.5*boxDimension*(yBox + xBox), 
                     2: intersectionPlate - 0.5*boxDimension*yBox, 
                     3: intersectionPlate - 0.5*boxDimension*(yBox - xBox), 
                     4: intersectionPlate + 0.5*boxDimension*xBox, 
                     5: intersectionPlate + 0.5*boxDimension*(yBox + xBox), 
                     6: intersectionPlate + 0.5*boxDimension*yBox, 
                     7: intersectionPlate - 0.5*boxDimension*(xBox - yBox), 
                     8: intersectionPlate - 0.5*boxDimension*xBox}
        boxPointsFound = {i: False for i in boxPoints.keys()}
        boxPointsElements = {i: None for i in boxPoints.keys()}
        self._projection_tolerance = projTol 
        # Elements in the box are identified 
        for i in boxPoints.keys(): 
            if all(boxPointsFound.values()): 
                break 
            minDistance = 0 
            candidateElements = [boltElement]
            seenCandidates = [] 
            # Adjacent elements will be evaluated until the distance from the bolt to them is greater than the
            # semidiagonal of the box. After this it is assured that no more points will be found far away and it
            # does not make sense to keep looking. The exception is when the element size is greater than the
            # box. In the case that some points are still be assigned, we can conclude that they lie outside the edge 
            # of the plate and should be projected.
            for iter in range(maxIterations): 
                if minDistance < boxSemiDiag: 
                    for j in candidateElements: 
                        # Candidate elements are checked 
                        if point_in_element(boxPoints[i], j, projTol): 
                            boxPointsFound[i] = True 
                            boxPointsElements[i] = j 
                            break 
                    if boxPointsFound[i]: 
                        break
                    adjacentElements = [k for k in model.get_elements_adjacent(candidateElements, domain) 
                                        if (isinstance(k, N2PElement) and k.TypeElement in supportedElements)]
                    if len(adjacentElements) < 2: 
                        # If there are not enough adjacent elements, there is a problem with the geometry of the plate (for example, 
                        # the loaded model does not include enough elements near the plates)
                        self._no_adjacents = True 
                        self._box_points = {j: np.zeros(3) for j in range(8)}
                        self._box_elements = {j: None for j in range(8)}
                        break 
                    # Candidate elements list is updated 
                    seenCandidates = list(set(seenCandidates + candidateElements))
                    candidateElements = [k for k in adjacentElements if k not in seenCandidates]
                    if len(candidateElements) == 0: 
                        N2PLog.Error.E508(self)
                        return None
                    candidateElementsNodes = np.array(list(set([k.GlobalCoords for l in candidateElements for k in l.Nodes])))
                    # Minimum distance is updated 
                    if len(candidateElementsNodes) > 0: 
                        minDistance = np.min(np.linalg.norm(intersectionPlate.transpose() - candidateElementsNodes, axis = 1))
                else: 
                    if not boxPointsFound[i]: 
                        for j in seenCandidates: 
                            # If some points have not been yet found, they may not be in the plane of the elements that 
                            # have been seen, so they are projected. 
                            projectedPoint = project_point(boxPoints[i], j) 
                            if point_in_element(projectedPoint, j, projTol): 
                                boxPointsFound[i] = True 
                                boxPoints[i] = projectedPoint 
                                boxPointsElements[i] = j 
                                break 
                    else: 
                        break 
                    # If some point still have not been found, a higher tolerance is used, which may solve the problem, 
                    # assuming, the user wants to increase the tolerance. 
                    if not boxPointsFound[i] and increaseTol > 0: 
                        minDistance = 0 
                        candidateElements = [boltElement]
                        seenCandidates = [] 
                        projTol = (1 + 0.01*increaseTol)*projTol 
                        self._projection_tolerance = max(self._projection_tolerance, projTol)
                if iter == maxIterations - 1: 
                    N2PLog.Error.E507(self)
                    return 0
        self._box_points = boxPoints 
        self._box_elements = boxPointsElements 
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to obtain the bypass loads of the plate -------------------------------------------------------------- 
    def get_bypass_PAG(self, model: N2PModelContent, domain: list, results: dict, cornerData: bool = False, projTol: float = 0.01): 

        """
        Method used to obtain the plate's bypass loads, once the box has been created. 

        Args: 
            model: N2PModelContent 
            domain: list 
            results: dict 
            cornerData: bool = False 
        """

        supportedElements = ["CQUAD4", "CTRIA3"]
        boltElement = self.ElementList[0]
        
        # If there are not enough adjacent elements (2 or less), an error is displayed and all dictionaries are 
        # filled with zeros. 
        if self._no_adjacents: 
            N2PLog.Warning.W520(self)
            for i in list(results.keys()):

                self._nx_bypass[i] = 0
                self._nx_total[i] = 0
                self._ny_bypass[i] = 0
                self._ny_total[i] = 0
                self._nxy_bypass[i] = 0
                self._nxy_total[i] = 0
                self._mx_total[i] = 0
                self._my_total[i] = 0
                self._mxy_total[i] = 0
                self._bypass_max[i] = 0
                self._bypass_min[i] = 0
                self._box_fluxes[i] = {1: np.zeros(6).tolist(), 2: np.zeros(6).tolist(), 3: np.zeros(6).tolist(), 4: np.zeros(6).tolist(),
                                       5: np.zeros(6).tolist(), 6: np.zeros(6).tolist(), 7: np.zeros(6).tolist(), 8: np.zeros(6).tolist()}
        else:         
            if cornerData: 
                resultDict = {}
                elementNodal = model.elementnodal()
                boxPointForces = {i: None for i in self.BoxPoints.keys()}
                # Forces and moments are obtained in each box points
                for i in self.BoxPoints.keys(): 
                    pointElement = self.BoxElements.get(i) 
                    elementSystemBoxPoint = pointElement.ElemSystemArray 
                    elementForces = []
                    resultForPoint = {j: None for j in results.keys()}
                    resultForNode = {j.ID: None for j in pointElement.Nodes}
                    for j in pointElement.Nodes: 
                        unsewNode = [k for k in elementNodal.keys() if j.ID == elementNodal.get(k)[1]]
                        unsewElementIDs = [elementNodal.get(k)[2] for k in elementNodal.keys() if j.ID == elementNodal.get(k)[1]]
                        unsewElement2 = [k for k in j.Connectivity if (isinstance(k, N2PElement) and k.TypeElement in supportedElements)]
                        unsewElement2IDs = [k.ID for k in unsewElement2]
                        indexNoElement = [k for k, l in enumerate(unsewElementIDs) if l not in unsewElement2IDs]
                        for k in reversed(indexNoElement): 
                            del unsewElementIDs[k]
                            del unsewNode[k]
                        unsewElement = sorted(unsewElement2, key = lambda x: unsewElementIDs.index(x.ID))
                        elementFrames = [k.ElemSystemArray for k in unsewElement]
                        # It looks like Altair ignores elements that are not coplanar when obtaining the forces in the box points
                        adjacentElements = [k for k in model.get_elements_adjacent(pointElement, domain = domain) 
                                            if (isinstance(k, N2PElement) and k.TypeElement in supportedElements)]
                        adjacentElementsBolt = [k for k in model.get_elements_adjacent(boltElement, domain = domain) 
                                                if (isinstance(k, N2PElement) and k.TypeElement in supportedElements)]
                        faceElements = model.get_elements_by_face(boltElement, domain = adjacentElements + adjacentElementsBolt, tolerance_angle = 15)
                        eliminateIndex = [k for k, l in enumerate(unsewElement) if l not in faceElements]
                        # Eliminate elements from lists using the stored indexes.
                        for k in reversed(eliminateIndex): 
                            del elementFrames[k]
                            del unsewNode[k]
                            del unsewElement[k]
                            del unsewElementIDs[k]
                        
                        resultForNodeLC = {k: None for k in results.keys()}
                        for k, l in results.items(): 
                            # Results are obtained in the corners 
                            fxC = l.get("FX CORNER")
                            fyC = l.get("FY CORNER")
                            fxyC = l.get("FXY CORNER")
                            mxC = l.get("MX CORNER")
                            myC = l.get("MY CORNER")
                            mxyC = l.get("MXY CORNER")
                            elementForces = []
                            unsewNodesForces = [[fxC[m], fyC[m], fxyC[m], mxC[m], myC[m], mxyC[m]] for m in unsewNode]
                            for m in unsewNodesForces: 
                                if len(m) != 6: 
                                    N2PLog.Error.E509(self)
                                    return None
                            unsewNodesForcesRot = [rotate_tensor2D(elementFrames[m], elementSystemBoxPoint, elementSystemBoxPoint[6:9], unsewNodesForces[m]) 
                                                    for m in range(len(unsewNode))]
                            # Mean forces are obtained 
                            resultForNodeLC[k] = np.mean(unsewNodesForcesRot, axis = 0)
                        
                        resultForNode[j.ID] = resultForNodeLC 
                    keysFirstElem = set(resultForNode[next(iter(resultForNode))].keys()) 
                    elementForces = {k: [] for k in keysFirstElem}
                    for k in keysFirstElem: 
                        for l in resultForNode.values(): 
                            if k in l: elementForces[k].append(l[k])
                            else: elementForces[k].append(None)

                    for k, l in elementForces.items(): 
                        # Interpolation from corner to box points 
                        cornerCoordsGlobal = np.array([m.GlobalCoords for m in pointElement.Nodes])
                        centroid = pointElement.Centroid 
                        cornerCoordElem, pointCoordElem = transformation_for_interpolation(cornerCoordsGlobal, centroid, self.BoxPoints.get(i), elementSystemBoxPoint)
                        interpolatedForces = interpolation(pointCoordElem, cornerCoordElem, l, tol = self._projection_tolerance)
                        interpolatedForcesRot = rotate_tensor2D(elementSystemBoxPoint, boltElement.MaterialSystemArray, elementSystemBoxPoint[6:9], interpolatedForces)
                        resultForPoint[k] = interpolatedForcesRot 
                    boxPointForces[i] = resultForPoint
                for i, j in boxPointForces.items(): 
                    for k, l in j.items(): 
                        if k not in resultDict: resultDict[k] = {} 
                        resultDict[k][i] = l

            else: 
                resultDict = {}
                # Forces and moments are obtained in each box points
                boxPointForces = {i: None for i in self.BoxPoints.keys()}
                for i in self.BoxPoints.keys(): 
                    pointElement = self.BoxElements.get(i) 
                    elementSystemBoxPoint = pointElement.ElemSystemArray 
                    neighborElements = [j for j in model.get_elements_adjacent(cells = pointElement) if (isinstance(j, N2PElement) and j.TypeElement in supportedElements)]
                    # It is determined whether the elements are coplanar or not 
                    adjacentElementsBolt = [j for j in model.get_elements_adjacent(boltElement, domain = domain) 
                                            if (isinstance(j, N2PElement) and j.TypeElement in supportedElements)]
                    # It looks like Altair ignores elements that are not coplanar when obtaining the forces in the box points
                    faceElementsPrev = model.get_elements_by_face(boltElement, domain = neighborElements + adjacentElementsBolt) \
                                        + model.get_elements_by_face(pointElement, domain = neighborElements + adjacentElementsBolt)
                    faceElements = [j for j in neighborElements if j in faceElementsPrev]
                    neighborElements = faceElements
                    resultForPoint = {j: None for j in results.keys()}
                    for j, k in results.items(): 
                        # Results are obtained in the centroid 
                        fx = k.get("FX")
                        fy = k.get("FY")
                        fxy = k.get("FXY")
                        mx = k.get("MX")
                        my = k.get("MY")
                        mxy = k.get("MXY")
                        elementForces = []
                        for l in pointElement.Nodes: 
                            nodeForces = []
                            for m in neighborElements: 
                                if l.InternalID in [n.InternalID for n in m.Nodes]: 
                                    elemSystemNeighbor = m.ElemSystemArray 
                                    n = m.InternalID 
                                    neighborForces = [fx[n], fy[n], fxy[n], mx[n], my[n], mxy[n]]
                                    if len(neighborForces) != 6: 
                                        N2PLog.Error.E509(self)
                                        return None
                                    neighborForces = rotate_tensor2D(elemSystemNeighbor, elementSystemBoxPoint, elementSystemBoxPoint[6:9], neighborForces)
                                    nodeForces.append(neighborForces)
                            nodeForces = np.array(nodeForces)
                            averageNodeForces = np.mean(nodeForces, axis = 0)
                            elementForces.append(averageNodeForces.tolist())

                        elementForces = np.array(elementForces)
                        # Interpolation from corners to box points 
                        cornerCoordsGlobal = np.array([l.GlobalCoords for l in pointElement.Nodes])
                        centroid = pointElement.Centroid 
                        cornerCoordElem, pointCoordElem = transformation_for_interpolation(cornerCoordsGlobal, centroid, self.BoxPoints.get(i), elementSystemBoxPoint)
                        interpolatedForces = interpolation(pointCoordElem, cornerCoordElem, elementForces, self._projection_tolerance)
                        interpolatedForcesRot = rotate_tensor2D(elementSystemBoxPoint, boltElement.MaterialSystemArray, elementSystemBoxPoint[6:9], interpolatedForces)
                        resultForPoint[j] = interpolatedForcesRot 
                    boxPointForces[i] = resultForPoint
                for i, j in boxPointForces.items(): 
                    for k, l in j.items(): 
                        if k not in resultDict: 
                            resultDict[k] = {} 
                        resultDict[k][i] = l 
            self._box_fluxes = resultDict

            # STEP 3. Bypass and total forces and moments are obtained 
            for i, j in resultDict.items(): 
                # Fluxes are obtained 
                side = {1: [1, 2, 3], 2: [3, 4, 5], 3: [5, 6, 7], 4: [7, 8, 1]}

                nxN = np.array([j.get(k)[0] for k in side[3]]).mean() 
                nxS = np.array([j.get(k)[0] for k in side[1]]).mean() 
                nxE = np.array([j.get(k)[0] for k in side[2]]).mean() 
                nxW = np.array([j.get(k)[0] for k in side[4]]).mean() 
                nxBypass = min((nxE, nxW), key = abs) 
                nxTotal = max((nxE, nxW), key = abs) 

                nyN = np.array([j.get(k)[1] for k in side[3]]).mean() 
                nyS = np.array([j.get(k)[1] for k in side[1]]).mean() 
                nyE = np.array([j.get(k)[1] for k in side[2]]).mean() 
                nyW = np.array([j.get(k)[1] for k in side[4]]).mean() 
                nyBypass = min((nyN, nyS), key = abs) 
                nyTotal = max((nyN, nyS), key = abs) 

                nxyN = np.array([j.get(k)[2] for k in side[3]]).mean() 
                nxyS = np.array([j.get(k)[2] for k in side[1]]).mean() 
                nxyE = np.array([j.get(k)[2] for k in side[2]]).mean() 
                nxyW = np.array([j.get(k)[2] for k in side[4]]).mean() 
                nxyBypass = min((nxyN, nxyS, nxyE, nxyW), key = abs) 
                nxyTotal = max((nxyN, nxyS, nxyE, nxyW), key = abs) 

                mxN = np.array([j.get(k)[3] for k in side[3]]).mean() 
                mxS = np.array([j.get(k)[3] for k in side[1]]).mean() 
                mxE = np.array([j.get(k)[3] for k in side[2]]).mean() 
                mxW = np.array([j.get(k)[3] for k in side[4]]).mean() 
                mxTotal = max((mxE, mxW), key = abs) 

                myN = np.array([j.get(k)[4] for k in side[3]]).mean() 
                myS = np.array([j.get(k)[4] for k in side[1]]).mean() 
                myE = np.array([j.get(k)[4] for k in side[2]]).mean() 
                myW = np.array([j.get(k)[4] for k in side[4]]).mean() 
                myTotal = max((myN, myS), key = abs) 

                mxyN = np.array([j.get(k)[5] for k in side[3]]).mean() 
                mxyS = np.array([j.get(k)[5] for k in side[1]]).mean() 
                mxyE = np.array([j.get(k)[5] for k in side[2]]).mean() 
                mxyW = np.array([j.get(k)[5] for k in side[4]]).mean() 
                mxyTotal = max((mxyN, mxyS, mxyE, mxyW), key = abs) 

                # STEP 4. The bypass tensor is rotated 
                materialSystem = boltElement.MaterialSystemArray 
                tensorToRotate = [nxBypass, nyBypass, nxyBypass, nxTotal, nyTotal, nxyTotal, mxTotal, myTotal, mxyTotal]
                for k in tensorToRotate: 
                    if not isinstance(k, float): 
                        N2PLog.Error.E509(self)
                        return None
                rotatedTensor = rotate_tensor2D(self.BoxSystem, materialSystem, materialSystem[6:9], tensorToRotate)

                self._nx_bypass[i] = rotatedTensor[0]
                self._ny_bypass[i] = rotatedTensor[1]
                self._nxy_bypass[i] = rotatedTensor[2]
                self._nx_total[i] = rotatedTensor[3]
                self._ny_total[i] = rotatedTensor[4]
                self._nxy_total[i] = rotatedTensor[5]
                self._mx_total[i] = rotatedTensor[6]
                self._my_total[i] = rotatedTensor[7]
                self._mxy_total[i] = rotatedTensor[8]

                self._bypass_max[i] = 0.5*(rotatedTensor[0] + rotatedTensor[1]) + (0.5*(rotatedTensor[0] - rotatedTensor[1])**2 + (rotatedTensor[2])**2)**0.5
                self._bypass_min[i] = 0.5*(rotatedTensor[0] + rotatedTensor[1]) - (0.5*(rotatedTensor[0] - rotatedTensor[1])**2 + (rotatedTensor[2])**2)**0.5

                self._bypass_sides[i] = [[nxN, nxS, nxE, nxW], [nyN, nyS, nyE, nyW], [nxyN, nxyS, nxyE, nxyW], 
                                         [mxN, mxS, mxE, mxW], [myN, myS, myE, myW], [mxyN, mxyS, mxyE, mxyW]]
    # ------------------------------------------------------------------------------------------------------------------