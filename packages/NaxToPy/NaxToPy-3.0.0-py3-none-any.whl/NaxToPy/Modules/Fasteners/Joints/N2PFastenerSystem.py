#
class N2PFastenerSystem:

    """
    class that represents a specific fastener designation whose values need to be defined in order to 
    obtain RF values for one or more failure modes

    Attributes:
        Designation: fastener system name (str)
        Fastener_pin_single_SH_allow: fastener pin single shear strength allowable [Force] (float)
        Fastener_collar_single_SH_allow: fastener collar single shear strength allowable [Force] (float)
        Fastener_pin_tensile_allow: fastener pin tensile strength allowable [Force] (float)
        Fastener_collar_tensile_allow: fastener collar tensile strength allowable [Force] (float)
        D_head: head diameter (float)
        D_tail: tail diameter (float)
        D_nom: nominal diameter (float)
        Configuration: BOLT or RIVET or SOLID (str) (Default: BOLT)
        FastenerType: LOCK or BLIND (str) (Default: LOCK)
        FastenerInstallation: PERMANENT or REMOVABLE or QUICK RELEASE (str) (Default: PERMANENT)
        FastenerHead: PAN or CSK (str) (Default: PAN)
        FloatingNut: True or False (str) (Default: False)
        AluminumNut: True or False (str) (Default: False)
        
    """

    # N2PFastenerSystem ----------------------------------------------------------------------------------------
    def __init__(self): 

        """
        The constructor creates an empty N2PGetFasteners instance. Its attributes must be added as properties.

        Calling example:
            >>> Fastener_HWGT315 = N2PFastenerSystem()
            >>> Fastener_HWGT315.designation = "HWGT315-LEADING-EDGE"
            >>> Fastener_HWGT315.Fastener_pin_single_SH_allow = 5000.0
            >>> Fastener_HWGT315.Fastener_collar_single_SH_allow = 6000.0
            >>> Fastener_HWGT315.Fastener_pin_tensile_allow = 7000.0
            >>> Fastener_HWGT315.Fastener_collar_tensile_allow = 8000.0
            >>> Fastener_HWGT315.D_head = 10.0
            >>> Fastener_HWGT315.D_tail = 9.0
            >>> Fastener_HWGT315.D_nom = 5.0
            >>> Fastener_HWGT315.Configuration = "RIVET" (optional)
            >>> Fastener_HWGT315.FastenerType = "LOCK" (optional)
            >>> Fastener_HWGT315.FastenerInstallation = "REMOVABLE" (optional)
            >>> Fastener_HWGT315.FastenerHead = "PAN" (optional)
            >>> Fastener_HWGT315.FloatingNut = "False" (optional)
            >>> Fastener_HWGT315.AluminumNut = "False" (optional)
        """

        self._designation: str = None
        self._fastener_pin_single_SH_allow: float = None
        self._fastener_collar_single_SH_allow: float = None
        self._fastener_pin_tensile_allow: float = None
        self._fastener_collar_tensile_allow: float = None
        self._d_head: float = None
        self._d_tail: float = None
        self._d_nom: float = None
        self._configuration: str = "BOLT"
        self._fastenertype: str = "LOCK"
        self._fastenerinstallation: str = "PERMANENT"
        self._fastenerhead: str = "PAN"
        self._floatingnut: str = "False"
        self._aluminumnut: str = "False"

    # -----------------------------------------------------------------------------------------------------------
    
    # Getters ---------------------------------------------------------------------------------------------------
    @property
    def Designation(self) -> str:

        """
        Property that returns the designation of the fastener.
        """

        return self._designation
    #------------------------------------------------------------------------------------------------------------

    @property
    def Fastener_pin_single_SH_allow(self) -> float:

        """
        Property that returns the designation of the fastener pin single shear strength allowable.
        """

        return self._fastener_pin_single_SH_allow
    #------------------------------------------------------------------------------------------------------------

    @property
    def Fastener_collar_single_SH_allow(self) -> float:

        """
        Property that returns the designation of the fastener collar single shear strength allowable.
        """

        return self._fastener_collar_single_SH_allow
    #------------------------------------------------------------------------------------------------------------

    @property
    def Fastener_pin_tensile_allow(self) -> float:

        """
        Property that returns the designation of the fastener pin tensile strength allowable.
        """

        return self._fastener_pin_tensile_allow
    #------------------------------------------------------------------------------------------------------------

    @property
    def Fastener_collar_tensile_allow(self) -> float:

        """
        Property that returns the designation of the fastener collar tensile strength allowable.
        """

        return self._fastener_collar_tensile_allow
    #------------------------------------------------------------------------------------------------------------

    @property
    def D_head(self) -> float:
        """
        Property that returns the head diameter of the fastener.
        """

        return self._d_head
    #------------------------------------------------------------------------------------------------------------

    @property
    def D_tail(self) -> float:
        """
        Property that returns the tail diameter of the fastener.
        """

        return self._d_tail
    #------------------------------------------------------------------------------------------------------------

    @property
    def D_nom(self) -> float:
        """
        Property that returns the nominal diameter of the fastener.
        """

        return self._d_nom
    #------------------------------------------------------------------------------------------------------------

    @property
    def Configuration(self) -> str:
        """
        Property that returns the fastener configuration (RIVET/BOLT/SOLID) (Default: BOLT).
        """

        return self._configuration
    #------------------------------------------------------------------------------------------------------------

    @property
    def FastenerType(self) -> str:
        """
        Property that returns the fastener configuration (LOCK/BLIND) (Default: LOCK).
        """

        return self._fastenertype
    #------------------------------------------------------------------------------------------------------------

    @property
    def FastenerInstallation(self) -> str:
        """
        Property that returns the fastener installation (PERMANENT/REMOVABLE/QUICK RELEASE) (Default: PERMANENT).
        """

        return self._fastenerinstallation
    #------------------------------------------------------------------------------------------------------------

    @property
    def FastenerHead(self) -> float:
        """
        Property that returns the fastener head geometry (PAN/CSK) (Default: PAN).
        """

        return self._fastenerhead
    #------------------------------------------------------------------------------------------------------------

    @property
    def FloatingNut(self) -> bool:
        """
        Property that returns if the fastener has a floating nut (True) or not (False).
        """

        return self._floatingnut
    #------------------------------------------------------------------------------------------------------------

    @property
    def AluminumNut(self) -> bool:
        """
        Property that returns if the nut is made out of aluminum (True) or not (False).
        """

        return self._aluminumnut
    #------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------

    # Setters ---------------------------------------------------------------------------------------------------
    @Designation.setter
    def designation(self, value: str):

        # If "value" is a string, it is stored.
        if type(value) == str:
            self._designation = value
        else:
            raise Exception("Fastener designation must be a string")
    #------------------------------------------------------------------------------------------------------------

    @Fastener_pin_single_SH_allow.setter
    def Fastener_pin_single_SH_allow(self, value: float):

        # If "value" is a float, it is stored.
        if type(value) == float:
            self._fastener_pin_single_SH_allow = value
        else:
            raise Exception("Fastener_pin_single_SH_allow must be a float")
    #------------------------------------------------------------------------------------------------------------

    @Fastener_collar_single_SH_allow.setter
    def Fastener_collar_single_SH_allow(self, value: float):

        # If "value" is a float, it is stored.
        if type(value) == float:
            self._fastener_collar_single_SH_allow = value
        else:
            raise Exception("Fastener_collar_single_SH_allow must be a float")
    #------------------------------------------------------------------------------------------------------------

    @Fastener_pin_tensile_allow.setter
    def Fastener_pin_tensile_allow(self, value: float):

        # If "value" is a float, it is stored.
        if type(value) == float:
            self._fastener_pin_tensile_allow = value
        else:
            raise Exception("Fastener_pin_tensile_allow must be a float")
    #------------------------------------------------------------------------------------------------------------

    @Fastener_collar_tensile_allow.setter
    def Fastener_collar_tensile_allow(self, value: float):

        # If "value" is a float, it is stored.
        if type(value) == float:
            self._fastener_collar_tensile_allow = value
        else:
            raise Exception("Fastener_collar_tensile_allow must be a float")
    #------------------------------------------------------------------------------------------------------------

    @D_head.setter
    def D_head(self, value: float):

        # If "value" is a float, it is stored.
        if type(value) == float:
            self._d_head = value
        else:
            raise Exception("Fastener D_head must be a float")
    #------------------------------------------------------------------------------------------------------------
    
    @D_tail.setter
    def D_tail(self, value: float):

        # If "value" is a float, it is stored.
        if type(value) == float:
            self._d_tail = value
        else:
            raise Exception("Fastener D_tail must be a float")
    #------------------------------------------------------------------------------------------------------------

    @D_nom.setter
    def D_nom(self, value: float):

        # If "value" is a float, it is stored.
        if type(value) == float:
            self._d_nom = value
        else:
            raise Exception("Fastener D_nom must be a float")
    #------------------------------------------------------------------------------------------------------------

    @Configuration.setter
    def Configuration(self, value: str):

        # If "value" is a str, it is stored.
        if type(value) == str:
            if value == "RIVET" or value =="BOLT" or value =="SOLID":
                self._configuration = value
            else:
                raise Exception("Fastener Configuration must be RIVET or BOLT or SOLID")
        else:
            raise Exception("Fastener Configuration must be a string")
    #------------------------------------------------------------------------------------------------------------

    @FastenerType.setter
    def FastenerType(self, value: str):

        # If "value" is a str, it is stored.
        if type(value) == str:
            if value == "LOCK" or value =="BLIND":
                self._fastenertype = value
            else:
                raise Exception("FastenerType must be LOCK or BLIND")
        else:
            raise Exception("FastenerType must be a string")
    #------------------------------------------------------------------------------------------------------------

    @FastenerInstallation.setter
    def FastenerInstallation(self, value: str):

        # If "value" is a float, it is stored.
        if type(value) == str:
            if value == "PERMANENT" or value == "REMOVABLE" or value =="QUICK RELEASE":
                self._fastenerinstallation = value
            else:
                raise Exception("FastenerInstallation must be PERMANENT or REMOVABLE or QUICK RELEASE")
        else:
            raise Exception("FastenerInstallation must be a string")
    #------------------------------------------------------------------------------------------------------------

    @FastenerHead.setter
    def FastenerHead(self, value: str):

        # If "value" is a string, it is stored.
        if type(value) == str:
            if value=="PAN" or value=="CSK":
                self._fastenerhead = value
            else:
                raise Exception("FastenerHead must be PAN or CSK")
        else:
            raise Exception("FastenerHead must be a string")
    #------------------------------------------------------------------------------------------------------------

    @FloatingNut.setter
    def FloatingNut(self, value: str):

        # If "value" is a string, it is stored.
        if type(value) == str:
            if value=="True" or value=="False":
                self._floatingnut = value
            else:
                raise Exception("FloatingNut must be True or False")
        else:
            raise Exception("FloatingNut must be a string")
    #------------------------------------------------------------------------------------------------------------

    @AluminumNut.setter
    def AluminumNut(self, value: str):

        # If "value" is a string, it is stored.
        if type(value) == str:
            if value=="True" or value=="False":
                self._aluminumnut = value
            else:
                raise Exception("AluminumNut must be True or False")
        else:
            raise Exception("AluminumNut must be a string")
    #------------------------------------------------------------------------------------------------------------