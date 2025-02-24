from __future__ import annotations
from NaxToPy.Core.Classes.N2PNastranInputData import * 
from NaxToPy.Core.Classes.N2PAbaqusInputData import * 
from NaxToPy.Core.Classes.N2PElement import N2PElement 
from NaxToPy.Core.Classes.N2PNode import N2PNode 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from NaxToPy.Modules.Fasteners.Joints.N2PJoint import N2PJoint
class N2PBolt: 

    """
    Class that represents a single bolt. 

    Attributes: 
        id: int -> bolt's internal identificator. 
        one_dim_elems_id_list: list[int] -> list of the internal IDs of N2PElements that make up the bolt. 
        cards: list[N2PCard] -> list of the cards of the N2PElements that make up the bolt. It could contain nulls/
        nones, like when dealing with .op2 files. 
        type: str -> type of bolt. 
        joint: N2PJoint -> N2PJoint associated to the N2PBolt. 
        element_list: list[N2PElement] -> list of all N2PElements associated to the N2PBolt. 
        element_local_system_force: dict[int, dict[int, list[float]]] -> dictionary in the form {Load Case ID: Bolt 
        Element ID: [FX, FY, FZ]} of the joint in the local coordinate system. 
        axial_force: dict[int, dict[int, float]] -> dictionary in the form {Load Case ID: Bolt Element ID: F} of the 
        joint's axial force. 
        shear_force: dict[int, dict[int, float]] -> dictionary in the form {Load Case ID: Bolt Element ID: F} of the 
        joint's shear force. 
        max_axial_force: dict[int, dict[int, float]] -> dictionary in the form {Load Case ID: F} of the joint's maximum 
        axial force. 
        load_angle: dict[int, dict[int, float]] -> dictionary in the form {Load Case ID: Bolt Element ID: Angle} of the 
        joint's load angle in degrees. 
    """

    __slots__ = ("__info__", 
                 "__input_data_father__", 
                 "_id", 
                 "_one_dim_elems_id_list", 
                 "_cards", 
                 "_type", 
                 "_joint", 
                 "_element_list", 
                 "_element_local_system_force", 
                 "_axial_force", 
                 "_shear_force", 
                 "_max_axial_force", 
                 "_load_angle")

    # N2PBolt constructor ----------------------------------------------------------------------------------------------
    def __init__(self, info, input_data_father): 
        self.__info__ = info 
        self.__input_data_father__ = input_data_father 

        self._id: int = int(self.__info__.ID)
        self._one_dim_elems_id_list: list[int] = list(self.__info__.OneDimElemsIdList)
        self._cards: list[N2PCard] = [self.__input_data_father__._N2PNastranInputData__dictcardscston2p[i] for i in self.__info__.Cards if self.__info__.Cards[0] is not None]
        self._type: str = self.__info__.Type.ToString() 

        self._joint: N2PJoint = None
        self._element_list: list[N2PElement] = None 

        self._element_local_system_force: dict[int, dict[int, list[float]]] = {} 
        self._axial_force: dict[int, dict[int, float]] = {}
        self._shear_force: dict[int, dict[int, float]] = {} 
        self._max_axial_force: dict[int, float] = {} 
        self._load_angle: dict[int, dict[int, float]] = {} 
    # ------------------------------------------------------------------------------------------------------------------
        
    # Getters ----------------------------------------------------------------------------------------------------------
    @property 
    def ID(self) -> int: 

        """
        Property that returns the id attribute, that is, the bolt's internal identificator. 
        """

        return self._id 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def OneDimElemsIDList(self) -> list[int]: 

        """
        Property that returns the one_dim_elems_id_list attribute, that is, the list of the internal IDs of all 
        N2PElements that make up the N2PBolt. 
        """

        return self._one_dim_elems_id_list
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def Cards(self) -> list[N2PCard]: 

        """
        Property that returns the cards attribute, that is, the list of N2PCards associated to the N2PElements that 
        make up the bolt.
        """

        return self._cards
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Type(self) -> str: 

        """
        Property that returns the type attribute, that is, what type of elements make up the bolt.
        """

        return self._type 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Joint(self) -> N2PJoint: 

        """
        Property that returns the joint attribute, that is, the N2PJoint associated to the bolt. 
        """

        return self._joint
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def ElementList(self) -> list[N2PElement]: 

        """
        Property that returns the element_list attribute, that is, the list of all N2PElements that compose the bolt. 
        """

        return self._element_list 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def ElementIDList(self) -> list[int]: 

        """
        Property that returns the list of the solver IDs of all N2PElements that compose the bolt. 
        """

        return [j.ID for j in self.ElementList]
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def ElementInternalIDList(self) -> list[int]: 

        """
        Property that returns the list of the internal IDs of all N2PElements that compose the bolt. 
        """

        return [j.InternalID for j in self.ElementList]
    # ------------------------------------------------------------------------------------------------------------------
    
    @property
    def NodeList(self) -> list[N2PNode]: 

        """
        Property that returns the list of all N2PNodes that compose the bolt. 
        """

        return [j.Nodes for j in self.ElementList]
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def PartID(self) -> str: 

        """
        Property that returns the part ID of the bolt. 
        """

        return self.ElementList[0].PartID
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def ElementLocalSystemForce(self) -> dict[int, list[float]]: 

        """
        Property that returns the element_local_system_force attribute, that is, the bolt's 1D forces in the local 
        reference frame. 
        """

        return self._element_local_system_force
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def AxialForce(self) -> dict[int, float]: 

        """
        Property that returns the axial_force attribute, that is, the bolt's shear force.
        """
        
        return self._axial_force
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def ShearForce(self) -> dict[int, float]: 

        """
        Property that returns the shear_force attribute, that is, the bolt's shear force.
        """
        
        return self._shear_force
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def MaxAxialForce(self) -> dict[int, float]: 

        """
        Property that returns the max_axial_force attribute, that is, the maximum axial force sustained by the bolt. 
        """

        return self._max_axial_force
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def LoadAngle(self) -> dict[int, float]: 

        """
        Property that returns the load_angle attribute, that is, the bolt's load angle in degrees. 
        """

        return self._load_angle
    # ------------------------------------------------------------------------------------------------------------------