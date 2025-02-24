from NaxToPy import N2PLog
from NaxToPy.Core.N2PModelContent import N2PModelContent 
from NaxToPy.Core.Classes.N2PElement import N2PElement
from NaxToPy.Modules.Fasteners.Joints.N2PBolt import N2PBolt 
from NaxToPy.Modules.Fasteners.Joints.N2PPlate import N2PPlate 
from NaxToPy.Modules.Fasteners.Joints.N2PJoint import N2PJoint
from NaxToPy.Modules.Fasteners.Joints.N2PAttachment import N2PAttachment
from NaxToPy.Modules.Fasteners._N2PFastenerAnalysis.Core.Functions.N2PGetAttachments import get_attachments
from time import time 
from typing import Union 

class N2PGetFasteners: 

    """
    Class used to obtain all necessary geometrical information of a model's N2PJoints, N2PBolts and N2PPlates. 

    The instance of this class must be prepared using its properties before calling it method calculate.
    """

    __slots__ = ("_model", 
                 "_get_attachments_bool", 
                 "_thresh", 
                 "_element_list", 
                 "_joints_list", 
                 "_attachments_list")

    # N2PGetFasteners constructor --------------------------------------------------------------------------------------
    def __init__(self): 

        """
        The constructor creates an empty N2PGetFasteners instance. Its attributes must be added as properties.

        Calling example: 
            >>> import NaxToPy as n2p 
            >>> from NaxToPy.Modules.Fasteners.N2PGetFasteners import N2PGetFasteners
            >>> model1 = n2p.load_model("route.fem") # model loaded from N2PModelContent 
            >>> fasteners = N2PGetFasteners()
            >>> # Compulsory input 
            >>> fasteners.Model = model1 
            >>> # Custom threshold is selected (optional)
            >>> fasteners.Thresh = 1.5
            >>> # Only some joints are to be analyzed (optional)
            >>> fasteners.GlobalIDList = [10, 11, 12, 13, 14]
            >>> # attachments will not be obtained
            >>> fasteners.GetAttachmentsBool = False  # True by default
            >>> # fasteners are obtained
            >>> fasteners.calculate()
        """

        self._model: N2PModelContent = None 
        self._get_attachments_bool: bool = True 

        self._thresh: float = 2.0 
        self._element_list: list[N2PElement] = None 

        self._joints_list: list[N2PJoint] = None  
        self._attachments_list: list[N2PAttachment] = None 
    # ------------------------------------------------------------------------------------------------------------------
        
    # Getters ----------------------------------------------------------------------------------------------------------
    @property 
    def Model(self) -> N2PModelContent: 

        """
        Model to be analyzed. It is a compulsory input and an error will occur if it is not present. 
        """
        
        return self._model 
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def GetAttachmentsBool(self) -> bool: 

        """
        Sets if the get_attachments() method will be used inside method calculate().
        """
        
        return self._get_attachments_bool
    # ------------------------------------------------------------------------------------------------------------------
    
    @property
    def Thresh(self) -> float: 

        """
        Tolerance used in the obtention of the N2Joints in C#. 2.0 by default.
        """

        return self._thresh
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def ElementList(self) -> list[N2PElement]: 
        """
        Property that returns the element_list attribute, that is, the list of the loaded CFASTs. 
        """

        return self._element_list 
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def JointsList(self) -> list[N2PJoint]: 

        """
        Property that returns the joints_list attribute, that is, the list of N2PJoints to be analyzed. 
        """
        
        return self._joints_list
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def PlateList(self) -> list[N2PPlate]: 

        """
        Property that returns the list of N2PPlates. 
        """
        
        return [j for i in self.JointsList for j in i.PlateList]
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def BoltsList(self) -> list[N2PBolt]: 

        """
        Property that returns the list of N2PBolts. 
        """
        
        return [i.Bolt for i in self.JointsList]
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def AttachmentsList(self) -> list[N2PAttachment]: 

        """
        Property that returns the attachments_list attribute, that is, the list of N2PAttachments. 
        """
        
        return self._attachments_list 
    # ------------------------------------------------------------------------------------------------------------------

    # Setters ----------------------------------------------------------------------------------------------------------
    
    @Model.setter 
    def Model(self, value: N2PModelContent) -> None: 

        if not isinstance(value, N2PModelContent): 
            N2PLog.Error.E535(value, N2PModelContent)
        else: 
            self._model = value 
    # ------------------------------------------------------------------------------------------------------------------
        
    @GetAttachmentsBool.setter 
    def GetAttachmentsBool(self, value: bool) -> None: 

        if not isinstance(value, bool): 
            N2PLog.Warning.W527(value, bool)
        else: 
            self._get_attachments_bool = value 
    # ------------------------------------------------------------------------------------------------------------------
        
    @Thresh.setter
    def Thresh(self, value: float) -> None: 

        if not isinstance(value, float) and not isinstance(value, int): 
            N2PLog.Warning.W527(value, float)
        else: 
            self._thresh = value 
    # ------------------------------------------------------------------------------------------------------------------

    @ElementList.setter 
    def ElementList(self, value: Union[list[N2PElement], tuple[N2PElement], set[N2PElement], N2PElement]) -> None: 

        if type(value) == tuple or type(value) == set: 
            value = list(value) 
        elif type(value) == N2PElement: 
            value = [value]

        for i in value: 
            if not isinstance(i, N2PElement): 
                N2PLog.Warning.W527(i, N2PElement)
                value.remove(i)

        if value == []: 
            N2PLog.Error.E536("ElementList", N2PElement)
        else: 
            self._element_list = value 

    # Method used to create all joints, plates and bolts ---------------------------------------------------------------
    def get_joints(self) -> None: 

        """
        This method is used to create all N2PJoints, N2PPlates and N2PBolts and assign them certain useful attributes. 
        In order to work, the n2joints and model attributes must have been previously filled. If they have not, an 
        error will occur. 

        The following steps are followed: 
            1. All N2Joints are created differently depending on the user's inputs. 
            1. All N2PJoints are created. Inside this, all N2PBolts and N2PPlates associated to each N2PJoint are also 
            created. 
            2. All N2PBolts, N2PPlates are assigned its corresponding N2PElements and N2PNodes. Also, N2PJoints are 
            assigned its bolt's N2PElements and N2PNodes, as well as its plates' N2PElements and N2PNodes. 

        Calling example: 
            >>> fasteners.get_joints()
        """

        t1 = time() 
        if self.Model is None: 
            N2PLog.Error.E521() 

        if self.ElementList:
            globalIDList = [i.InternalID for i in self.ElementList]
            n2joints = list(self.Model._N2PModelContent__vzmodel.GetJoints(self._thresh, global_id_list = globalIDList))
        else:  
            n2joints = list(self.Model._N2PModelContent__vzmodel.GetJoints(self._thresh))


        # N2PJoints are created from the N2Joints
        self._joints_list = [N2PJoint(i, self._model.ModelInputData) for i in n2joints]
        for i in self.JointsList: 
            for j in i.PlateList: 
                j._joint = i
                
        elementList = list(self.Model.ElementsDict.values())
        for i in self.PlateList: 
            i._element_list = [elementList[j] for j in i.GlobalID]
        for i in self.JointsList: 
            i.Bolt._element_list = [elementList[j] for j in i.Bolt.OneDimElemsIDList]
            i._diameter = self.Model.PropertyDict[i.Bolt.ElementList[0].Prop].Diameter
            if i.PlateList == [] or i.PlateElementList == []: 
                N2PLog.Warning.W529(i.BoltElementIDList[0])
                self._joints_list.remove(i)                 

        N2PLog.Debug.D601(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to obtain the distance from each N2PBolt to its N2PPlates' edge --------------------------------------
    def get_distance(self) -> None: 

        """
        Method used to obtain the distance from every N2PPlate's edge to its N2PJoint, the intersection between an 
        N2PPlate and its N2PJoint and the perpendicular direction to the N2PPlates. The get_joints() method must be 
        used before this one. Otherwise, an error will occur. 

        Calling example: 
            >>> fasteners.get_distance() 
        """

        t1 = time() 
        if self.JointsList is None: 
            N2PLog.Error.E522() 

        # Only CQUAD4 and CTRIA3 elements are supported. 
        supportedElements = ["CQUAD4", "CTRIA3"]
        domain = [i for i in self.Model.get_elements() if i.TypeElement in supportedElements]

        [i.get_distance(self.Model, domain) for i in self.JointsList]
        N2PLog.Debug.D605(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to obtain a list of attachments ----------------------------------------------------------------------
    def get_attachments(self) -> None: 


        """
        Method used to obtain the list of N2PAttachments and calculate their pitch. The get_joints() method must be 
        used before this one. Otherwise, an error will occur. 

        Calling example: 
            >>> fasteners.get_attachments() 
        """

        t1 = time()
        if self.JointsList is None: 
            N2PLog.Error.E522() 

        self._attachments_list = get_attachments(self.Model, self.JointsList)
        for i in self.AttachmentsList: 
            for j in i.JointsList: 
                j._attachment = i
        [i.get_pitch() for i in self.AttachmentsList]
        N2PLog.Debug.D603(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to use all previous methods --------------------------------------------------------------------------
    def calculate(self) -> None: 

        """
        Method used to do all the previous calculations. 

        Calling example: 
            >>> fasteners.calculate()
        """

        self.get_joints() 
        self.get_distance() 
        if self.GetAttachmentsBool: 
            self.get_attachments()
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to flip the list of plates of the necessary joints 
    def flip_plates(self) -> None: 

        """
        Method used to flip some plate lists. 

        Calling example: 
            >>> fasteners.flip_plates( )
        """

        for i in self.JointsList: 
            if i.SwitchPlates: 
                i.PlateList.reverse()