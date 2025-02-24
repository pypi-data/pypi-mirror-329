from NaxToPy.Core.N2PModelContent import N2PModelContent 
from NaxToPy.Core.Classes.N2PElement import N2PElement 
from NaxToPy.Core.Classes.N2PNode import N2PNode
from NaxToPy.Core.Classes.N2PNastranInputData import * 
from NaxToPy.Core.Classes.N2PAbaqusInputData import * 
from NaxToPy.Modules.Fasteners.Joints.N2PBolt import N2PBolt 
from NaxToPy.Modules.Fasteners.Joints.N2PPlate import N2PPlate 
from NaxToPy.Modules.Fasteners.Joints.N2PAttachment import N2PAttachment 
from NaxToPy.Modules.Fasteners.Joints.N2PFastenerSystem import N2PFastenerSystem
from NaxToPy import N2PLog
from NaxToPy.Modules.Fasteners._N2PFastenerAnalysis.Core.Functions.N2PRotation import * 
from NaxToPy.Modules.Fasteners._N2PFastenerAnalysis.Core.Functions.N2PInterpolation import interpolation
from typing import Literal 
import numpy as np 
import csv
import time

class N2PJoint: 

    """
    Class that represents a single joint, that is, a N2PBolt and a series of N2PPlate objects. 

    Attributes: 
        diameter: float = None -> joint's diameter. 
        bolt: N2PBolt -> N2PBolt associated. 
        plate_list: list[N2PPlate] -> list of unique N2PPlates associated to the N2PJoint. 
        switch_plates: bool -> boolean that shows if the joint's plates have to be switched. 
        attachment: N2PAttachment -> joint's attachment. 
        pitch: float -> joint's pitch.
        fastener_system: N2PFastenerSystem -> joint's Fastener System associated 
    """

    __slots__ = ("__info__", 
                 "__input_data_father__", 
                 "_diameter", 
                 "_bolt", 
                 "_plate_list", 
                 "_switch_plates", 
                 "_attachment", 
                 "_pitch",
                 "_fastener_system")

    # N2PJoint constructor ---------------------------------------------------------------------------------------------
    def __init__(self, info, input_data_father): 

        """
        In this constructor, the N2PBolt associated to the N2PJoint is created. Also, all N2PPlates associated to the 
        N2PJoint are created and then some of them are removed if two (or more) of them share the same solver ID (that 
        is, the same N2PElements are associated to both N2PPlates). 
        """
        
        self.__info__ = info 
        self.__input_data_father__ = input_data_father 

        self._diameter: float = None 
        self._bolt: N2PBolt = N2PBolt(self.__info__.Bolt, self.__input_data_father__) 
        self._bolt._joint = self
        
        allPlates = list(N2PPlate(self.__info__.Plates[i], self.__input_data_father__) for i in range(len(self.__info__.Plates)))
        platesID = [] 
        listPlates = [] 
        for i in allPlates: 
            if i.SolverID not in platesID: 
                platesID.append(i.SolverID)
                listPlates.append(i)
        self._plate_list: list[N2PPlate] = listPlates
        self._switch_plates: bool = False 

        self._attachment: N2PAttachment = None 
        self._pitch: float = None 
        self._fastener_system: N2PFastenerSystem = None
    # ------------------------------------------------------------------------------------------------------------------
        
    # Getters ----------------------------------------------------------------------------------------------------------
    @property 
    def Diameter(self) -> float: 

        """
        Property that returns the diameter attribute, that is, the joint's diameter. 
        """

        return self._diameter
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def Bolt(self) -> N2PBolt: 

        """
        Property that returns the bolt attribute, that is, the N2PBolt associated to the N2PJoint. 
        """
        
        return self._bolt
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def ID(self) -> int: 

        """
        Property that returns the joint's internal identificator. 
        """
    
        return self.Bolt.ID 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def TypeFastener(self) -> str: 

        """
        Property that returns the type of joint that is being used. 
        """
        
        return self.Bolt.Type
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def PlateList(self) -> list[N2PPlate]: 

        """
        Property that returns the plate_list attribute, that is, the list of N2PPlates associated to the N2PJoint. 
        """
        
        return self._plate_list
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def SwitchPlates(self) -> bool: 

        """
        Property that returns the switch_plates attribute, that is, whether the joint's plates have to be switched or 
        not. 
        """
        
        return self._switch_plates
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def PartID(self) -> int: 

        """
        Property that returns the part ID of the elements that make up the bolt. 
        """

        return self.Bolt.PartID 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BoltElementList(self) -> list[N2PElement]: 

        """
        Property that returns the list of N2PElements that make up the joint's bolt. 
        """
        
        return self.Bolt.ElementList 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BoltElementIDList(self) -> list[int]: 

        """
        Property that returns the list of the IDs of the N2PElements that make up the joint's bolt. 
        """
        
        return self.Bolt.ElementIDList
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BoltElementInternalIDList(self) -> list[int]: 

        """
        Property that returns the list of the internal IDs of the N2PElements that make up the joint's bolt.
        """

        return self.Bolt.ElementInternalIDList
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BoltNodeList(self) -> list[N2PNode]: 

        """
        Property that returns the list of N2PNodes that make up the joint's bolt. 
        """
        
        return self.Bolt.NodeList
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def PlateElementList(self) -> list[N2PElement]: 

        """
        Property that returns the list of N2PElements that make up the joint's plates. 
        """
    
        return [j.ElementList for j in self.PlateList]
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def PlateElementIDList(self) -> list[int]: 

        """
        Property that returns the list of the IDs of the N2PElements that make up the joint's plates. 
        """
        
        return [j.ElementIDList for j in self.PlateList]
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def PlateElementInternalIDList(self) -> list[int]: 

        """
        Property that returns the internal ID of the N2PElements that make up the joint's plates. 
        """

        return [j.ElementInternalIDList for j in self.PlateList]
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def PlateNodeList(self) -> list[N2PNode]: 

        """
        Property that returns the list of N2PNodes that make up the joint's plates. 
        """
        
        return [j.NodeList for j in self.PlateList]
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def PlatePartID(self) -> list[str]: 

        """
        Property that returns the part ID of each element that makes up the plates. 
        """

        return [j.PartID for j in self.PlateList]
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Attachment(self) -> N2PAttachment: 

        """
        Property that returns the attachment attribute, that is, the joint's N2PAttachment. 
        """

        return self._attachment
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Pitch(self) -> float: 

        """
        Property that returns the pitch attribute, that is, the joint's pitch. 
        """

        return self._pitch
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def FastenerSystem(self) -> N2PFastenerSystem: 

        """
        Property that returns the N2PFastenerSystem of the joint. 
        """

        return self._fastener_system
    # ------------------------------------------------------------------------------------------------------------------

    # Setters ----------------------------------------------------------------------------------------------------------
    @Diameter.setter 
    def Diameter(self, value: float) -> None: 

        if not isinstance(value, float) and not isinstance(value, int): 
            N2PLog.Warning.W527(value, float)
        else: 
            self._diameter = value
    # ------------------------------------------------------------------------------------------------------------------

    @SwitchPlates.setter 
    def SwitchPlates(self, value: bool) -> None: 

        if not isinstance(value, bool): 
            N2PLog.Warning.W527(value, bool)
        else: 
            self._switch_plates = value
    # ------------------------------------------------------------------------------------------------------------------
    
    @FastenerSystem.setter 
    def FastenerSystem(self, value: N2PFastenerSystem) -> None: 

        if not isinstance(value, N2PFastenerSystem): 
            N2PLog.Warning.W527(value, N2PFastenerSystem)
        else: 
            self._fastener_system = value
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to obtain the distance from an N2PJoint to its closest N2PPlate's edge -------------------------------
    def get_distance(self, model: N2PModelContent, domain: list[N2PElement]): 
        
        """
        Method that calculates the distance from each N2PJoint to the edge of its corresponding N2PPlates. 

        Args: 
            model: N2PModelContent 

        The following steps are followed: 
            1. The intersection points between every N2PPlate and its N2PJoint is obtained. 
            2. All the elements that are attached to the element where the intersection point is are retrieved using 
            the function “get_elements_attached”. Right after this, “get_free_edges” obtains a list of segments from  
            the attached elements which define the free edges of the selection.
            3. Finally, the distance between the intersection point to each segments is obtained and compared to the 
            rest in order to get the minimum one, which is of course the desired value. 

        Calling example: 
            >>> myJoint.get_distance(model1)
        """

        boltNodes = [j for i in self.BoltNodeList for j in i]
        boltNodes2 = []
        for i in boltNodes: 
            if i not in boltNodes2: 
                boltNodes2.append(i)
        intersection = [] 
        for i in boltNodes2: 
            intersection.append(i.GlobalCoords)
        # Of course, one distance will be needed form every N2PPlate in the N2PJoint. 
        for p in range(len(self.PlateList)): 

            if len(self.PlateList[p].ElementList) == 0: 
                N2PLog.Warning.W512(p, self)
                continue

            plateElem = self.PlateList[p].ElementList[0]

            node1 = np.array([plateElem.Nodes[0].X, plateElem.Nodes[0].Y, plateElem.Nodes[0].Z])
            node2 = np.array([plateElem.Nodes[1].X, plateElem.Nodes[1].Y, plateElem.Nodes[1].Z])
            node3 = np.array([plateElem.Nodes[2].X, plateElem.Nodes[2].Y, plateElem.Nodes[2].Z])
            normalPlane = np.cross(node3 - node1, node2 - node1) / np.linalg.norm(np.cross(node3 - node1, node2 - node1))

            self._plate_list[p]._normal = normalPlane.tolist()
            self._plate_list[p]._intersection = list(intersection[p])

            # The plate's free edges are obtained
            t1 = time.time()
            freeEdges = model.get_free_edges(model.get_elements_attached(cells = [plateElem], domain = domain))
            t2 = time.time() - t1
            
            savedDistance = float("inf")
            # Of course, the desired distance is the minimum distance to an edge, so all free edges must be searched. 
            for i in freeEdges: 
                A = np.array(i[1].GlobalCoords)
                B = np.array(i[2].GlobalCoords)
                length = np.linalg.norm(B - A) 
                ts = np.dot(intersection[p] - A, B - A) / length ** 2
                if ts <= 0: 
                    distance = np.linalg.norm(A - intersection[p]) # A is the closest point.
                elif ts >= 1: 
                    distance = np.linalg.norm(B - intersection[p]) # B is the closest point.
                else: 
                    distance = np.linalg.norm(A + ts * (B - A) - intersection[p]) # The closest point is elsewhere. 
                if distance < savedDistance: 
                    savedDistance = distance 
            self._plate_list[p]._distance = float(savedDistance)
    # ------------------------------------------------------------------------------------------------------------------
    
    # Method used to organise some forces ------------------------------------------------------------------------------
    def _organise_forces(self, forces: list) -> list: 

        """
        Method which takes a list of forces defined in the following format: 
                [[FX, FY, FZ], [FX, FY, FZ], ..., [FX, FY, FZ]] 
        and organises it in order to be consistent with the plates order and to be comfortable to export.

        Args: 
            forces: list -> list of forces to be transformed
        Returns: 
            forcesOrganised: list 

        Calling example: 
            >>> forcesOrg = myJoint._organise_forces(forces)
        """

        organisedForces = []
        if len(forces) == 1: 
            organisedForces = [[forces[0], [0, 0, 0]], [forces[0], [0, 0, 0]]]
        else: 
            organisedForces.append([forces[0], [0, 0, 0]])
            for i in range(1, len(forces)): 
                organisedForces.append([forces[i - 1], forces[i]])
            organisedForces.append([forces[len(forces) - 1], [0, 0, 0]])
        return organisedForces
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to obtain the model's forces -------------------------------------------------------------------------
    def get_forces(self, results: dict): 

        """
        Method that takes an N2PJoint element and obtains its 1D forces, as well as the 1D forces associated to each of 
        its N2PPlates. Forces will be obtained as N2PPlate or N2PBolt attributes as dictionaries in the form: 
                {Load Case ID: [FX, FY, FZ]}    or      {Load Case ID: F or Angle}
        depending on what is obtained. 

        Args: 
            results: dict -> results dictionary. 

        The following attributes are obtained: 
            - shear_force: dictionary in the form {Load Case ID: Bolt Element ID: F} which represents the 1D force in 
            the bolt's element reference frame. It is a N2PBolt attribute. 
            - axial_force: dictionary in the form {Load Case ID: Bolt Element ID: F} which represents the axial force 
            in the 1st plate's material reference frame. It will be positive if the fastener is extender or 0 if it is 
            compressed. It is a N2PBolt attribute. 
            - element_local_system_force: dictionary in the form {Load Case ID: Bolt Element ID: [FX, FY, FZ]} which 
            represents the 1D force in the 1st plate's material reference frame. It is a N2PBolt attribute. 
            - translational_fastener_forces: dictionary in the form {Load Case ID: [[FX, FY, FZ], [FX, FY, FZ]]} which 
            represents the 1D forces that each the N2PElements associated to the N2PBolt associated to the N2PPlate 
            experience. It is represented in a local reference frame, in which the x-axis is the same as the N2PPlate's 
            material reference frame's x-axis, the z-axis is coincident with the axial direction of the bolt and the 
            y-axis is obtained via the cross product. If there is only one fastener attached to the plate, the second 
            list will be filled with zeros. It is a N2PPlate attribute. 
            - bearing_force: dictionary in the form {Load Case ID: [FX, FY, FZ]} which represents the 1D force 
            experienced by the joint, as calculated by Altair. It takes into account if there are two joints attached 
            to the plate and, if so, sums up their contributions. It is represented in the local reference frame and it 
            is a N2PPlate attribute. 
            - max_axial_force: dictionary in the form {Load Case ID: Bolt Element ID: F} which represents the maximum 
            axial force of the whole joint. It is a N2PBolt attribute. 
            - load_angle: dictionary in the form {Load Case ID: Bolt Element ID: Angle} which represents the joint's 
            load angle in degrees. It is a N2PBolt attribute. 

        The following steps are followed: 
            1. All reference frames are obtained: the 1st plate's material reference frame, the bolt's N2PElement 
            reference frame and the local reference frame. 
            2. All forces are calculated according to their definition. If necessary, they are rotated so that they are 
            expressed in the correct reference frame. 
            3. If there are two joints attached to the same plate, their contributions are added. 

        It must be added that, in the original code, there was a distinction between top and bottom plates and, as 
        such, the force that the top and bottom plates experienced was also calculated. As in the modern code this 
        distinction no longer exists, this cannot be calculated. 

        Calling example: 
            >>> myForces = myJoint.get_forces(loads.Results)
        """

        plateElement = self.PlateList[0].ElementList[0]
        materialSystem = plateElement.MaterialSystemArray 
        xlocal = materialSystem[0:3]
        for i, j in results.items(): 
            elementForcesMaterial = []
            elementForcesLocal = []
            self._bolt._element_local_system_force[i] = {}
            self._bolt._axial_force[i] = {}
            self._bolt._shear_force[i] = {}
            self._bolt._load_angle[i] = {}
            for k in self.BoltElementList: 
                id = k.InternalID
                system1D = k.ElemSystemArray
                force1D = [j.get("FZ1D")[id], j.get("FY1D")[id], j.get("FX1D")[id]]
                # Local reference frame is defined
                zlocal = system1D[0:3]
                ylocal = np.cross(zlocal, xlocal)
                localSystem = [xlocal[0], xlocal[1], xlocal[2], ylocal[0], ylocal[1], ylocal[2], zlocal[0], zlocal[1], zlocal[2]]

                # Calculations regarding the shear force
                shearForce = np.array([force1D[1], force1D[2]])
                alpha = angle_between_2_systems(system1D, materialSystem, materialSystem[6:9])
                R = np.array([[np.cos(alpha), np.sin(alpha)], [-np.sin(alpha), np.cos(alpha)]])
                rotShearForce = np.matmul(R, shearForce)

                forcesToRotate = [force1D[0], force1D[1]]

                # Plate's reference frame is defined
                betaLocal = angle_between_2_systems(system1D, localSystem, localSystem[6:9])
                R2Local = np.array([[np.cos(betaLocal), np.sin(betaLocal)], [-np.sin(betaLocal), np.cos(betaLocal)]])

                F1DRotLocalXY = np.matmul(R2Local, forcesToRotate)
                F1DRotLocal = [F1DRotLocalXY[0], F1DRotLocalXY[1], force1D[2]]
                elementForcesLocal.append(F1DRotLocal)

                beta = angle_between_2_systems(system1D, materialSystem, materialSystem[6:9])
                R2 = np.array([[np.cos(beta), np.sin(beta)], [-np.sin(beta), np.cos(beta)]])

                F1DRotPrev = np.matmul(R2, forcesToRotate)
                F1DRot = [float(F1DRotPrev[0]), float(F1DRotPrev[1]), float(force1D[2])]
                elementForcesMaterial.append(F1DRot)

                # N2PBolt attributes are set
                self._bolt._element_local_system_force[i][k.ID] = F1DRot
                self._bolt._axial_force[i][k.ID] = max(0, F1DRot[2])
                self._bolt._shear_force[i][k.ID] = float(np.linalg.norm(np.array([force1D[1], force1D[2]])))
                self._bolt._load_angle[i][k.ID] = float((np.rad2deg(np.arctan2(rotShearForce[1], rotShearForce[0])) + 360) % 360)

                # Some forces are organised to be easier to export later on
                elementForcesMaterialOrg = self._organise_forces(elementForcesMaterial)
                elementForcesLocalOrg = self._organise_forces(elementForcesLocal)

            self._bolt._max_axial_force[i] = max(self.Bolt.AxialForce[i].values())

            # Calculations regarding the 1D forces applied on each plate
            for k, l in enumerate(self.PlateList): 
                elementForcesLocalOrg[k][0] = [float(m) for m in elementForcesLocalOrg[k][0]]
                elementForcesLocalOrg[k][1] = [float(m) for m in elementForcesLocalOrg[k][1]]
                l._translational_fastener_forces[i] = elementForcesLocalOrg[k]
                forces = project_vector(elementForcesMaterialOrg[k], materialSystem, l.ElementList[0].MaterialSystemArray)
                if type(forces[0].tolist()) == list: 
                    forces = [x - y for x, y in zip(forces[1], forces[0])] 
                else: 
                    forces = forces.tolist()
                forces = [float(m) for m in forces]
                l._bearing_force[i] = forces
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to obtain the model's forces, as done by PAG ---------------------------------------------------------
    def get_forces_PAG(self, results: dict): 
        """
        Method that takes an N2PJoint and obtains its 1D forces, as well as the 1D forces associated to each of its 
        N2PPlates. Forces will be obtained as N2PPlate or N2PBolt attributes as dictionaries in the form: 
                {Load Case ID: [FX, FY, FZ]}    or      {Load Case ID: F or Load Angle}
        depending on what is obtained. 

        Args: 
            results: dict -> results dictionary. 

        The following attributes are obtained: 
            - shear_force: dictionary in the form {Load Case ID: Bolt Element ID: F} which represents the 1D force in 
            the bolt's element reference frame. It is a N2PBolt attribute. 
            - axial_force: dictionary in the form {Load Case ID: Bolt Element ID: F} which represents the axial force 
            (pulltrhrough force) in the 1st plate's material reference frame. It will be positive if the fastener is 
            extended or 0 if it is compressed. It is a N2PBolt attribute. 
            - translational_fastener_forces: dictionary in the form {Load Case ID: [[FX, FY, FZ], [FX, FY, FZ]]} which 
            represents the 1D forces that each the N2PElements associated to the N2PBolt associated to the N2PPlate 
            experience. It is             represented in a local reference frame, in which the x-axis is the same as 
            the N2PPlate's material reference frame's x-axis, the z-axis is coincident with the axial direction of the 
            bolt and the y-axis is obtained via the cross product. If there is only one fastener attached to the plate, 
            the second list will be filled with zeros. It is a N2PPlate attribute. 
            - bearing_force: dictionary in the form {Load Case ID: [FX, FY, FZ]} which represents the 1D force 
            experienced by the bolt, as calculated by Altair. It takes into account if there are two CFASTs attached 
            to the plate and, if so, sums up their contributions. It is represented in the local reference frame and it 
            is a N2PPlate attribute. 
            - max_axial_force: dictionary in the form {Load Case ID: Bolt Element ID: F} which represents the maximum 
            axial force (bolt tension) of the whole bolt. It is a N2PBolt attribute.
            - load_angle: dictionary in the form {Load Case ID: Bolt Element ID: Angle} which represents the joint's 
            load angle in degrees. It is a N2PBolt attribute. 

        The following steps are followed: 
            1. Forces are adequately rotated into the plate's material reference frame. 
            2. The shear and axial forces are calculated with their formulas, as well as the load angle. 
            3. If there are two CFASTs attached to a plate, the shear and axial force may be updated. 
            4. The final force that the plate experiences (called here bearing_force) is obtained by adding the 
            contributions of both CFAST, if they exist, or taking into account if the existing CFAST is the A or B one. 

        Calling example: 
            >>> myForces = myJoint.get_forces(loads.Results)
        """
        W = np.array([[0, -1, 0], 
                      [1, 0, 0], 
                      [0, 0, 1]])
        V = np.array([[0, 0, -1],
                      [1, 0, 0],
                      [0, -1, 0]])
        for i, j in results.items(): 
            self._bolt._axial_force[i] = {}
            self._bolt._shear_force[i] = {}
            self._bolt._load_angle[i] = {}
            for k in self.PlateList: 
                matSystem = k.ElementList[0].MaterialSystemArray 
                M = sysToMat(matSystem)
                forces = [] 
                forces2 = [] 
                for l, m in k.BoltElementList.items(): 
                    if m: 
                        system1D = m.ElemSystemArray
                        id = m.InternalID
                        fx = j.get("FX1D")[id]
                        fy = -j.get("FY1D")[id]
                        fz = -j.get("FZ1D")[id]
                        f = [fz, fy, fx]
                        S = sysToMat(system1D)
                        beta = angle_between_2_systems(system1D, matSystem, matSystem[6:9])
                        R = np.array([[np.cos(beta), np.sin(beta), 0], 
                                      [-np.sin(beta), np.cos(beta), 0], 
                                      [0, 0, 1]])
                        forcesBolt = matMul([W, M, S.T, V, R, f])
                        forces.append(forcesBolt) 
                        if l == "A" and k.BoltDirection["A"] == "->": 
                            forces2.append(np.array([forcesBolt[0], forcesBolt[1], -forcesBolt[2]]))
                            self._bolt._axial_force[i][m.ID] = max(0, -forcesBolt[2])
                            self._bolt._load_angle[i][m.ID] = float((np.rad2deg(np.arctan2(forcesBolt[1], forcesBolt[0])) + 360) % 360)
                        elif l == "A" and k.BoltDirection["A"] == "<-": 
                            forces2.append(np.array([-forcesBolt[0], -forcesBolt[1], forcesBolt[2]]))
                            self._bolt._axial_force[i][m.ID] = max(0, forcesBolt[2])
                            self._bolt._load_angle[i][m.ID] = float((np.rad2deg(np.arctan2(-forcesBolt[1], -forcesBolt[0])) + 360) % 360)
                        elif l == "B" and k.BoltDirection["B"] == "->": 
                            forces2.append(np.array([-forcesBolt[0], -forcesBolt[1], forcesBolt[2]]))
                            self._bolt._axial_force[i][m.ID] = max(0, forcesBolt[2])
                            self._bolt._load_angle[i][m.ID] = float((np.rad2deg(np.arctan2(-forcesBolt[1], -forcesBolt[0])) + 360) % 360)
                        elif l == "B" and k.BoltDirection["B"] == "<-": 
                            forces2.append(forcesBolt)
                            self._bolt._axial_force[i][m.ID] = max(0, forcesBolt[2])
                            self._bolt._load_angle[i][m.ID] = float((np.rad2deg(np.arctan2(forcesBolt[1], forcesBolt[0])) + 360) % 360)
                        self._bolt._shear_force[i][m.ID] = np.linalg.norm(forcesBolt[0:2]) 
                    else: 
                        forces.append(np.array([0, 0, 0]))
                        forces2.append(np.array([0, 0, 0]))
                self._bolt._max_axial_force[i] = max(self.Bolt.AxialForce[i].values())
                altairForce = forces2[1] + forces2[0]
                if altairForce[2] < 0: 
                    altairForce[2] = 0 
                k._bearing_force[i] = altairForce 
                k._translational_fastener_forces[i] = forces2
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to calculate the model's bypass loads ----------------------------------------------------------------
    def get_bypass_loads(self, model: N2PModelContent, results: dict, cornerData: bool = False, materialFactorMetal: float = 4.0, materialFactorComposite: float = 4.5, 
                         areaFactor: float = 2.5, maxIterations: int = 200, boxTol: float = 1e-3, projTol: float = 0):

        """
        Method that takes an N2PJoint, as well as some other inputs obtained throughout the code, and obtains the 
        bypass loads of each of its associated N2PPlates. It is highly recommended to use the default inputs, but the 
        user could manually alter any of them. 

        Args: 
            model: N2PModelContent
            results: dict -> result dictionary.
            cornerData: bool = False ->  boolean which shows whether the corner data is to be used or not.
            materialFactorMetal: float = 4.0 -> material factor corresponding to metallic materials. 
            materialFactorComposite: float = 4.5 -> material factor corresponding to composite materials. 
            areaFactor: float = 2.5
            maxIterations: int = 200: maximum number of iterations. 
            boxTol: float = 1e-3 -> tolerance used to determine whether a point is inside the box or not. 
            projTol: float = 0 -> tolerance used in the projections. 

        Calling example: 
            >>> bypassLoads = myJoint.get_bypass_loads(model1, fasteners.Results)

        Procedure and methodology: 
            - The procedure is based on the crown method, so the fluxes will be calculated using a square-shaped box 
            around the joint in the plate's plane. 
            - Firstly, the box where the calculations are to be made is obtained. Its dimension is 
                    a = 0.4 * areaFactor * materialFactor * Diameter 
            - Knowing its dimension, the box should be defined with a specific orientation and order. The orientation 
            is defined by the box reference frame, which coincides with the material system of the element where the 
            joint is pierced. This may cause a small variation because the z-axis is defined as the joint's axial 
            direction, and sometimes the material system's z-axis does not coincide with it. 
            - Then, the box system's origin would be placed in the center of the box and the first point would be 
            located in (-a, a) and the other points would be placed in the clockwise direction. 
            - This does not always coincide with what Altair displays, but the final results should be the same. 
            - Adjacent elements will be evaluated until the distance from the joint to them is greater to the box's 
            semidiagonal. After this, no more points will be found further away, so the search stops here. If there are 
            still points to be assigned, it is concluded that they lie outside of the edge of the plate and therefore 
            they will be projected. 
            - If all points lie within the free edges, the process is simple. The adjacent elements to the pierced one 
            are evaluated in case that any point lies inside of it, which is done taking into consideration the 
            so-called box tolerance, stopping the iterations when the element that is being analysed is far from the 
            box location. 
            - However, there are two cases where the box point location is not as simple. Firstly, if there are points 
            outside the free edges, they are orthogonally projected onto the mesh. In the FastPPH tool used by Altair, 
            this projection does not always follow the same procedure but, to simplify, in this tool an orthogonal 
            projection is always used. 
            - The second critical case occurs when a box crosses a T-edge or gets out of a surface that does not finish 
            in a free edge. If the box crosses a T-edge, it is considered that all points are located within the free 
            edges and should not be projected. If the box gets out of the borders of a surface, and these borders are 
            not free edges, they are treated as so, and the same procedure is followed as when they were outside of 
            free edges (they are orthogonally projected). 
            - Now, the fluxes in each of the points of the boxes, for each load case, must be obtained, in order to 
            calculate the final values for bypass and total loads. There are two options to be analyzed: 

                1. cornerData = True 
                
                If the user asks for results in the corner when running the model and obtaining the corresponding 
                results, these results will be given by node and not by element, giving several values for a node, 
                related to the element where it is. This can be achieved by selecting the CORNER or BILIN describer in 
                the FORCE card. Results will be more accurate if corner data is used, as there are more values to be 
                used. 

                Taking each of the box's points, the same procedure is carried out. Firstly, the results for all nodes 
                that form the element where the box point is are retrieved. They are represented in their element 
                reference frame, so they are transformed into the same reference frame. Once 3 or 4 values for the 
                nodes are obtained (depending on wether the element is a TRIA or QUAD), a bilinear interpolation to the 
                box point from the node locations is used. 

                2. cornerData = False

                The results in the result files are retrieved in the centroid of each element, leading to results that 
                will be less precise, since results in the corners must be approximated instead of actually calculated. 
                This approximation is made by averaging the adjacent elements. Besides this, the same procedure is used 
                as in the previous case. 

            - Finally, all results are transformed into the material reference frame corresponding to the element where 
            the joint is pierced. 

            There are several checks during the program that help the user understand if there are any problems in the
            analysis. In any case, an error appears. The checks are the following: 
                1. There are less than two plates connected to the joint. 
                2. A plate does not have the necessary information (intersection, normal, distance and elements). 
                3. The joint has no diameter or it is negative. 
                4. The maximum number of iterations is reached. 
                5. There are no candidate elements to search. This should not actually occur, though, because of a 
                previous check. 
                6. There are not enough adjacent elements in the model. 
                7. Certain arrays do not have, for whatever reason, six elements. 
                8. The final rotation matrix is not well defined. 
        """

        # Only CQUAD4 and CTRIA3 elements are supported
        supportedElements = ["CQUAD4", "CTRIA3"]
        domain = [i for i in model.get_elements() if i.TypeElement in supportedElements]

        # If there are less than two plates connected to the joint, an error occurs
        if len(self.PlateList) < 2: 
            N2PLog.Error.E505(self)
            return None

        # Every plate in the joint is checked
        for p in self.PlateList: 
            if p.Intersection is None:
                N2PLog.Warning.W513(self)
                continue
            if p.Normal is None:
                N2PLog.Warning.W514(self)
                continue
            if p.Distance is None:
                N2PLog.Warning.W515(self)
                continue
            if p.ElementList is None or type(p.ElementList) == list and len(p.ElementList) == 0: 
                N2PLog.Warning.W516(self)
                continue
            # STEP 1. The box is obtained
            # The material factor is selected depending on whether the material is composite or not
            if model.PropertyDict.get(p.ElementList[0].Prop).PropertyType == "PCOMP": 
                materialFactor = materialFactorComposite
            else: 
                materialFactor = materialFactorMetal
            if self.Diameter is None or self.Diameter <= 0: 
                N2PLog.Error.E506(self)
                return None

            boxDimension = 0.4*areaFactor*materialFactor*self.Diameter 
            boxSemiDiag = 0.5*boxDimension*(2**0.5)
            boltElement = [i for i in p.ElementList if i.ID == p.PlateCentralCellSolverID][0]

            intersectionPlate = np.array(p.Intersection)
            p._box_dimension = boxDimension 

            # Box reference frame is defined
            xMat = np.array(boltElement.MaterialSystemArray[0:3])
            xBox = xMat 
            zBox = np.array(boltElement.ElemSystemArray[6:9])
            yBox = np.cross(zBox, xBox)
            boxSystem = [xBox[0], xBox[1], xBox[2], yBox[0], yBox[1], yBox[2], zBox[0], zBox[1], zBox[2]]
            p._box_system = [float(i) for i in boxSystem] 
            # The box's boundary is created
            ax = np.array([[-1.0, 0.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0]])
            ay = np.array([[ 1.0, 1.0, 1.0, 0.0, -1.0, -1.0, -1.0, 0.0]])
            boxPoints = intersectionPlate + 0.5*boxDimension*(np.matmul(ax.transpose(), xBox.reshape((1,3))) + np.matmul(ay.transpose(), yBox.reshape((1,3))))
            boxPoints = {i + 1: boxPoints[i] for i in range(len(boxPoints))}

            # STEP 2. Elements contained in the box are identified
            boxPointsFound = {i: False for i in boxPoints.keys()}
            boxPointsElements = {i: None for i in boxPoints.keys()}
            candidateElements = [boltElement]
            seenCandidates = []
            minDistance = 0 
            iterations = 0 

            # The loop will keep going as long as there are elements to be found
            while not all(boxPointsFound.values()): 
                iterations += 1
                if iterations > maxIterations: 
                    N2PLog.Error.E507(p)
                    return 0 
                
                noAdjacents = False 

                # Adjacent elements will be evaluated until the distance from the bolt to them is greater than the
                # semidiagonal of the box. After this it is assured that no more points will be found far away and it
                # does not make sense to keep looking. The exception is when the element size is greater than the
                # box. In this case the distance condition alone fails, that is why while iterations are smaller than
                # 2 it is ignored. In the case that some points are still be assigned, we can conclude that they lie
                # outside the edge of the plate and should be projected.

                # STEP 2.1. All points within free edges are located
                if minDistance < boxSemiDiag or iterations < 3: 
                    for i in boxPoints.keys(): 
                        if not boxPointsFound.get(i): 
                            for j in candidateElements: 
                                vertices = [np.array(k.GlobalCoords) for k in j.Nodes]
                                # Check if element is inside the element
                                normal = np.cross(vertices[1] - vertices[0], vertices[2] - vertices[0])
                                normal = normal/np.linalg.norm(normal)
                                pointPlaneDistance = abs(np.dot(normal, boxPoints.get(i)) - np.dot(normal, vertices[0]))
                                if pointPlaneDistance > boxTol: 
                                    continue 
                                # Check if the point is inside the convex hull of the element
                                inside = [False] * len(vertices) 
                                for k in range(len(vertices)): 
                                    edgeVector = vertices[(k + 1) % len(vertices)] - vertices[k] 
                                    toPointVector = boxPoints.get(i) - vertices[k] 
                                    crossProduct = np.cross(edgeVector, toPointVector)
                                    if np.dot(normal, crossProduct) > 0: 
                                        inside[k] = True 
                                # If all conditions are not met, the element is inside the convex hull
                                if all(inside): 
                                    boxPointsFound[i] = [True]
                                    boxPointsElements[i] = j
                    # Candidate element list is updated 
                    seenCandidates = list(set(seenCandidates + candidateElements))
                    adjacentElements = [i for i in model.get_elements_adjacent(candidateElements, domain) 
                                        if (isinstance(i, N2PElement) and i.TypeElement in supportedElements)]
                    # If there are not enough adjacent elements, bypass loads are not calculated in this plate
                    if len(adjacentElements) < 2: 
                        noAdjacents = True
                        break 
                    candidateElements = list(set(adjacentElements).difference(set(seenCandidates)))
                    if len(candidateElements) == 0: 
                        N2PLog.Error.E508(p)
                        return None
                    candidateElementsNodes = np.array(list(set([i.GlobalCoords for j in candidateElements for i in j.Nodes])))
                    # This few lines of code should not be implemented in this way, originally there was no check to 
                    # see if candidateElementsNodes had any elements, it just happened always
                    if len(candidateElementsNodes) > 0: 
                        minDistance = np.min(np.linalg.norm(intersectionPlate.transpose() - candidateElementsNodes, axis = 1))
                    else: 
                        minDistance = np.min(np.linalg.norm(intersectionPlate.transpose())) 
                # STEP 2.2. All points outside of T-edges or free edges are located
                else: 
                    # Since only the plane where the bolt is is considered, T-edges are also considered free edges
                    faceElements = model.get_elements_by_face(boltElement, domain = seenCandidates)
                    freeEdges = model.get_free_edges(domain = faceElements)
                    for i in boxPoints.keys(): 
                        # Of course, points that have been found are skipped
                        if not boxPointsFound.get(i): 
                            A = np.array([[j[1].X, j[1].Y, j[1].Z] for j in freeEdges])
                            B = np.array([[j[2].X, j[2].Y, j[2].Z] for j in freeEdges])
                            segmentVector = B - A 
                            pointVector = boxPoints.get(i) - A 
                            projection = np.sum(pointVector * segmentVector, axis = 1) / np.sum(segmentVector * segmentVector, axis = 1)
                            projectedPoint = []
                            for j in range(A.shape[0]): 
                                if projection[j] < np.linalg.norm(segmentVector)*projTol: 
                                    projectedPoint.append(A[j])
                                elif projection[j] > 1 - np.linalg.norm(segmentVector)*projTol: 
                                    projectedPoint.append(B[j])
                                else: 
                                    projectedPoint.append(A[j] + projection[j]*segmentVector[j])
                            distanceToProjectedPoint = [np.linalg.norm(boxPoints.get(i) - j) for j in projectedPoint]
                            # Of course, only the minimum distance will be saved
                            index = distanceToProjectedPoint.index(np.nanmin(distanceToProjectedPoint))
                            boxPointsElements[i] = freeEdges[index][0]
                            boxPoints[i] = projectedPoint[index]
                            boxPointsFound[i] = True 
            
            # If there are not enough adjacent elements (2 or less), an error is displayed and all dictionaries are 
            # filled with zeros. 
            if noAdjacents: 
                N2PLog.Warning.W520(p)
                for i in list(results.keys()):

                    p._nx_bypass[i] = 0
                    p._nx_total[i] = 0
                    p._ny_bypass[i] = 0
                    p._ny_total[i] = 0
                    p._nxy_bypass[i] = 0
                    p._nxy_total[i] = 0
                    p._mx_total[i] = 0
                    p._my_total[i] = 0
                    p._mxy_total[i] = 0
                    p._bypass_max[i] = 0
                    p._bypass_min[i] = 0
                    p._box_fluxes[i] = {1: np.zeros(6).tolist(), 2: np.zeros(6).tolist(), 3: np.zeros(6).tolist(), 4: np.zeros(6).tolist(),
                                     5: np.zeros(6).tolist(), 6: np.zeros(6).tolist(), 7: np.zeros(6).tolist(), 8: np.zeros(6).tolist()}
                    
                p._box_points = {1: np.zeros(3), 2: np.zeros(3), 3: np.zeros(3), 4: np.zeros(3),
                                 5: np.zeros(3), 6: np.zeros(3), 7: np.zeros(3), 8: np.zeros(3)}
                continue 
            
            # All box points are placed and their container elements are identified
            p._box_points = boxPoints
            if cornerData: 
                resultDict = {}
                elementNodal = model.elementnodal()
                boxPointForces = {i: None for i in boxPoints.keys()}
                # Forces and moments are obtained in each box points
                for i in boxPoints.keys(): 
                    pointElement = boxPointsElements.get(i) 
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
                        cornerCoordElem, pointCoordElem = transformation_for_interpolation(cornerCoordsGlobal, centroid, boxPoints.get(i), elementSystemBoxPoint)
                        interpolatedForces = interpolation(pointCoordElem, cornerCoordElem, l)
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
                boxPointForces = {i: None for i in boxPoints.keys()}
                for i in boxPoints.keys(): 
                    pointElement = boxPointsElements.get(i) 
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
                        cornerCoordElem, pointCoordElem = transformation_for_interpolation(cornerCoordsGlobal, centroid, boxPoints.get(i), elementSystemBoxPoint)
                        interpolatedForces = interpolation(pointCoordElem, cornerCoordElem, elementForces)
                        interpolatedForcesRot = rotate_tensor2D(elementSystemBoxPoint, boltElement.MaterialSystemArray, elementSystemBoxPoint[6:9], interpolatedForces)
                        resultForPoint[j] = interpolatedForcesRot 
                    boxPointForces[i] = resultForPoint
                for i, j in boxPointForces.items(): 
                    for k, l in j.items(): 
                        if k not in resultDict: 
                            resultDict[k] = {} 
                        resultDict[k][i] = l 
            p._box_fluxes = resultDict

            # STEP 3. Bypass and total forces and moments are obtained 
            for i, j in resultDict.items(): 
                # Fluxes are obtained 
                side = {1: [1, 2, 3], 2: [3, 4, 5], 3: [5, 6, 7], 4: [7, 8, 1]}

                # X fluxes 
                nx2 = np.array([j.get(k)[0] for k in side[2]]).mean()
                nx4 = np.array([j.get(k)[0] for k in side[4]]).mean() 
                nxBypass = min((nx2, nx4), key = abs) 
                nxTotal = max((nx2, nx4), key = abs) 
                mx2 = np.array([j.get(k)[3] for k in side[2]]).mean()
                mx4 = np.array([j.get(k)[3] for k in side[4]]).mean() 
                mxTotal = -0.5*(mx2 + mx4) 

                # Y fluxes 
                ny1 = np.array([j.get(k)[1] for k in side[1]]).mean()
                ny3 = np.array([j.get(k)[1] for k in side[3]]).mean() 
                nyBypass = min((ny1, ny3), key = abs) 
                nyTotal = max((ny1, ny3), key = abs)
                my1 = np.array([j.get(k)[4] for k in side[1]]).mean() 
                my3 = np.array([j.get(k)[4] for k in side[3]]).mean()
                myTotal = -0.5*(my1 + my3) 

                # XY fluxes 
                nxy1 = np.array([j.get(k)[2] for k in side[1]]).mean()
                nxy2 = np.array([j.get(k)[2] for k in side[2]]).mean()
                nxy3 = np.array([j.get(k)[2] for k in side[3]]).mean()
                nxy4 = np.array([j.get(k)[2] for k in side[4]]).mean()
                nxyBypass = min((nxy1, nxy2, nxy3, nxy4), key = abs) 
                nxyTotal = max((nxy1, nxy2, nxy3, nxy4), key = abs) 
                mxy1 = np.array([j.get(k)[5] for k in side[1]]).mean()
                mxy2 = np.array([j.get(k)[5] for k in side[2]]).mean()
                mxy3 = np.array([j.get(k)[5] for k in side[3]]).mean()
                mxy4 = np.array([j.get(k)[5] for k in side[4]]).mean()
                mxyTotal = -0.25*(mxy1 + mxy2 + mxy3 + mxy4)

                # STEP 4. The bypass tensor is rotated 
                materialSystem = boltElement.MaterialSystemArray 
                tensorToRotate = [nxBypass, nyBypass, nxyBypass, nxTotal, nyTotal, nxyTotal, mxTotal, myTotal, mxyTotal]
                for k in tensorToRotate: 
                    if not isinstance(k, float): 
                        N2PLog.Error.E509(self)
                        return None
                rotatedTensor = rotate_tensor2D(boxSystem, materialSystem, materialSystem[6:9], tensorToRotate)

                p._nx_bypass[i] = rotatedTensor[0]
                p._ny_bypass[i] = rotatedTensor[1]
                p._nxy_bypass[i] = rotatedTensor[2]
                p._nx_total[i] = rotatedTensor[3]
                p._ny_total[i] = rotatedTensor[4]
                p._nxy_total[i] = rotatedTensor[5]
                p._mx_total[i] = rotatedTensor[6]
                p._my_total[i] = rotatedTensor[7]
                p._mxy_total[i] = rotatedTensor[8]

                p._bypass_max[i] = 0.5*(rotatedTensor[0] + rotatedTensor[1]) + (0.5*(rotatedTensor[0] - rotatedTensor[1])**2 + (rotatedTensor[2])**2)**0.5
                p._bypass_min[i] = 0.5*(rotatedTensor[0] + rotatedTensor[1]) - (0.5*(rotatedTensor[0] - rotatedTensor[1])**2 + (rotatedTensor[2])**2)**0.5           
    # ------------------------------------------------------------------------------------------------------------------

    def get_bypass_loads_PAG(self, model: N2PModelContent, results: dict, cornerData: bool = False, materialFactorMetal: float = 4.0, materialFactorComposite: float = 4.5, 
                             areaFactor: float = 2.5, maxIterations: int = 200, projTol: float = 0.01, increaseTol: float = 10): 
    
        """
        Method used to obtain the bypass loads of a joint's plates. Maintaining the defauld parameters is highly 
        recommended, although the user is free to change some of them. 

        Args: 
            model: N2PModelContent 
            results: dict -> results dictionary.
            cornerData: bool = False -> boolean that shows if there is data on the corners of the elements or not. 
            materialFactorMetal: float = 4.0 
            materialFactorComposite: float = 4.5 -> in order to obtain the box with the same dimensions as the one 
            obtained by PAG, this value should be set to 4.0. 
            areaFactor: float = 2.5 
            maxIterations: int = 200 
            projTol: float = 0.01 
            increaseTol: float = 10 -> percentage that the projection tolerance increases if a point has not been 
            found. By default, it is 10%, so the projection tolerance would be multiplied by 1.1. 

        Calling example: 
            >>> myJoint.get_bypass_loads_PAG(loads.Model, loads.Results) 

        Procedure and methodology: 
            - The procedure is based on the crown method, so the fluxes will be calculated using a square-shaped box 
            around the joint in the plate's plane. 
            - Firstly, the box where the calculations are to be made is obtained. Its dimension is 
                    a = 0.4 * areaFactor * materialFactor * Diameter 
            - In order to obtain the box dimension used by PAG, which is a = 4*Diameter, then materialFactor should 
            always be set to 4.0. 
            - Knowing its dimension, the box should be defined with a specific orientation and order. The orientation 
            is defined by the box reference frame, which coincides with the material system of the element where the 
            joint is pierced. This may cause a small variation because the z-axis is defined as the joint's axial 
            direction, and sometimes the material system's z-axis does not coincide with it. 
            - Then, the box system's origin would be placed in the center of the box and the first point would be 
            located in (-a, a) and the other points would be placed in the clockwise direction. 
            - This does not always coincide with what Altair displays, but the final results should be the same. 
            - Adjacent elements will be evaluated until the distance from the joint to them is greater to the box's 
            semidiagonal. After this, no more points will be found further away, so the search stops here. If there are 
            still points to be assigned, it is concluded that they lie outside of the edge of the plate and therefore 
            they will be projected. 
            - If all points lie within the free edges, the process is simple. The adjacent elements to the pierced one 
            are evaluated in case that any point lies inside of it, which is done taking into consideration the 
            so-called box tolerance, stopping the iterations when the element that is being analysed is far from the 
            box location. 
            - However, there are two cases where the box point location is not as simple. Firstly, if there are points 
            outside the free edges, they are orthogonally projected onto the mesh. In the FastPPH tool used by Altair, 
            this projection does not always follow the same procedure but, to simplify, in this tool an orthogonal 
            projection is always used. 
            - The second critical case occurs when a box crosses a T-edge or gets out of a surface that does not finish 
            in a free edge. If the box crosses a T-edge, it is considered that all points are located within the free 
            edges and should not be projected. If the box gets out of the borders of a surface, and these borders are 
            not free edges, they are treated as so, and the same procedure is followed as when they were outside of 
            free edges (they are orthogonally projected). 
            - Now, the fluxes in each of the points of the boxes, for each load case, must be obtained, in order to 
            calculate the final values for bypass and total loads. There are two options to be analyzed: 

                1. cornerData = True 
                
                If the user asks for results in the corner when running the model and obtaining the corresponding 
                results, these results will be given by node and not by element, giving several values for a node, 
                related to the element where it is. This can be achieved by selecting the CORNER or BILIN describer in 
                the FORCE card. Results will be more accurate if corner data is used, as there are more values to be 
                used. 

                Taking each of the box's points, the same procedure is carried out. Firstly, the results for all nodes 
                that form the element where the box point is are retrieved. They are represented in their element 
                reference frame, so they are transformed into the same reference frame. Once 3 or 4 values for the 
                nodes are obtained (depending on wether the element is a TRIA or QUAD), a bilinear interpolation to the 
                box point from the node locations is used. 

                2. cornerData = False

                The results in the result files are retrieved in the centroid of each element, leading to results that 
                will be less precise, since results in the corners must be approximated instead of actually calculated. 
                This approximation is made by averaging the adjacent elements. Besides this, the same procedure is used 
                as in the previous case. 

            - Finally, all results are transformed into the material reference frame corresponding to the element where 
            the joint is pierced. 

            There are several checks during the program that help the user understand if there are any problems in the
            analysis. In any case, an error appears. The checks are the following: 
                1. There are less than two plates connected to the joint. 
                2. A plate does not have the necessary information (intersection, normal, distance and elements). 
                3. The joint has no diameter or it is negative. 
                4. The maximum number of iterations is reached. 
                5. There are no candidate elements to search. This should not actually occur, though, because of a 
                previous check. 
                6. There are not enough adjacent elements in the model. 
                7. Certain arrays do not have, for whatever reason, six elements. 
                8. The final rotation matrix is not well defined. 
        """

        if not self.Diameter or self.Diameter <= 0: 
            N2PLog.Error.E506(self) 
            return None 
        for i in self.PlateList: 
            if len(self.PlateList) < 2: 
                N2PLog.Error.E505(self) 
                return None 
            if not i.Intersection: 
                N2PLog.Warning.W513(self) 
                continue 
            if not i.Normal: 
                N2PLog.Warning.W514(self) 
                continue
            if not i.Distance: 
                N2PLog.Warning.W515(self) 
                continue
            if not i.ElementList or len(i.ElementList) == 0: 
                N2PLog.Warning.W516(self) 
                continue 

            if model.PropertyDict.get(i.ElementList[0].Prop).PropertyType == "PCOMP": 
                materialFactor = materialFactorComposite 
            else: 
                materialFactor = materialFactorMetal 

            supportedElements = ["CQUAD4", "CTRIA3"]
            domain = [i for i in model.get_elements() if i.TypeElement in supportedElements]
            # STEP 1. The box is obtained 
            if not i.BoxDimension: 
                i.get_box_PAG(model, domain, materialFactor, areaFactor, maxIterations, projTol, increaseTol)
            # STEP 2. Bypass loads are calculated in the box 
            i.get_bypass_PAG(model, domain, results, cornerData) 

    # Method used to adequately export forces --------------------------------------------------------------------------
    def export_forces(self, model: N2PModelContent, pathFile: str, analysisName: str, results: dict, 
                     typeExport: Literal["NAXTOPY", "ALTAIR", "PAG_CSV"] = "NAXTOPY"): 

        """
        Method used to export the obtained forces and bypass loads to a CSV file in the path described by the user. 

        Args: 
            model: N2PModelContent
            pathFile: str -> path file. 
            analysisName: str -> file's name.
            results: dict -> results dictionary.
            typeExport: Literal["NAXTOPY", "ALTAIR"] = "NAXTOPY" -> export style. By default, results are exported in 
            the NAXTOPY style. 

        The CSV file has the following information, in this order, for the NAXTOPY style: 
            Bolt ID 
            Plate Global ID 
            Plate Local ID 
            Plate Part ID 
            Plate Element ID -> solver ID of the central N2PElement associated to the N2PPlate.
            Plate Element Property ID -> ID of the N2PProperty associated to the previous N2PElement. 
            Bolt Element 1 ID -> ID of the 1st N2PElement associated to the N2PBolt. 
            Bolt Element 2 ID -> ID of the 2nd N2PElement associated to the N2PBolt (if there is no 2nd element, '0' is 
            displayed instead). 
            Load Case ID
            Analysis Name -> as defined by the user. 
            Box Dimension 
            Box System 
            Intersection -> intersection point between the plate and its bolt 
            FX Altair; FY Altair; FZ Altair 
            FX Connector 1; FY Connector 1; FZ Connector 1; FX Connector 2; FY Connector 2; FZ Connector 2
            FZ max 
            p1; p2; ...; p8 -> nth box point 
            Fxx p1; Fxx p2; ...; Fxx p8 -> FXX flux associated to the nth box point. 
            Fyy p1; ... -> FYY flux associated to the nth box point. 
            Fxy p1; ... -> FXY flux associated to the nth box point. 
            Mxx p1; ... -> MXX flux associated to the nth box point. 
            Myy p1; ... -> MYY flux associated to the nth box point. 
            Mxy p1; ... -> MXY flux associated to the nth box point. 
            Nx bypass; Nx total; Ny bypass; Ny total; Nxy bypass; Nxy total; Mx total; My total; Mxy total 

        It has the following information, in this order, for the ALTAIR style: 
            DDP -> joint ID.
            elementid -> ID of the central N2PElement associated to the N2PPlate.
            Component Name 
            elem 1 id -> ID of the first connector.
            elem 1 node id -> ID of the first node of the first connector. 
            elem 2 id -> ID of the second connector.
            elem 2 node id -> ID of the first node of the second connector.
            box dimension
            loadcase -> loadcase ID. 
            file name -> analysis name.
            LoadCase Name 
            Time Step Name -> 'N/A'
            pierced location -> intersection point.
            FX, FY, FZ 
            MaxFz 
            p1; p2; ...; p8 -> nth box point 
            Fxx p1; Fxx p2; ...; Fxx p8 -> FXX flux associated to the nth box point. 
            Fyy p1; ... -> FYY flux associated to the nth box point. 
            Fxy p1; ... -> FXY flux associated to the nth box point. 
            Mxx p1; ... -> MXX flux associated to the nth box point. 
            Myy p1; ... -> MYY flux associated to the nth box point. 
            Mxy p1; ... -> MXY flux associated to the nth box point. 
            Nx bypass; Nx total; Ny bypass; Ny total; Nxy bypass; Nxy total; Mx total; My total; Mxy total 


        There is one row for each loadcase and each distinct N2PPlate, so there are a total of 
                    Numer of Loadcases * Number of different N2PPlates       
        total rows, without taking into consideration the header.

        Calling example: 
            >>> myJoint.export_forces(pathFile, "test", fasteners.Results, "ALTAIR")
        """

        newPathFile = "{}\\{}_fastpph.csv".format(pathFile, analysisName)
        if typeExport == "PAG_CSV": 
            headline = ["PLATE ELEMENT ID", "LOAD CASE ID", "PROPERTY", "CFAST A ID", "CFAST B ID", "DIRECTION", 
                        "GA NODE CFAST A", "GB NODE CFAST A", "GA NODE CFAST B", "GB NODE CFAST B", "DIAMETER", "EXT. ZONE", 
                        "ELEMENT 1 ID", "ELEMENT 2 ID", "ELEMENT 3 ID", "ELEMENT 4 ID", "ELEMENT 5 ID", "ELEMENT 6 ID", "ELEMENT 7 ID", "ELEMENT 8 ID", 
                        "POINT 1 (X,Y,Z)", "POINT 2 (X,Y,Z)", "POINT 3 (X,Y,Z)", "POINT 4 (X,Y,Z)", 
                        "POINT 5 (X,Y,Z)", "POINT 6 (X,Y,Z)", "POINT 7 (X,Y,Z)", "POINT 8 (X,Y,Z)", 
                        "X BEARING FORCE", "Y BEARING FORCE", "PULLTHROUGH FORCE", "BOLT SHEAR", "BOLT TENSION", 
                        "NXX BYPASS", "NYY BYPASS", "NXY BYPASS", "MXX BYPASS", "MYY BYPASS", "MXY BYPASS", 
                        "FXX CFAST A", "FYY CFAST A", "FZZ CFAST A", "FXX CFAST B", "FYY CFAST B", "FZZ CFAST B", "FACTOR CFAST A", "FACTOR CFAST B", 
                        "FXX POINT 1", "FYY POINT 1", "FXY POINT 1", "MXX POINT 1", "MYY POINT 1", "MXY POINT 1", 
                        "FXX POINT 2", "FYY POINT 2", "FXY POINT 2", "MXX POINT 2", "MYY POINT 2", "MXY POINT 2", 
                        "FXX POINT 3", "FYY POINT 3", "FXY POINT 3", "MXX POINT 3", "MYY POINT 3", "MXY POINT 3", 
                        "FXX POINT 4", "FYY POINT 4", "FXY POINT 4", "MXX POINT 4", "MYY POINT 4", "MXY POINT 4", 
                        "FXX POINT 5", "FYY POINT 5", "FXY POINT 5", "MXX POINT 5", "MYY POINT 5", "MXY POINT 5", 
                        "FXX POINT 6", "FYY POINT 6", "FXY POINT 6", "MXX POINT 6", "MYY POINT 6", "MXY POINT 6", 
                        "FXX POINT 7", "FYY POINT 7", "FXY POINT 7", "MXX POINT 7", "MYY POINT 7", "MXY POINT 7", 
                        "FXX POINT 8", "FYY POINT 8", "FXY POINT 8", "MXX POINT 8", "MYY POINT 8", "MXY POINT 8", 
                        "FXX NORTH", "FYY NORTH", "FXY NORTH", "MXX NORTH", "MYY NORTH", "MXY NORTH", 
                        "FXX SOUTH", "FYY SOUTH", "FXY SOUTH", "MXX SOUTH", "MYY SOUTH", "MXY SOUTH", 
                        "FXX EAST", "FYY EAST", "FXY EAST", "MXX EAST", "MYY EAST", "MXY EAST", 
                        "FXX WEST", "FYY WEST", "FXY WEST", "MXX WEST", "MYY WEST", "MXY WEST"]
            propDict = model.PropertyDict 
            with open(newPathFile, "a+", newline = "") as i: 
                writerCSV = csv.writer(i) 
                if i.tell() == 0: 
                    writerCSV.writerow(headline) 
                for p in self.PlateList: 
                    plateElem = p.ElementList[0]
                    prop = propDict[plateElem.Prop].PropertyType + "." + str(plateElem.Prop)
                    boltElementList = p.BoltElementList
                    if boltElementList["A"]: 
                        cfastA_id = str(boltElementList["A"].ID)
                        directionA = p.BoltDirection["A"]
                        cfastA_nodeA = str(boltElementList["A"].Nodes[0].ID)
                        cfastA_nodeB = str(boltElementList["A"].Nodes[1].ID)
                    else: 
                        cfastA_id = "0"
                        directionA = ""
                        cfastA_nodeA = "0"
                        cfastA_nodeB = "0"
                    if boltElementList["B"]: 
                        cfastB_id = str(boltElementList["B"].ID)
                        directionB = p.BoltDirection["B"]
                        cfastB_nodeA = str(boltElementList["B"].Nodes[0].ID)
                        cfastB_nodeB = str(boltElementList["B"].Nodes[1].ID)
                    else: 
                        cfastB_id = "0"
                        directionB = ""
                        cfastB_nodeA = "0"
                        cfastB_nodeB = "0"
                    extZone = "SQUARE"
                    boltElementsPlate = [l.ID for l in p.BoltElementList.values() if l]
                    for j, k in results.items(): 
                        data = [str(plateElem.ID), str(j), prop, cfastA_id, cfastB_id, directionA + "|" + directionB, 
                                cfastA_nodeA, cfastA_nodeB, cfastB_nodeA, cfastB_nodeB, str(self.Diameter), extZone]
                        data = data + [str(element.ID) for element in p.BoxElements.values()]
                        boxPoints = list(p.BoxPoints.values())
                        for l in range(len(boxPoints)): 
                            points = [] 
                            for m in boxPoints[l]: 
                                points.append("{:.4f}".format(m))
                            data.append(points) 
                        tf = p.TranslationalFastenerForces[j]
                        bf = {}
                        for l,m in p.BoxFluxes[j].items(): 
                            bf[l] = [] 
                            for n in m: 
                                bf[l].append("{:.4f}".format(n))
                        bs = p.BypassSides[j]
                        data2 = ["{:.4f}".format(p.BearingForce.get(j)[0]), "{:.4f}".format(p.BearingForce.get(j)[1]), "{:.4f}".format(p.BearingForce.get(j)[2]), 
                                "{:.4f}".format(max([self.Bolt.ShearForce[j][l] for l in boltElementsPlate])), 
                                "{:.4f}".format(max([self.Bolt.AxialForce[j][l] for l in boltElementsPlate])), 
                                "{:.4f}".format(p.NxBypass[j]), "{:.4f}".format(p.NyBypass[j]), "{:.4f}".format(p.NxyBypass[j]), 
                                "{:.4f}".format(p.MxTotal[j]), "{:.4f}".format(p.MyTotal[j]), "{:.4f}".format(p.MxyTotal[j]), 
                                "{:.4f}".format(tf[0][0]), "{:.4f}".format(tf[0][1]), "{:.4f}".format(tf[0][2]), 
                                "{:.4f}".format(tf[1][0]), "{:.4f}".format(tf[1][1]), "{:.4f}".format(tf[1][2]), 
                                str(p.CFASTFactor["A"]), str(p.CFASTFactor["B"]), 
                                bf[1][0], bf[1][1], bf[1][2], bf[1][3], bf[1][4], bf[1][5], 
                                bf[2][0], bf[2][1], bf[2][2], bf[2][3], bf[2][4], bf[2][5], 
                                bf[3][0], bf[3][1], bf[3][2], bf[3][3], bf[3][4], bf[3][5], 
                                bf[4][0], bf[4][1], bf[4][2], bf[4][3], bf[4][4], bf[4][5], 
                                bf[5][0], bf[5][1], bf[5][2], bf[5][3], bf[5][4], bf[5][5], 
                                bf[6][0], bf[6][1], bf[6][2], bf[6][3], bf[6][4], bf[6][5], 
                                bf[7][0], bf[7][1], bf[7][2], bf[7][3], bf[7][4], bf[7][5], 
                                bf[8][0], bf[8][1], bf[8][2], bf[8][3], bf[8][4], bf[8][5], 
                                "{:.4f}".format(bs[0][0]), "{:.4f}".format(bs[1][0]), "{:.4f}".format(bs[2][0]), 
                                "{:.4f}".format(bs[3][0]), "{:.4f}".format(bs[4][0]), "{:.4f}".format(bs[5][0]), 
                                "{:.4f}".format(bs[0][1]), "{:.4f}".format(bs[1][1]), "{:.4f}".format(bs[2][1]), 
                                "{:.4f}".format(bs[3][1]), "{:.4f}".format(bs[4][1]), "{:.4f}".format(bs[5][1]), 
                                "{:.4f}".format(bs[0][2]), "{:.4f}".format(bs[1][2]), "{:.4f}".format(bs[2][2]), 
                                "{:.4f}".format(bs[3][2]), "{:.4f}".format(bs[4][2]), "{:.4f}".format(bs[5][2]), 
                                "{:.4f}".format(bs[0][3]), "{:.4f}".format(bs[1][3]), "{:.4f}".format(bs[2][3]), 
                                "{:.4f}".format(bs[3][3]), "{:.4f}".format(bs[4][3]), "{:.4f}".format(bs[5][3])]
                        data = data + data2 
                        writerCSV.writerow(data)
        else: 
            jointElements = self.BoltElementList
            connectors = []
            if len(jointElements) == 1: 
                connectors = [[jointElements[0].ID, 0], [jointElements[0].ID, 0]]
            else:
                connectors.append([jointElements[0].ID, 0])
                for i in range(1, len(jointElements)): 
                    connectors.append([jointElements[i - 1].ID, jointElements[i].ID])
                connectors.append([jointElements[-1].ID, 0])
            jointElementsDict = {}
            for i, j in enumerate(self.PlateList):
                jointElementsDict[j] = connectors[i]

            if typeExport == "ALTAIR":
                jointNodes = self.BoltNodeList 
                connectors2 = [] 
                connectors2.append([jointNodes[0][0].ID, 0])
                for i in range(1, len(jointNodes)): 
                    connectors2.append([jointNodes[i - 1][1].ID, jointNodes[i][0].ID])
                connectors2.append([jointNodes[-1][0].ID, 0])
                jointNodesDict = {}
                for i,j in enumerate(self.PlateList): 
                    jointNodesDict[j] = connectors2[i]

            loadCaseID = list(results.keys())
            lc = model.LoadCases
            lcDict = {} 
            for i in lc: 
                for j in loadCaseID: 
                    if j == i.ID: 
                        lcDict[j] = i

            propDict = model.PropertyDict

            # The header is created 
            if typeExport == "NAXTOPY": 
                headline = ["Bolt ID", "Plate Global ID", "Plate Local ID", "Plate Part ID", "Plate Element ID", "Plate Element Property ID", 
                            "Bolt Element 1 ID", "Bolt Element 2 ID", "Load Case ID", "Analysis Name", "Box Dimension", 
                            "Box System", "Intersection", "FX Altair", "FY Altair", "FZ Altair", 
                            "FX Connector 1", "FY Connector 1", "FZ Connector 1", 
                            "FX Connector 2", "FY Connector 2", "FZ Connector 2", "FZ max", 
                            "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", 
                            "Fxx p1", "Fxx p2", "Fxx p3", "Fxx p4", "Fxx p5", "Fxx p6", "Fxx p7", "Fxx p8", 
                            "Fyy p1", "Fyy p2", "Fyy p3", "Fyy p4", "Fyy p5", "Fyy p6", "Fyy p7", "Fyy p8", 
                            "Fxy p1", "Fxy p2", "Fxy p3", "Fxy p4", "Fxy p5", "Fxy p6", "Fxy p7", "Fxy p8", 
                            "Mxx p1", "Mxx p2", "Mxx p3", "Mxx p4", "Mxx p5", "Mxx p6", "Mxx p7", "Mxx p8", 
                            "Myy p1", "Myy p2", "Myy p3", "Myy p4", "Myy p5", "Myy p6", "Myy p7", "Myy p8", 
                            "Mxy p1", "Mxy p2", "Mxy p3", "Mxy p4", "Mxy p5", "Mxy p6", "Mxy p7", "Mxy p8", 
                            "Nx bypass", "Nx total", "Ny bypass", "Ny total", "Nxy bypass", "Nxy total",
                            "Mx total", "My total", "Mxy total"] 
            elif typeExport == "ALTAIR": 
                headline = ["DDP", "elementid", "Component Name", "elem 1 id", "elem 1 Node id", "elem 2 id", "elem 2 Node id", 
                            "box dimension", "loadcase", "file Name", "LoadCase Name", "Time Step Name", "pierced location",
                            "Fx", "Fy", "Fz", "MaxFz", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", 
                            "Fxx p1", "Fxx p2", "Fxx p3", "Fxx p4", "Fxx p5", "Fxx p6", "Fxx p7", "Fxx p8", 
                            "Fyy p1", "Fyy p2", "Fyy p3", "Fyy p4", "Fyy p5", "Fyy p6", "Fyy p7", "Fyy p8", 
                            "Fxy p1", "Fxy p2", "Fxy p3", "Fxy p4", "Fxy p5", "Fxy p6", "Fxy p7", "Fxy p8", 
                            "Mxx p1", "Mxx p2", "Mxx p3", "Mxx p4", "Mxx p5", "Mxx p6", "Mxx p7", "Mxx p8", 
                            "Myy p1", "Myy p2", "Myy p3", "Myy p4", "Myy p5", "Myy p6", "Myy p7", "Myy p8", 
                            "Mxy p1", "Mxy p2", "Mxy p3", "Mxy p4", "Mxy p5", "Mxy p6", "Mxy p7", "Mxy p8", 
                            "Nx bypass", "Nx total", "Ny bypass", "Ny total", "Nxy bypass", "Nxy total",
                            "Mx total", "My total", "Mxy total"]
            else: 
                N2PLog.Error.E526(typeExport)
            with open(newPathFile, "a+", newline = "") as i: 
                writerCSV = csv.writer(i) 
                if i.tell() == 0: 
                    writerCSV.writerow(headline) 
                for p in self.PlateList: 
                    for j, k in results.items(): 
                        if typeExport == "NAXTOPY": 
                            data = [p.Bolt.ID, p.GlobalID[0], p.ID, p.Joint.PartID, p.PlateCentralCellSolverID, p.ElementList[0].Prop, 
                                    jointElementsDict[p][0], jointElementsDict[p][1], j, analysisName, p.BoxDimension, 
                                    p.BoxSystem, p.Intersection, p.BearingForce[j][0], p.BearingForce[j][1], p.BearingForce[j][2],
                                    p.TranslationalFastenerForces[j][0][0], p.TranslationalFastenerForces[j][0][1], p.TranslationalFastenerForces[j][0][2], 
                                    p.TranslationalFastenerForces[j][1][0], p.TranslationalFastenerForces[j][1][1], p.TranslationalFastenerForces[j][1][2], self.Bolt.MaxAxialForce[j], 
                                    p.BoxPoints[1].tolist(), p.BoxPoints[2].tolist(), p.BoxPoints[3].tolist(), p.BoxPoints[4].tolist(), 
                                    p.BoxPoints[5].tolist(), p.BoxPoints[6].tolist(), p.BoxPoints[7].tolist(), p.BoxPoints[8].tolist(), 
                                    p.BoxFluxes[j][1][0], p.BoxFluxes[j][2][0], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][0], 
                                    p.BoxFluxes[j][5][0], p.BoxFluxes[j][6][0], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][0], 
                                    p.BoxFluxes[j][1][1], p.BoxFluxes[j][2][1], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][1], 
                                    p.BoxFluxes[j][5][1], p.BoxFluxes[j][6][1], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][1], 
                                    p.BoxFluxes[j][1][2], p.BoxFluxes[j][2][2], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][2], 
                                    p.BoxFluxes[j][5][2], p.BoxFluxes[j][6][2], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][2], 
                                    p.BoxFluxes[j][1][3], p.BoxFluxes[j][2][3], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][3], 
                                    p.BoxFluxes[j][5][3], p.BoxFluxes[j][6][3], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][3], 
                                    p.BoxFluxes[j][1][4], p.BoxFluxes[j][2][4], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][4], 
                                    p.BoxFluxes[j][5][4], p.BoxFluxes[j][6][4], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][4], 
                                    p.BoxFluxes[j][1][5], p.BoxFluxes[j][2][5], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][5], 
                                    p.BoxFluxes[j][5][5], p.BoxFluxes[j][6][5], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][5], 
                                    p.NxBypass[j], p.NxTotal[j], p.NyBypass[j], p.NyTotal[j], p.NxyBypass[j], p.NxyTotal[j], 
                                    p.MxTotal[j], p.MyTotal[j], p.MxyTotal[j]] 
                        else: 
                            data = [p.Bolt.ID, p.PlateCentralCellSolverID, propDict[p.ElementList[0].Prop] + '_' + str(p.Elements[0].Prop), 
                                    jointElementsDict[p][0], jointNodesDict[p][0], jointElementsDict[p][1], jointNodesDict[p][1],
                                    p.BoxDimension, j, analysisName, lcDict[j].Name, 'N/A', p.Intersection, 
                                    p.BearingForce[j][0], p.BearingForce[j][1], p.BearingForce[j][2], self.Bolt.MaxAxialForce[j], 
                                    p.BoxPoints[1].tolist(), p.BoxPoints[2].tolist(), p.BoxPoints[3].tolist(), p.BoxPoints[4].tolist(), 
                                    p.BoxPoints[5].tolist(), p.BoxPoints[6].tolist(), p.BoxPoints[7].tolist(), p.BoxPoints[8].tolist(), 
                                    p.BoxFluxes[j][1][0], p.BoxFluxes[j][2][0], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][0], 
                                    p.BoxFluxes[j][5][0], p.BoxFluxes[j][6][0], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][0], 
                                    p.BoxFluxes[j][1][1], p.BoxFluxes[j][2][1], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][1], 
                                    p.BoxFluxes[j][5][1], p.BoxFluxes[j][6][1], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][1], 
                                    p.BoxFluxes[j][1][2], p.BoxFluxes[j][2][2], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][2], 
                                    p.BoxFluxes[j][5][2], p.BoxFluxes[j][6][2], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][2], 
                                    p.BoxFluxes[j][1][3], p.BoxFluxes[j][2][3], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][3], 
                                    p.BoxFluxes[j][5][3], p.BoxFluxes[j][6][3], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][3], 
                                    p.BoxFluxes[j][1][4], p.BoxFluxes[j][2][4], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][4], 
                                    p.BoxFluxes[j][5][4], p.BoxFluxes[j][6][4], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][4], 
                                    p.BoxFluxes[j][1][5], p.BoxFluxes[j][2][5], p.BoxFluxes[j][3][0], p.BoxFluxes[j][4][5], 
                                    p.BoxFluxes[j][5][5], p.BoxFluxes[j][6][5], p.BoxFluxes[j][7][0], p.BoxFluxes[j][8][5], 
                                    p.NxBypass[j], p.NxTotal[j], p.NyBypass[j], p.NyTotal[j], p.NxyBypass[j], p.NxyTotal[j], 
                                    p.MxTotal[j], p.MyTotal[j], p.MxyTotal[j]] 
                        dataNew = []
                        # The data list is slightly altered, so that nothing is shown as a numpy array or numpy float. 
                        for l in data: 
                            if type(l) == float: 
                                dataNew.append(str(l))
                            elif type(l) == list or type(l) == tuple: 
                                for m in range(len(l)): 
                                    if type(l[m]) == float: 
                                        l[m] = str(l[m])
                                dataNew.append(l) 
                            elif type(l) == str or type(l) == int: 
                                dataNew.append(l)
                            else: 
                                dataNew.append(str(float(l)))
                        writerCSV.writerow(dataNew)
    # ------------------------------------------------------------------------------------------------------------------