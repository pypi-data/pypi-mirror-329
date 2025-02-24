import NaxToPy as NP 
from NaxToPy import N2PLog
from NaxToPy.Core.N2PModelContent import N2PModelContent 
from NaxToPy.Core.Classes.N2PLoadCase import N2PLoadCase
from NaxToPy.Modules.Fasteners.N2PGetFasteners import N2PGetFasteners
from NaxToPy.Modules.Fasteners.Joints.N2PJoint import N2PJoint
from NaxToPy.Modules.Fasteners.Joints.N2PPlate import N2PPlate
from NaxToPy.Modules.Fasteners._N2PFastenerAnalysis.Core.Functions.N2PGetResults import get_results  
from NaxToPy.Modules.Fasteners._N2PFastenerAnalysis.Core.Functions.N2PLoadModel import get_adjacency, import_results
from NaxToPy.Modules.common.data_input_hdf5 import DataEntry 
from NaxToPy.Modules.common.hdf5 import HDF5_NaxTo
import numpy as np
import os 
import sys 
from time import time 
from typing import Union, Literal 

class N2PGetLoadFasteners: 

    """
    Class used to calculate joints' forces and bypass loads.

    The instance of this class must be prepared using its properties before calling it method calculate.
    """

    __slots__ = ("_results_files", 
                 "_get_fasteners", 
                 "_joints_list", 
                 "_model", 
                 "_adjacency_level", 
                 "_load_cases", 
                 "_corner_data", 
                 "_bypass_parameters", 
                 "_default_diameter", 
                 "_analysis_name", 
                 "_export_location", 
                 "_type_analysis", 
                 "_type_export", 
                 "_export_precision", 
                 "_load_case_number", 
                 "_results")

    # N2PGetLoadFasteners constructor ----------------------------------------------------------------------------------
    def __init__(self): 

        """
        The constructor creates an empty N2PGetLoadFasteners instance. Its attributes must be added as properties.

        Calling example: 
            >>> import NaxToPy as n2p 
            >>> from NaxToPy.Modules.Fasteners.N2PGetFasteners import N2PGetFasteners
            >>> from NaxToPy.Modules.Fasteners.N2PGetLoadFasteners import N2PGetLoadFasteners
            >>> model1 = n2p.get_model(route.fem) # model loaded 
            >>> fasteners = N2PGetFasteners() 
            >>> fasteners.Model = model1 # compulsory input 
            >>> fasteners.Thresh = 1.5 # a custom threshold is selected (optional)
            >>> fasteners.ElementList = model1.get_elements([10, 11, 12, 13, 14]) # Only some joints are to be 
            analyzed (optional)
            >>> fasteners.GetAttachmentsBool = False # attachments will not be obtained (optional)
            >>> fasteners.calculate() # fasteners are obtained 
            >>> fasteners.JointsList[0].Diameter = 6.0 # this joint is assigned a certain diameter 
            >>> loads = N2PGetLoadFasteners()
            >>> loads.GetFasteners = fasteners # compulsory input 
            >>> loads.ResultsFiles = [r"route1.op2", r"route2.op2", r"route3.op2"] # the desired results files are 
            loaded
            >>> loads.AdjacencyLevel = 3 # a custom adjacency level is selected (optional)
            >>> loads.LoadCases = [1, 2, 133986] # list of load cases' ID to be analyzed (optional) 
            >>> loads.CornerData = True # the previous load cases have corner data (optional)
            >>> # some bypass parameters are changed (optional and not recommended)
            >>> loads.BypassParameters = {"max iterations" = 50, "PROJECTION TOLERANCE" = 1e-6} 
            >>> loads.DefaultDiameter = 3.6 #  joints with no previously assigned diameter will get this diameter (optional)
            >>> loads.AnalysisName = "Analysis_1" # name of the CSV file where the results will be exported (optional)
            >>> loads.ExportLocation = r"path" # results are to be exported to a certain path (optional)
            >>> loads.TypeAnalysis = "Altair" # results will be exported in the Altair style (optional)
            >>> loads.calculate() # calculations will be made and results will be exported

        Instead of using loads.GetFasteners, the user could also set these attributes:
            >>> loads.Model = model1 # the same model is loaded, compulsory input 
            >>> loads.JointsList = fasteners.JointsList[0:10] # only a certain amount of joints is loaded, compulsory 
            input 
            >>> loadFasteners.calculate() # calculations will be made with all of the default parameters and, 
            therefore, results will not be exported. 
        """
        
        self._results_files: list[str] = None 
        self._get_fasteners: N2PGetFasteners = None 
        self._joints_list: list[N2PJoint] = None 
        self._model: N2PModelContent = None 
        self._adjacency_level: int = 4
        self._load_cases: list[N2PLoadCase] = None 
        self._corner_data: bool = False 
        self._bypass_parameters: dict = {"MATERIAL FACTOR METAL": 4.0, 
                                         "MATERIAL FACTOR COMPOSITE": 4.0, 
                                         "AREA FACTOR": 2.5, 
                                         "MAX ITERATIONS": 200, 
                                         "BOX TOLERANCE": 0.05, 
                                         "PROJECTION TOLERANCE": 0.05, 
                                         "TOLERANCE INCREMENT": 10}
        self._default_diameter: float = None 
        self._analysis_name: str = "JointAnalysis"
        self._export_location: str = None 
        self._type_analysis: Literal["ALTAIR", "PAG"] = "PAG"
        self._type_export: Literal["NAXTOPY", "ALTAIR", "PAG_TXT", "PAG_CSV", "PAG_HDF5"] = "PAG_TXT"
        self._export_precision: int = 4 
        self._load_case_number: int = 100 
        self._results: dict = None 
    # ------------------------------------------------------------------------------------------------------------------
    
    # Getters ----------------------------------------------------------------------------------------------------------
    @property
    def ResultsFiles(self) -> list[str]: 
        """
        List of paths of OP2 results files. It is a compulsory input unless the model loaded in model or in get_fasteners
        has results loaded in. 
        """

        return self._results_files
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def GetFasteners(self) -> N2PGetFasteners: 

        """
        N2PGetFasteners model. Either this, or both _list_joints and _model, is a compulsory input and an error will occur
        if this is not present.
        """

        return self._get_fasteners
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def Model(self) -> N2PModelContent: 

        """
        Model to be analyzed. Either both this and _list_joints, or _get_fasteners, are compulsory inputs and an error
        will occur if they are not present. 
        """

        return self._model 
    # ------------------------------------------------------------------------------------------------------------------
    
    @property 
    def JointsList(self) -> list[N2PJoint]: 

        """
        Property that returns the joints_list attribute, that is, the list of N2PJoints to be analyzed. 
        """

        return self._joints_list
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def AdjacencyLevel(self) -> int: 

        """
        Number of adjacent elements that are loaded into the model. 4 by default.
        """

        return self._adjacency_level
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def LoadCases(self) -> list[N2PLoadCase]: 

        """
        Property that returns the load_cases attributes, that is, the list of the load cases to be analyzed. 
        """
        
        return self._load_cases 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def CornerData(self) -> bool: 
        
        """
        Whether there is data on the corners or not to extract the results. False by default.
        """
        
        return self._corner_data 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def BypassParameters(self) -> dict: 

        """
        Dictionary with the parameters used in the bypass loads calculation. Even though the user may change any of
        these parameters, it is not recomended. 
        """

        return self._bypass_parameters 
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def DefaultDiameter(self) -> float: 

        """
        Diameter to be applied to joints with no previously assigned diameter. 
        """
        
        return self._default_diameter
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def AnalysisName(self) -> str: 

        """
        Name of the CSV file where the results are to be exported. 
        """
        
        return self._analysis_name
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def ExportLocation(self) -> str: 

        """
        Path where the results are to be exported. 
        """
        
        return self._export_location
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def TypeAnalysis(self) -> Literal["ALTAIR", "PAG"]: 

        """
        Property that returns the path where the type_analysis attribute, that is, whether the results are analyzed in 
        the Altair or PAG style. 
        """
        
        return self._type_analysis
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def TypeExport(self) -> Literal["NAXTOPY", "ALTAIR", "PAG_TXT", "PAG_CSV", "PAG_HDF5"]: 

        """
        Property that returns the path where the type_export attribute, that is, whether the results are exported in 
        the NaxToPy, Altair or PAG TXT, PAG CSV or PAG HDF5 style. 
        """
        
        return self._type_export
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def ExportPrecision(self) -> int: 

        """
        Property that returns the precision atribute, that is, the precision used when exporting the results to a HDF5 
        file. It can be either 4 or 8.
        """
        
        return self._export_precision    
    # ------------------------------------------------------------------------------------------------------------------

    @property 
    def LoadCaseNumber(self) -> int: 

        """
        Property that returns the load_case_number attribute, that is, the number of load cases that are analyzed at 
        the same time. 
        """
        
        return self._load_case_number    
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def Results(self) -> dict: 
        
        """
        Results obtained in get_results_joints(). 
        """
        
        return self._results 
    # ------------------------------------------------------------------------------------------------------------------

    # Setters ----------------------------------------------------------------------------------------------------------
    @ResultsFiles.setter 
    def ResultsFiles(self, value: Union[list[str], str]): 

        # If "value" is a list, then it must be a list of op2 files. 
        if type(value) == list: 
            for i in value: 
                if not os.path.exists(i) or not os.path.isfile(i): 
                    N2PLog.Error.E531(i)
            self._results_files = value 
        elif os.path.exists(value): 
            # If "value" is a string and a file, it is a single op2 file. 
            if os.path.isfile(value): 
                self._results_files = [value]
            # If "value" is a string and not a file, it is a folder. 
            else: 
                self._results_files = import_results(value) 
        else: 
            N2PLog.Error.E531(value)

        if self.JointsList and self.Model: 
            self.__create_model() 
    # ------------------------------------------------------------------------------------------------------------------

    @GetFasteners.setter 
    def GetFasteners(self, value: N2PGetFasteners) -> None: 

        if not isinstance(value, N2PGetFasteners): 
            N2PLog.Error.E535(value, N2PGetFasteners)

        if self.Model is not None or self.JointsList is not None: 
            N2PLog.Warning.W522() 

        self._get_fasteners = value 
        self._joints_list = self._get_fasteners._joints_list
        self._model = self._get_fasteners._model 
        if self.ResultsFiles: 
            self.__create_model() 
    # ------------------------------------------------------------------------------------------------------------------

    @Model.setter 
    def Model(self, value: N2PModelContent) -> None: 

        if not isinstance(value, N2PModelContent): 
            N2PLog.Error.E535(value, N2PModelContent)

        if self.GetFasteners is not None: 
            N2PLog.Warning.W523() 

        self._model = value 
        if self.JointsList and self.ResultsFiles: 
            self.__create_model() 
    # ------------------------------------------------------------------------------------------------------------------
        
    @JointsList.setter 
    def JointsList(self, value: Union[list[N2PJoint], tuple[N2PJoint], set[N2PJoint], N2PJoint]) -> None: 

        if self.GetFasteners is not None: 
            N2PLog.Warning.W524() 

        if type(value) == tuple or type(value) == set: 
            value = list(value) 
        elif type(value) == N2PJoint: 
            value = [value]

        for i in value: 
            if not isinstance(i, N2PJoint): 
                N2PLog.Warning.W527(i, N2PJoint)
                value.remove(i)

        if value == []: 
            N2PLog.Error.E536("ElementList", N2PJoint)
        else: 
            self._joints_list = value 
    # ------------------------------------------------------------------------------------------------------------------
        
    @AdjacencyLevel.setter 
    def AdjacencyLevel(self, value: int) -> None: 

        if not isinstance(value, int): 
            N2PLog.Warning.W527(value, int)
        else: 
            self._adjacency_level = value 
            if self.Model and self.JointsList and self.ResultsFiles: 
                self.__create_model() 
    # ------------------------------------------------------------------------------------------------------------------
        
    @LoadCases.setter 
    def LoadCases(self, value: Union[list[N2PLoadCase], tuple[N2PLoadCase], set[N2PLoadCase], N2PLoadCase]) -> None: 

        if type(value) == tuple or type(value) == set: 
            value = list(value) 
        elif type(value) == N2PLoadCase: 
            value = [value]

        for i in value: 
            if not isinstance(i, N2PLoadCase): 
                N2PLog.Warning.W527(i, N2PLoadCase)
                value.remove(i)
        
        if value == []: 
            N2PLog.Error.E536("LoadCases", N2PLoadCase)
        else: 
            self._load_cases = value
    # ------------------------------------------------------------------------------------------------------------------
        
    @CornerData.setter 
    def CornerData(self, value: bool) -> None: 

        if not isinstance(value, bool): 
            N2PLog.Warning.W527(value, bool)
        else: 
            self._corner_data = value 
    # ------------------------------------------------------------------------------------------------------------------
        
    @BypassParameters.setter 
    def BypassParameters(self, value: dict) -> None: 
        
        valueUpper = {}
        for i, j in value.items(): 
            valueUpper[i.upper().strip()] = j 
        if "MATERIAL FACTOR METAL" in valueUpper.keys(): 
            if type(valueUpper["MATERIAL FACTOR METAL"]) != float and type(valueUpper["MATERIAL FACTOR METAL"]) != int: 
                N2PLog.Warning.W526("MATERIAL FACTOR METAL")
                valueUpper.pop("MATERIAL FACTOR METAL")
        if "MATERIAL FACTOR COMPOSITE" in valueUpper.keys(): 
            if type(valueUpper["MATERIAL FACTOR COMPOSITE"]) != float and type(valueUpper["MATERIAL FACTOR COMPOSITE"]) != int: 
                N2PLog.Warning.W526("MATERIAL FACTOR COMPOSITE")
                valueUpper.pop("MATERIAL FACTOR COMPOSITE")  
        if "AREA FACTOR" in valueUpper.keys(): 
            if type(valueUpper["AREA FACTOR"]) != float and type(valueUpper["AREA FACTOR"]) != int: 
                N2PLog.Warning.W526("AREA FACTOR")
                valueUpper.pop("AREA FACTOR")
        if "MAX ITERATIONS" in valueUpper.keys(): 
            if type(valueUpper["MAX ITERATIONS"]) != int: 
                N2PLog.Warning.W526("MAX ITERATIONS")
                valueUpper.pop("MAX ITERATIONS")
        if "BOX TOLERANCE" in valueUpper.keys(): 
            if type(valueUpper["BOX TOLERANCE"]) != float and type(valueUpper["BOX TOLERANCE"]) != int: 
                N2PLog.Warning.W526("BOX TOLERANCE")
                valueUpper.pop("BOX TOLERANCE")
        if "PROJECTION TOLERANCE" in valueUpper.keys(): 
            if type(valueUpper["PROJECTION TOLERANCE"]) != float and type(valueUpper["PROJECTION TOLERANCE"]) != int: 
                N2PLog.Warning.W526("PROJECTION TOLERANCE")
                valueUpper.pop("PROJECTION TOLERANCE")
        if "TOLERANCE INCREMENT" in valueUpper.keys(): 
            if type(valueUpper["TOLERANCE INCREMENT"]) != float and type(valueUpper["TOLERANCE INCREMENT"]) != int: 
                N2PLog.Warning.W526("TOLERANCE INCREMENT")
                valueUpper.pop("TOLERANCE INCREMENT")

        self._bypass_parameters.update(valueUpper)
    # ------------------------------------------------------------------------------------------------------------------
        
    @DefaultDiameter.setter 
    def DefaultDiameter(self, value: float) -> None: 

        if not isinstance(value, float) and not isinstance(value, int): 
            N2PLog.Warning.W527(value, float)
        else: 
            self._default_diameter = value 
    # ------------------------------------------------------------------------------------------------------------------
        
    @AnalysisName.setter 
    def AnalysisName(self, value: str) -> None: 

        if not isinstance(value, str): 
            N2PLog.Warning.W527(value, str)
        else: 
            self._analysis_name = value 
    # ------------------------------------------------------------------------------------------------------------------

    @ExportLocation.setter 
    def ExportLocation(self, value: str) -> None: 

        if not isinstance(value, str): 
            N2PLog.Warning.W527(value, str)
        else: 
            self._export_location = value 
    # ------------------------------------------------------------------------------------------------------------------
        
    @TypeAnalysis.setter 
    def TypeAnalysis(self, value: Literal["ALTAIR", "PAG"]) -> None: 

        if not isinstance(value, str): 
            N2PLog.Warning.W527(value, str)
        else: 
            value = value.upper().replace(" ", "")
            if value == "ALTAIR" or value == "PAG": 
                self._type_analysis = value 
            else: 
                N2PLog.Warning.W525()
    # ------------------------------------------------------------------------------------------------------------------

    @TypeExport.setter 
    def TypeExport(self, value: Literal["NAXTOPY", "ALTAIR", "PAG_TXT", "PAG_CSV", "PAG_HDF5"]) -> None: 

        if not isinstance(value, str): 
            N2PLog.Warning.W527(value, str)
        else: 
            value = value.upper().replace(" ", "")
            acceptedValues = ["NAXTOPY", "ALTAIR", "PAG_TXT", "PAG_CSV", "PAG_HDF5"]
            if value in acceptedValues: 
                self._type_analysis = value 
            else: 
                N2PLog.Warning.W525()
    # ------------------------------------------------------------------------------------------------------------------

    @ExportPrecision.setter 
    def ExportPrecision(self, value: int) -> None: 

        if not isinstance(value, int): 
            N2PLog.Warning.W527(value, int)
        else: 
            if value == 4 or value == 8: 
                self._export_precision = value 
            else: 
                N2PLog.Warning.W528()
    # ------------------------------------------------------------------------------------------------------------------

    @LoadCaseNumber.setter 
    def LoadCaseNumber(self, value: int) -> None: 

        if not isinstance(value, int): 
            N2PLog.Warning.W527(value, int)
        else: 
            self._load_case_number = value 
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to create the model ----------------------------------------------------------------------------------
    def __create_model(self): 

        """
        Method used to create a new model and import its results. It fires when the model, joints_list (they may have 
        been filled with get_fasteners) and results_files attributes have been filled in. 
        """

        self._model = get_adjacency(self.Model, self.JointsList, self.AdjacencyLevel) 
        self._model.import_results_from_files(self.ResultsFiles) 
    # ------------------------------------------------------------------------------------------------------------------
        
    # Method used to updta elements ------------------------------------------------------------------------------------
    def update_elements(self): 
        
        """
        Method used to update some elements to the new model. 
        
        The following steps are followed: 

            1. Elements and their internal IDs are updated so that they correspond to the values of the new model. 
            2. Plates are assigned their A and B CFAST, as well as its orientation. This is done taking into account 
            the normal direction of the plate, the intersection point between the bolt and the plate, the direction of 
            the CFASTs and the A and B nodes of the CFASTs. 

        Calling example: 
            >>> loads.update_model() 
        """

        t1 = time() 
        if self.Model is None: 
            N2PLog.Error.E521() 
        if self.JointsList is None: 
            N2PLog.Error.E523() 
        if self.ResultsFiles is None: 
            N2PLog.Error.E534() 
        
        # Bolts are assigned their N2PElements from the new model 
        elementsDict = dict(self.Model.ElementsDict)
        partDict = self.Model._N2PModelContent__StrPartToID
        for i in self.JointsList: 
            i.Bolt._element_list = [elementsDict[(j, partDict[i.PartID])] for j in i.BoltElementIDList]
            cfast = i.Bolt.Cards 
            boltElements = [elementsDict[(k.ID, partDict[i.PartID])] for k in i.BoltElementList]
            for j in i.PlateList: 
                j._element_list = [elementsDict[(j.ElementIDList[k], partDict[j.PartID[k]])] for k in range(len(j.ElementIDList))]
                j._bolt_element_list = {"A": None, "B": None}
                j._bolt_direction = {"A": None, "B": None}
                j._cfast_factor = {"A": 0, "B": 0} 
                for k in range(len(boltElements)): 
                    dir = (np.array(boltElements[k].Nodes[1].GlobalCoords) - np.array(boltElements[k].Nodes[0].GlobalCoords))
                    dir = dir / np.linalg.norm(dir) 
                    if j.Normal @ dir > 0: # n_plate = n_cfast 
                        if cfast[k].TYPE == "ELEM": 
                            if cfast[k].IDA == j.PlateCentralCellSolverID: # nodo A, n = n 
                                j._bolt_element_list["B"] = boltElements[k]
                                j._bolt_direction["B"] = "<-"
                                j._cfast_factor["B"] = 1 
                            elif cfast[k].IDB == j.PlateCentralCellSolverID: # nodo B, n = n 
                                j._bolt_element_list["A"] = boltElements[k]
                                j._bolt_direction["A"] = "<-"
                                j._cfast_factor["A"] = 1 
                        else: 
                            if cfast[k].IDA == j.ElementList[0].Prop[0]: # nodo A, n = n 
                                j._bolt_element_list["B"] = boltElements[k]
                                j._bolt_direction["B"] = "<-"
                                j._cfast_factor["B"] = 1 
                            elif cfast[k].IDB == j.ElementList[0].Prop[0]: # nodo B, n = n 
                                j._bolt_element_list["A"] = boltElements[k]
                                j._bolt_direction["A"] = "<-"
                                j._cfast_factor["A"] = 1 
                    else: # n_plate = -n_cfast 
                        if cfast[k].TYPE == "ELEM": 
                            if cfast[k].IDA == j.PlateCentralCellSolverID: # nodo A, n = -n 
                                j._bolt_element_list["A"] = boltElements[k]
                                j._bolt_direction["A"] = "->"
                                j._cfast_factor["A"] = -1 
                            elif cfast[k].IDB == j.PlateCentralCellSolverID: # nodo B, n = -n
                                j._bolt_element_list["B"] = boltElements[k]
                                j._bolt_direction["B"] = "->"
                                j._cfast_factor["B"] = -1 
                        else: 
                            if cfast[k].IDA == j.ElementList[0].Prop[0]: # nodo A, n = -n 
                                j._bolt_element_list["A"] = boltElements[k]
                                j._bolt_direction["A"] = "->"
                                j._cfast_factor["A"] = -1 
                            elif cfast[k].IDB == j.ElementList[0].Prop[0]: # nodo B, n = -n
                                j._bolt_element_list["B"] = boltElements[k]
                                j._bolt_direction["B"] = "->"
                                j._cfast_factor["B"] = -1 

        # If no load cases have been selected, all of them are 
        if self.LoadCases == [] or not self.LoadCases: 
            self._load_cases = self.Model.LoadCases 
            N2PLog.Info.I500()
        if self.LoadCases is None or self.LoadCases == []: 
            N2PLog.Error.E504()
        
        N2PLog.Debug.D600(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to obtain the load cases' results --------------------------------------------------------------------
    def get_results_joints(self, loadCaseList: list[N2PLoadCase]): 

        """
        Method used to obtain the results of the model. If no load cases have been selected, then it is assumed that all 
        load cases are to be analyzed. In order to work, the joints_list and model attributes must have been previously 
        filled. If they have not, an error will occur. 

        The following steps are followed: 

            1. If no load cases have been selected by the user, all load cases in the model will be analyzed. 
            2. Results are obtained with the get_results() function. Its outputs are, (a), the results per se, and (b), 
            the list of broken load cases, that is, the list of load cases that lack an important result. 
            3. If there are some broken load cases, they are removed from the _load_cases attribute and. If all load 
            cases were broken (meaning that the current _load_cases attribute is empty), an error is displayed. 

        Calling example: 
            >>> loads.get_results_joints()
        """

        t1 = time() 
        if self.Model is None: 
            N2PLog.Error.E521() 
        if self.JointsList is None: 
            N2PLog.Error.E523() 
        if self.ResultsFiles is None: 
            N2PLog.Error.E534() 

        # Results and broken load cases are obtained 
        resultsList = get_results(self.Model, loadCaseList, self.CornerData, self.JointsList[0].Bolt.Type)
        self._results = resultsList[0]
        brokenLC = resultsList[1]
        # Broken load cases are removed 
        if len(brokenLC) != 0: 
            for i in brokenLC: 
                self._load_cases.remove(i)
        # If all load cases are broken, an error occurs 
        if self.LoadCases is None or self.LoadCases == []: 
            N2PLog.Critical.C520()
        N2PLog.Debug.D600(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------
        
    # Method used to obtain the joint's forces -------------------------------------------------------------------------
    def get_forces_joints(self): 
        
        """
        Method used to obtain the 1D forces of each joint. In order to work, the results attribute must have been 
        previously filled (by having called get_results_joints()). If it has not, an error will occur. 

        Calling example: 
            >>> loads.get_forces_joints()
        """

        t1 = time() 
        if self.Results is None: 
            N2PLog.Error.E524() 

        for i, j in enumerate(self.JointsList, start = 1): 
            if self.TypeAnalysis == "ALTAIR": 
                j.get_forces(self.Results)
            else: 
                j.get_forces_PAG(self.Results)
            self.__progress(i, len(self.JointsList), "Processing forces.")
            if i < len(self.JointsList): 
                sys.stdout.write("\r")
                sys.stdout.flush() 
        sys.stdout.write("\n")
        N2PLog.Debug.D606(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------
        
    # Method used to obtain the joint's bypass loads -------------------------------------------------------------------    
    def get_bypass_joints(self): 

        """
        Method used to obtain the bypass loads of each joint. If an N2PJoint has no diameter, the default diameter is 
        assigned (in case it has been defined by the user). In order to work, the results attribute must have been 
        previously filled (by having called get_results_joints()). If it has not, an error will occur. 

        The following steps are followed: 

            1. If there are joints with no diameter, the default one is assigned.
            2. If there are still joints with no diameter or negative diameter (which could happen if some joints did 
            not have a diameter and no default diameter was given), these joints are removed from the list of joints, 
            as well as their associated N2PBolts and N2PPlates, and an error is displayed. 
            3. The bypass loads of each (remaining) N2PJoint is calculated. 

        Calling example: 
            >>> loads.get_bypass_joints()
        """

        t1 = time()
        if self.Results is None: 
            N2PLog.Error.E524() 

        # Joints with no diameter are assigned one 
        for i in self.JointsList: 
            if i.Diameter is None: 
                i._diameter = self.DefaultDiameter
        
        # Joints with no diameter are identified and removed 
        wrongJoints = [i for i in self.JointsList if i.Diameter is None or i.Diameter <= 0]
        wrongJointsID = [i.ID for i in wrongJoints]
        if len(wrongJointsID) > 0: 
            N2PLog.Error.E517(wrongJointsID)
        
        for i in self.JointsList: 
            if i in wrongJoints: 
                self._joints_list.remove(i)

        for i, j in enumerate(self.JointsList, start = 1): 
            if self.TypeAnalysis == "ALTAIR": 
                j.get_bypass_loads(self.Model, self.Results, self.CornerData, materialFactorMetal = self.BypassParameters["MATERIAL FACTOR METAL"], 
                                   materialFactorComposite = self.BypassParameters["MATERIAL FACTOR COMPOSITE"], areaFactor = self.BypassParameters["AREA FACTOR"], 
                                   maxIterations = self.BypassParameters["MAX ITERATIONS"], boxTol = self.BypassParameters["BOX TOLERANCE"], 
                                   projTol = self.BypassParameters["PROJECTION TOLERANCE"])
            else: 
                j.get_bypass_loads_PAG(self.Model, self.Results, self.CornerData, materialFactorMetal = self.BypassParameters["MATERIAL FACTOR METAL"], 
                                       materialFactorComposite = self.BypassParameters["MATERIAL FACTOR COMPOSITE"], areaFactor = self.BypassParameters["AREA FACTOR"], 
                                       maxIterations = self.BypassParameters["MAX ITERATIONS"], projTol = self.BypassParameters["PROJECTION TOLERANCE"], 
                                       increaseTol = self.BypassParameters["TOLERANCE INCREMENT"])
            self.__progress(i, len(self.JointsList), "Processing bypasses.")
            if i < len(self.JointsList): 
                sys.stdout.write("\r")
                sys.stdout.flush()
        sys.stdout.write("\n")
        N2PLog.Debug.D607(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------
        
    # Method used to export the obtained results to a CSV file ---------------------------------------------------------
    def export_results(self): 

        """
        Method used to export the obtained results to a CSV file. 

        Calling example: 
            >>> loads.export_results()
        """

        t1 = time()
        if self.JointsList[0].PlateList[0].BearingForce is None: 
            N2PLog.Error.E529() 
        elif self.JointsList[0].PlateList[0].BoxDimension is None: 
            N2PLog.Error.E530()
        if self.TypeExport == "PAG_TXT": 
            self.__export_pag_txt()
        elif self.TypeExport == "PAG_HDF5": 
            self.__export_pag_hdf5() 
        else: 
            [i.export_forces(self.Model, self.ExportLocation, self.AnalysisName, self.Results, self.TypeAnalysis) for i in self.JointsList]
        N2PLog.Debug.D608(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------

    # Method used to export the obtained PAG results as a txt file -----------------------------------------------------
    def __export_pag_txt(self): 

        """
        Method used to export the obtained results, if they are in PAG style, in a txt. It works similarly as the other 
        export options but, in order to follow the same methodology as the one followed in PAG, this method cannot be 
        in the N2PJoint file. 

        Calling example: 
            >>> loads.__export_pag_txt() 
        """

        newPathFile = "{}\\{}_fastpph.txt".format(self.ExportLocation, self.AnalysisName)
        propDict = self.Model.PropertyDict 
        if self.GetFasteners: 
            plateList = self.GetFasteners.PlateList 
        else: 
            plateList = [] 
            for i in self.JointsList: 
                for j in i.PlateList: 
                    plateList.append(j) 

        lcList = [i.ID for i in self.LoadCases]
        with open(newPathFile, "a+") as i: 
            h11 = " ----------  ----------------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ------------------------------  ------------------------------  ------------------------------  ------------------------------  ------------------------------  ------------------------------  ------------------------------  ------------------------------"
            h12 = "   A/B-ELEM      A/B-PROPERTY     CFAST_A     CFAST_B  DIRECTIONS    EXT.ZONE   ELEMENT_1   ELEMENT_2   ELEMENT_3   ELEMENT_4   ELEMENT_5   ELEMENT_6   ELEMENT_7   ELEMENT_8                  POINT_1(X,Y,Z)                  POINT_2(X,Y,Z)                  POINT_3(X,Y,Z)                  POINT_4(X,Y,Z)                  POINT_5(X,Y,Z)                  POINT_6(X,Y,Z)                  POINT_7(X,Y,Z)                  POINT_8(X,Y,Z)"
            h13 = " ----------  ----------------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ------------------------------  ------------------------------  ------------------------------  ------------------------------  ------------------------------  ------------------------------  ------------------------------  ------------------------------"
            i.write("\n")
            i.write(h11)
            i.write("\n")
            i.write(h12)
            i.write("\n")
            i.write(h13)
            i.write("\n")
            for p in plateList: 
                plateElem = p.ElementList[0]
                if propDict[plateElem.Prop].PropertyType == "PSHELL": 
                    prop = "PSHEL" + "." + str(plateElem.Prop[0])
                else: 
                    prop = propDict[plateElem.Prop].PropertyType + "." + str(plateElem.Prop[0])
                boltElementList = p.BoltElementList
                if boltElementList["A"]: 
                    cfastA_id = "{:12}".format(boltElementList["A"].ID)
                    directionA = p.BoltDirection["A"]
                else: 
                    cfastA_id = "{:12}".format(0)
                    directionA = "  "
                if boltElementList["B"]: 
                    cfastB_id = "{:12}".format(boltElementList["B"].ID)
                    directionB = p.BoltDirection["B"]
                else: 
                    cfastB_id = "{:12}".format(0)
                    directionB = "  "
                extZone = "      SQUARE"
                boltElementsPlate = [l.ID for l in p.BoltElementList.values() if l]

                data1 = "{:11}".format(plateElem.ID) + "    " + prop + cfastA_id + cfastB_id + "       " + directionA + "|" + directionB + extZone
                for l in ["{:12}".format(element.ID) for element in p.BoxElements.values()]: 
                    data1 = data1 + l
                boxPoints = list(p.BoxPoints.values())
                data1 = data1 + "     "
                for l in boxPoints: 
                    data1 = data1 + "[" + "{0:.2f}".format(l[0]) + "," + "{0:.2f}".format(l[1]) + "," + "{0:.2f}".format(l[2]) + "]" + "     "
                i.write(data1) 
                i.write("\n")
            
            h21 = " ----------  ----------------  ----------  ----------  ----------  ----------  ----------  ----------  -----------------------"
            h22 = "   CFAST-ID    CFAST-PROPERTY     GS-NODE     GA-NODE     GB-NODE      A-ELEM      B-ELEM    DIAM(mm)  MATERIAL"
            h23 = " ----------  ----------------  ----------  ----------  ----------  ----------  ----------  ----------  -----------------------"

            i.write("\n")
            i.write(h21)
            i.write("\n")
            i.write(h22)
            i.write("\n")
            i.write(h23)
            i.write("\n")
            
            for joint in self.JointsList: 
                for b in joint.Bolt.Cards: 
                    if propDict.get(b.PID): 
                        propfast = propDict[b.PID].PropertyType + "." + str(b.PID)
                    else: 
                        propfast = "N/A           "
                    if b.GS: 
                        gs = "{:12}".format(b.GS)
                    else: 
                        gs = "N/A     "
                    data2 = "{:11}".format(b.EID) + "    " + propfast + "    " + gs + "{:12}".format(b.GA) + "{:12}".format(b.GB) + "{:12}".format(b.IDA) + "{:12}".format(b.IDB) + "{:12.2f}".format(joint.Diameter) + "  " + "N/A"
                    i.write(data2) 
                    i.write("\n")
            
            
            h301 = " ======="
            h302 = " RESULTS"
            h303 = " ======="

            h31 = " ----------  ----------------  ----------------------------------  ----------  ----------  ----------  ----------  ----------  ------------  --------------  --------------  --------------  --------------  --------------"
            h32 = "   A/B-ELEM      A/B-PROPERTY                    LOADCASE,SUBCASE  BypassFlux  BypassFlux  BypassFlux    Xbearing    Ybearing   PullThrough   TotalMomentum   TotalMomentum   TotalMomentum       BoltShear     BoltTension"
            h33 = " ----------  ----------------  ----------------------------------   Nxx(N/mm)   Nyy(N/mm)   Nxy(N/mm)    Force(N)     Force(N)     Force(N)      Flux_Mxx(N)     Flux_Myy(N)     Flux_Mxy(N)       Force(N)        Force(N)"
            h34 = " ----------  ----------------  ----------------------------------  ----------  ----------  ----------  ----------  ----------  ------------  --------------  --------------  --------------  --------------  --------------"

            i.write("\n")
            i.write(h301)
            i.write("\n")
            i.write(h302)
            i.write("\n")
            i.write(h303)
            i.write("\n")
            i.write(h31)
            i.write("\n")
            i.write(h32)
            i.write("\n")
            i.write(h33)
            i.write("\n")
            i.write(h34) 
            i.write("\n")

            for p in plateList: 
                plateElem = p.ElementList[0]
                if propDict[plateElem.Prop].PropertyType == "PSHELL": 
                    prop = "PSHEL" + "." + str(plateElem.Prop[0])
                else: 
                    prop = propDict[plateElem.Prop].PropertyType + "." + str(plateElem.Prop[0])
                boltElementsPlate = [l.ID for l in p.BoltElementList.values() if l]
                for j in lcList: 
                    lc = "SC" + str(j) + [l for l in self.Model.LoadCases if l.ID == j][0].Name
                    loadcase = "" 
                    for l,m in enumerate(lc): 
                        if l == 34: 
                            break 
                        loadcase = loadcase + m
                    while len(loadcase) < 34: 
                        loadcase = loadcase + " "
                    data3 = "{:11}".format(plateElem.ID) + "    " + prop + "  " + loadcase + "{:12.2f}".format(p.NxBypass[j]) + "{:12.2f}".format(p.NyBypass[j]) + "{:12.2f}".format(p.NxyBypass[j])
                    data3 = data3 + "{:12.2f}".format(p.BearingForce[j][0]) + "{:12.2f}".format(p.BearingForce[j][1]) + "{:14.2f}".format(p.BearingForce[j][2])
                    data3 = data3 + "{:16.2f}".format(p.MxTotal[j]) + "{:16.2f}".format(p.MyTotal[j]) + "{:16.2f}".format(p.MxyTotal[j])
                    data3 = data3 + "{:16.2f}".format(max([p.Bolt.ShearForce[j][l] for l in boltElementsPlate])) + "{:16.2f}".format(max([p.Bolt.AxialForce[j][l] for l in boltElementsPlate]))
                    i.write(data3) 
                    i.write("\n")

            h401 = " ============================="
            h402 = " TRANSLATIONAL_FASTENER_FORCES"
            h403 = " ============================="

            h41 = " ----------  ----------------  ----------------------------------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------"
            h42 = "   A/B-ELEM      A/B-PROPERTY                    LOADCASE,SUBCASE  ----------     CFAST_A  ----------  ----------     CFAST_B  ----------     CFAST_A     CFAST_B"
            h43 = " ----------  ----------------  ----------------------------------   Fxx(N/mm)   Fyy(N/mm)   Fzz(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fzz(N/mm)   Factor(-)   Factor(-)"
            h44 = " ----------  ----------------  ----------------------------------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------"

            i.write("\n")
            i.write(h401)
            i.write("\n")
            i.write(h402)
            i.write("\n")
            i.write(h403)
            i.write("\n")
            i.write(h41)
            i.write("\n")
            i.write(h42)
            i.write("\n")
            i.write(h43)
            i.write("\n")
            i.write(h44) 
            i.write("\n")

            for p in plateList: 
                plateElem = p.ElementList[0]
                if propDict[plateElem.Prop].PropertyType == "PSHELL": 
                    prop = "PSHEL" + "." + str(plateElem.Prop[0])
                else: 
                    prop = propDict[plateElem.Prop].PropertyType + "." + str(plateElem.Prop[0])
                for j in lcList: 
                    tf = p.TranslationalFastenerForces[j]
                    lc = "SC" + str(j) + [l for l in self.Model.LoadCases if l.ID == j][0].Name
                    loadcase = "" 
                    for l,m in enumerate(lc): 
                        if l == 34: 
                            break 
                        loadcase = loadcase + m
                    while len(loadcase) < 34: 
                        loadcase = loadcase + " "
                    data4 = "{:11}".format(plateElem.ID) + "    " + prop + "  " + loadcase 
                    data4 = data4 + "{:12.2f}".format(tf[0][0]) + "{:12.2f}".format(tf[0][1]) + "{:12.2f}".format(tf[0][2])
                    data4 = data4 + "{:12.2f}".format(tf[1][0]) + "{:12.2f}".format(tf[1][1]) + "{:12.2f}".format(tf[1][2]) 
                    data4 = data4 + "{:12}".format(p.CFASTFactor["A"]) + "{:12}".format(p.CFASTFactor["B"])
                    i.write(data4)
                    i.write("\n")

            h501 = " ==================================="
            h502 = " EXTRACTION_POINT_SHELL_FORCE_FLUXES"
            h503 = " ==================================="

            h51 = " ----------  ----------------  ----------------------------------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------"
            h52 = "   A/B-ELEM      A/B-PROPERTY                    LOADCASE,SUBCASE  ----------     POINT_1  ----------  ----------     POINT_2  ----------  ----------     POINT_3  ----------  ----------     POINT_4  ----------  ----------     POINT_5  ----------  ----------     POINT_6  ----------  ----------     POINT_7  ----------  ----------     POINT_8  ----------  ----------   AVG_NORTH  ----------  ----------   AVG_SOUTH  ----------  ----------    AVG_WEST  ----------  ----------    AVG_EAST  ----------  ----------      BYPASS  ----------"
            h53 = " ----------  ----------------  ----------------------------------   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)   Fxx(N/mm)   Fyy(N/mm)   Fxy(N/mm)"
            h54 = " ----------  ----------------  ----------------------------------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------"

            i.write("\n")
            i.write(h501)
            i.write("\n")
            i.write(h502)
            i.write("\n")
            i.write(h503)
            i.write("\n")
            i.write(h51)
            i.write("\n")
            i.write(h52)
            i.write("\n")
            i.write(h53)
            i.write("\n")
            i.write(h54) 
            i.write("\n")

            for p in plateList: 
                plateElem = p.ElementList[0]
                if propDict[plateElem.Prop].PropertyType == "PSHELL": 
                    prop = "PSHEL" + "." + str(plateElem.Prop[0])
                else: 
                    prop = propDict[plateElem.Prop].PropertyType + "." + str(plateElem.Prop[0])
                for j in lcList: 
                    lc = "SC" + str(j) + [l for l in self.LoadCases if l.ID == j][0].Name
                    loadcase = "" 
                    for l,m in enumerate(lc): 
                        if l == 34: 
                            break 
                        loadcase = loadcase + m
                    while len(loadcase) < 34: 
                        loadcase = loadcase + " "
                    bf = p.BoxFluxes[j]
                    bs = p.BypassSides[j]
                    data5 = "{:11}".format(plateElem.ID) + "    " + prop + "  " + loadcase 
                    data5 = data5 + "{:12.2f}".format(bf[1][0]) + "{:12.2f}".format(bf[1][1]) + "{:12.2f}".format(bf[1][2]) 
                    data5 = data5 + "{:12.2f}".format(bf[2][0]) + "{:12.2f}".format(bf[2][1]) + "{:12.2f}".format(bf[2][2])
                    data5 = data5 + "{:12.2f}".format(bf[3][0]) + "{:12.2f}".format(bf[3][1]) + "{:12.2f}".format(bf[3][2]) 
                    data5 = data5 + "{:12.2f}".format(bf[4][0]) + "{:12.2f}".format(bf[4][1]) + "{:12.2f}".format(bf[4][2]) 
                    data5 = data5 + "{:12.2f}".format(bf[5][0]) + "{:12.2f}".format(bf[5][1]) + "{:12.2f}".format(bf[5][2]) 
                    data5 = data5 + "{:12.2f}".format(bf[6][0]) + "{:12.2f}".format(bf[6][1]) + "{:12.2f}".format(bf[6][2]) 
                    data5 = data5 + "{:12.2f}".format(bf[7][0]) + "{:12.2f}".format(bf[7][1]) + "{:12.2f}".format(bf[7][2])
                    data5 = data5 + "{:12.2f}".format(bf[8][0]) + "{:12.2f}".format(bf[8][1]) + "{:12.2f}".format(bf[8][2]) 
                    data5 = data5 + "{:12.2f}".format(bs[0][0]) + "{:12.2f}".format(bs[1][0]) + "{:12.2f}".format(bs[2][0]) 
                    data5 = data5 + "{:12.2f}".format(bs[0][1]) + "{:12.2f}".format(bs[1][1]) + "{:12.2f}".format(bs[2][1]) 
                    data5 = data5 + "{:12.2f}".format(bs[0][2]) + "{:12.2f}".format(bs[1][2]) + "{:12.2f}".format(bs[2][2]) 
                    data5 = data5 + "{:12.2f}".format(bs[0][3]) + "{:12.2f}".format(bs[1][3]) + "{:12.2f}".format(bs[2][3]) 
                    data5 = data5 + "{:12.2f}".format(p.NxBypass[j]) + "{:12.2f}".format(p.NyBypass[j]) + "{:12.2f}".format(p.NxyBypass[j])
                    i.write(data5) 
                    i.write("\n")

            h601 = " ======================================"
            h602 = " EXTRACTION_POINT_SHELL_MOMENTUM_FLUXES"
            h603 = " ======================================"

            h61 = " ----------  ----------------  ----------------------------------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------"
            h62 = "   A/B-ELEM      A/B-PROPERTY                    LOADCASE,SUBCASE  ----------     POINT_1  ----------  ----------     POINT_2  ----------  ----------     POINT_3  ----------  ----------     POINT_4  ----------  ----------     POINT_5  ----------  ----------     POINT_6  ----------  ----------     POINT_7  ----------  ----------     POINT_8  ----------  ----------   AVG_NORTH  ----------  ----------   AVG_SOUTH  ----------  ----------    AVG_WEST  ----------  ----------    AVG_EAST  ----------  ----------      BYPASS  ----------"
            h63 = " ----------  ----------------  ----------------------------------       Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)      Mxx(N)      Myy(N)      Mxy(N)   "
            h64 = " ----------  ----------------  ----------------------------------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------"

            i.write("\n")
            i.write(h601)
            i.write("\n")
            i.write(h602)
            i.write("\n")
            i.write(h603)
            i.write("\n")
            i.write(h61)
            i.write("\n")
            i.write(h62)
            i.write("\n")
            i.write(h63)
            i.write("\n")
            i.write(h64) 
            i.write("\n")

            for p in plateList: 
                plateElem = p.ElementList[0]
                if propDict[plateElem.Prop].PropertyType == "PSHELL": 
                    prop = "PSHEL" + "." + str(plateElem.Prop[0])
                else: 
                    prop = propDict[plateElem.Prop].PropertyType + "." + str(plateElem.Prop[0])
                for j in lcList: 
                    lc = "SC" + str(j) + [l for l in self.LoadCases if l.ID == j][0].Name
                    loadcase = "" 
                    for l,m in enumerate(lc): 
                        if l == 34: 
                            break 
                        loadcase = loadcase + m
                    while len(loadcase) < 34: 
                        loadcase = loadcase + " "
                    bf = p.BoxFluxes[j]
                    bs = p.BypassSides[j]
                    data6 = "{:11}".format(plateElem.ID) + "    " + prop + "  " + loadcase 
                    data6 = data6 + "{:12.2f}".format(bf[1][3]) + "{:12.2f}".format(bf[1][4]) + "{:12.2f}".format(bf[1][5]) 
                    data6 = data6 + "{:12.2f}".format(bf[2][3]) + "{:12.2f}".format(bf[2][4]) + "{:12.2f}".format(bf[2][5])
                    data6 = data6 + "{:12.2f}".format(bf[3][3]) + "{:12.2f}".format(bf[3][4]) + "{:12.2f}".format(bf[3][5]) 
                    data6 = data6 + "{:12.2f}".format(bf[4][3]) + "{:12.2f}".format(bf[4][4]) + "{:12.2f}".format(bf[4][5]) 
                    data6 = data6 + "{:12.2f}".format(bf[5][3]) + "{:12.2f}".format(bf[5][4]) + "{:12.2f}".format(bf[5][5]) 
                    data6 = data6 + "{:12.2f}".format(bf[6][3]) + "{:12.2f}".format(bf[6][4]) + "{:12.2f}".format(bf[6][5]) 
                    data6 = data6 + "{:12.2f}".format(bf[7][3]) + "{:12.2f}".format(bf[7][4]) + "{:12.2f}".format(bf[7][5])
                    data6 = data6 + "{:12.2f}".format(bf[8][3]) + "{:12.2f}".format(bf[8][4]) + "{:12.2f}".format(bf[8][5]) 
                    data6 = data6 + "{:12.2f}".format(bs[3][0]) + "{:12.2f}".format(bs[4][0]) + "{:12.2f}".format(bs[5][0]) 
                    data6 = data6 + "{:12.2f}".format(bs[3][1]) + "{:12.2f}".format(bs[4][1]) + "{:12.2f}".format(bs[5][1]) 
                    data6 = data6 + "{:12.2f}".format(bs[3][2]) + "{:12.2f}".format(bs[4][2]) + "{:12.2f}".format(bs[5][2]) 
                    data6 = data6 + "{:12.2f}".format(bs[3][3]) + "{:12.2f}".format(bs[4][3]) + "{:12.2f}".format(bs[5][3]) 
                    data6 = data6 + "{:12.2f}".format(p.MxTotal[j]) + "{:12.2f}".format(p.MyTotal[j]) + "{:12.2f}".format(p.MxyTotal[j])
                    i.write(data6) 
                    i.write("\n")
    # ------------------------------------------------------------------------------------------------------------------
        
    # Method used to export the obtained PAG results as a HDF5 file ----------------------------------------------------
    def __export_pag_hdf5(self): 

        """
        Method used to export the PAG results to an HDF5 file. 
        """

        hdf5 = HDF5_NaxTo() 
        hdf5.FilePath = self.ExportLocation 
        hdf5.create_hdf5() 

        if self.GetFasteners: 
            plateList = self.GetFasteners.PlateList
        else: 
            plateList = [] 
            for i in self.JointsList: 
                for j in i.PlateList: 
                    plateList.append(j)

        for p in plateList: 
            for j in [lc.ID for lc in self.LoadCases]: 
                hdf5.write_dataset([self.__transform_results(j, p)])


    # Method used to obtain the main fastener analysis -----------------------------------------------------------------
    def get_analysis_joints(self): 

        """
        Method used to do the previous analysis and, optionally, export the results. 

        Calling example: 
            >>> loads.get_analysis_joints()
        """

        t1 = time()
        self.get_forces_joints()
        self.get_bypass_joints()
        N2PLog.Debug.D602(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------
    
    # Method used to do the entire analysis ----------------------------------------------------------------------------
    def calculate(self): 

        """
        Method used to do all the previous calculations and, optionally, export the results. 

        Calling example: 
            >>> loads.calculate()
        """
        
        t1 = time()
        self.update_elements()
        N = len(self.LoadCases)
        n = self.LoadCaseNumber
        for i in range(N//n): 
            loadCaseList = self.LoadCases[i*n: (i+1)*n]
            self.get_results_joints(loadCaseList) 
            self.get_analysis_joints()
        if (N//n)*n != N: 
            loadCaseList = self.LoadCases[n*(N//n):N]
            self.get_results_joints(loadCaseList) 
            self.get_analysis_joints()
        if self.ExportLocation: 
            self.export_results()
        N2PLog.Debug.D604(time(), t1)
    # ------------------------------------------------------------------------------------------------------------------
        
    # Method used to transform the results into arrays to be exported into an HDF5 -------------------------------------
    def __transform_results(self, loadcase: int, p: N2PPlate) -> DataEntry: 

        """
        Method used to transform the results obtained in the previous calculations into a DataEntry instance in odrer 
        to be exported to an HDF5 file. 

        Args: 
            loadcase: int -> load case ID 
            p: N2PPlate -> plate to be analysed 

        Returns: 
            dataEntry: DataEntry -> DataEntry instance to be written to an HDF5 file.
        """

        plateElem = p.ElementList[0]
        boltElementsPlate = [l.ID for l in p.BoltElementList.values() if l]
        partDict = self.Model._N2PModelContent__StrPartToID
        platePart = str((partDict[p.PartID[0]], p.PartID[0]))

        pi = "i" + str(self.ExportPrecision)
        pf = "f" + str(self.ExportPrecision)

        dataType = np.dtype([("ID_ENTITY", pi), ("BYPASS FLUX NXX", pf), ("BYPASS FLUX NYY", pf), ("BYPASS FLUX NXY", pf), ("X BEARING FORCE", pf), ("Y BEARING FORCE", pf), ("PULLTHROUGH FORCE", pf), 
                            ("TOTAL MOMENTUM FLUX MXX", pf), ("TOTAL MOMENTUM FLUX MYY", pf), ("TOTAL MOMENTUM FLUX MXY", pf), ("BOLT SHEAR", pf), ("BOLT TENSION", pf), 
                            ("FXX CFAST A", pf), ("FYY CFAST A", pf), ("FZZ CFAST A", pf), ("FXX CFAST B", pf), ("FYY CFAST B", pf), ("FZZ CFAST B", pf), 
                            ("FXX POINT 1", pf), ("FYY POINT 1", pf), ("FXY POINT 1", pf), ("MXX POINT 1", pf), ("MYY POINT 1", pf), ("MXY POINT 1", pf), 
                            ("FXX POINT 2", pf), ("FYY POINT 2", pf), ("FXY POINT 2", pf), ("MXX POINT 2", pf), ("MYY POINT 2", pf), ("MXY POINT 2", pf),
                            ("FXX POINT 3", pf), ("FYY POINT 3", pf), ("FXY POINT 3", pf), ("MXX POINT 3", pf), ("MYY POINT 3", pf), ("MXY POINT 3", pf), 
                            ("FXX POINT 4", pf), ("FYY POINT 4", pf), ("FXY POINT 4", pf), ("MXX POINT 4", pf), ("MYY POINT 4", pf), ("MXY POINT 4", pf),
                            ("FXX POINT 5", pf), ("FYY POINT 5", pf), ("FXY POINT 5", pf), ("MXX POINT 5", pf), ("MYY POINT 5", pf), ("MXY POINT 5", pf), 
                            ("FXX POINT 6", pf), ("FYY POINT 6", pf), ("FXY POINT 6", pf), ("MXX POINT 6", pf), ("MYY POINT 6", pf), ("MXY POINT 6", pf),
                            ("FXX POINT 7", pf), ("FYY POINT 7", pf), ("FXY POINT 7", pf), ("MXX POINT 7", pf), ("MYY POINT 7", pf), ("MXY POINT 7", pf), 
                            ("FXX POINT 8", pf), ("FYY POINT 8", pf), ("FXY POINT 8", pf), ("MXX POINT 8", pf), ("MYY POINT 8", pf), ("MXY POINT 8", pf),
                            ("FXX NORTH", pf), ("FYY NORTH", pf), ("FXY NORTH", pf), ("FXX SOUTH", pf), ("FYY SOUTH", pf), ("FXY SOUTH", pf),
                            ("FXX WEST", pf), ("FYY WEST", pf), ("FXY WEST", pf), ("FXX EAST", pf), ("FYY EAST", pf), ("FXY EAST", pf),
                            ("MXX NORTH", pf), ("MYY NORTH", pf), ("MXY NORTH", pf), ("MXX SOUTH", pf), ("MYY SOUTH", pf), ("MXY SOUTH", pf),
                            ("MXX WEST", pf), ("MYY WEST", pf), ("MXY WEST", pf), ("MXX EAST", pf), ("MYY EAST", pf), ("MXY EAST", pf)])

        shear = max([p.Bolt.ShearForce[loadcase][l] for l in boltElementsPlate]) 
        tension = max([p.Bolt.AxialForce[loadcase][l] for l in boltElementsPlate]) 
        tf = p.TranslationalFastenerForces[loadcase]
        bf = p.BoxFluxes[loadcase]
        bs = p.BypassSides[loadcase]
        resultList = np.array([(plateElem.ID, p.NxBypass[loadcase], p.NyBypass[loadcase], p.NxyBypass[loadcase], 
                                p.BearingForce[loadcase][0], p.BearingForce[loadcase][1], p.BearingForce[loadcase][2], 
                                p.MxTotal[loadcase], p.MyTotal[loadcase], p.MxyTotal[loadcase], shear, tension, tf[0][0], tf[0][1], tf[0][2], tf[1][0], tf[1][1], tf[1][2], 
                                bf[1][0], bf[1][1], bf[1][2], bf[1][3], bf[1][4], bf[1][5], bf[2][0], bf[2][1], bf[2][2], bf[2][3], bf[2][4], bf[2][5], 
                                bf[3][0], bf[3][1], bf[3][2], bf[3][3], bf[3][4], bf[3][5], bf[4][0], bf[4][1], bf[4][2], bf[4][3], bf[4][4], bf[4][5], 
                                bf[5][0], bf[5][1], bf[5][2], bf[5][3], bf[5][4], bf[5][5], bf[6][0], bf[6][1], bf[6][2], bf[6][3], bf[6][4], bf[6][5], 
                                bf[7][0], bf[7][1], bf[7][2], bf[7][3], bf[7][4], bf[7][5], bf[8][0], bf[8][1], bf[8][2], bf[8][3], bf[8][4], bf[8][5], 
                                bs[0][0], bs[1][0], bs[2][0], bs[3][0], bs[4][0], bs[5][0], bs[0][1], bs[1][1], bs[2][1], bs[3][1], bs[4][1], bs[5][1], 
                                bs[0][2], bs[1][2], bs[2][2], bs[3][2], bs[4][2], bs[5][2], bs[0][3], bs[1][3], bs[2][3], bs[3][3], bs[4][3], bs[5][3])], dataType) 

        dataEntry = DataEntry() 
        dataEntry.ResultsName = "FASTENER ANALYSIS"
        dataEntry.LoadCase = loadcase 
        dataEntry.Section = "None"
        dataEntry.Part = platePart 
        dataEntry.Data = resultList

        return dataEntry

    # Method used to create a progress bar during the calculations -----------------------------------------------------
    def __progress(self, count: int, total: int, suffix: str = "") -> None:

        """
        Method used to display a progress bar while the bypass loads are calculated. 

        Args:
            count: int -> current progress. 
            total: int -> total progress. 
            suffix: str -> optional suffix to be displayed alongside the progress bar. 
        """

        barLength = 60
        filledLength = int(round(barLength * count / total))
        percents = round(100.0 * count / total, 1)
        bar = "■" * filledLength + "□" * (barLength - filledLength)

        sys.stdout.write("\r[%s] %s%s ...%s" % (bar, percents, "%", suffix))
        sys.stdout.flush()
    # ------------------------------------------------------------------------------------------------------------------