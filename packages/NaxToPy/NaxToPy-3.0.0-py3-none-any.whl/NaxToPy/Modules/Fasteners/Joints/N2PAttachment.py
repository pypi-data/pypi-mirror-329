from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from NaxToPy.Modules.Fasteners.Joints.N2PPlate import N2PPlate 
    from NaxToPy.Modules.Fasteners.Joints.N2PJoint import N2PJoint
import numpy as np 

class N2PAttachment: 

    """
    Class that represents an attachment, which is a series of N2PJoints that join the same N2PPlates.

    Attributes: 
        id: int 
        attached_plates_id_list: list[int] -> list of the attached N2PPlates' ID.
        attached_plates_list: list[N2PPlate] -> list of the attached N2PPlates. 
        joints_list: list[N2PJoint] -> list of the attached N2PJoints. 
        pitch: float -> minimum distance from an N2PJoint to its neighbours. 
    """

    __slots__ = ("_id", 
                 "_attached_plates_id_list", 
                 "_attached_plates_list", 
                 "_joints_list", 
                 "_pitch")

    # N2PAttachment constructor ----------------------------------------------------------------------------------------
    def __init__(self, id): 
        self._id: int = id 
        self._attached_plates_id_list: list[int] = None 
        self._attached_plates_list: list[N2PPlate] = None 
        self._joints_list: list[N2PJoint] = [] 
        self._pitch: float = None 
    # ------------------------------------------------------------------------------------------------------------------
        
    # Getters ----------------------------------------------------------------------------------------------------------
    @property 
    def ID(self) -> int: 
        
        """
        Property that returns the id attribute, that is, the N2PAttachment's ID. 
        """
        
        return self._id 
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def AttachedPlatesIDList(self) -> list[int]: 

        """
        Property that returns the attached_plates_id_list attribute, that is, the list of the IDs of all attached N2PPlates.
        """

        return self._attached_plates_id_list
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def AttachedPlateList(self) -> list[N2PPlate]: 

        """
        Property that returns the attached_plates_list attribute, that is, the list of all attached N2PPlates. 
        """

        return self._attached_plates_list
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def JointsList(self) -> list[N2PJoint]: 

        """
        Property that returns the joints attribute, that is, the list of all N2PJoints. 
        """

        return self._joints_list
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Pitch(self) -> float: 

        """
        Property that returns the pitch attribute, that is, the attachment's pitch. 
        """

        return self._pitch
    # ------------------------------------------------------------------------------------------------------------------
    

    # Method used to obtain the attachment's pitch ---------------------------------------------------------------------
    def get_pitch(self): 

        """
        Method used to obtain the attachment's pitch, that is, the minimum distance from an N2PJoint to its neighbours. 

        Calling example: 
            >>> jointPitch = myAttachment.get_pitch()
        """

        intersectionPoints = [] 
        plateID = self.JointsList[0].PlateList[0].AttachmentID
        for i in self._joints_list: 
            plate = [p for p in i.PlateList if p.AttachmentID == plateID][0]
            intersectionPoints.append(np.array(plate.Intersection))

        numPoints = len(intersectionPoints)
        distances = np.zeros((numPoints, numPoints))

        for i in range(numPoints): 
            for j in range(i + 1, numPoints): 
                distance = np.linalg.norm(intersectionPoints[i] - intersectionPoints[j])
                distances[i, j] = distances[j, i] = distance 

        np.fill_diagonal(distances, np.inf) 

        distances = np.min(distances, axis = 0) 
        for i, j in enumerate(self._joints_list): 
            j._pitch = float(distances[i])
        self._pitch = float(np.min(distances))
    # -------------------------------------------------------------------------------------------------------------------