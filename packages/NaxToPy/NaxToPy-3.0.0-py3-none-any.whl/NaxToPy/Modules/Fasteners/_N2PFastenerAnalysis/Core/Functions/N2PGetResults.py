from NaxToPy.Core.N2PModelContent import N2PModelContent 
from NaxToPy.Core.Classes.N2PElement import N2PElement
from NaxToPy.Core.Classes.N2PLoadCase import N2PLoadCase
from NaxToPy import N2PLog

# Method used to obtain the results dictionary -------------------------------------------------------------------------
def get_results(model: N2PModelContent, loadcase: list[N2PLoadCase], cornerData: bool = True, jointType: str = "CFAST"): 

    """
    Method used to obtain a dictionary of dictionaries of all important results that have to be saved in memory. The 
    dictionary is in the form {Load Case ID: {'FX1D': [...], 'FY1D': [...], ...}}. In other words, the dictionary is 
    made up of several dictionaries whose keys are the load cases IDs. These inner dictionaries' keys are: 
        'FX1D', 'FY1D', 'FZ1D', 'FX', 'FY', 'FXY', 'MX', 'MY', 'MXY', 
        'FX1D CORNER', 'FY1D CORNER', 'FZ1D CORNER', 'FX CORNER', 'FY CORNER', 'FXY CORNER', 
        'MX CORNER', 'MY CORNER', 'MXY CORNER', 
        'cornerData', 'Name'

    Args: 
        model: N2PModelContent -> compulsory input.
        loadcase: list[N2PLoadCase] = None -> load case(s) to be studied. 
        cornerData: bool = False -> boolean which shows whether the corner data is to be used or not.
        jointType: str = "CFAST" -> string which shows what is the joint's type. 

    Returns: 
        resultsDict: dict 
        brokenLC: list[N2PLoadCase] -> list of broken load cases. 

    If results have been obtained in the corner, it is recommended to use them, as this data will be more accurate and 
    the computed bypass loads will be more precise, but the process is slower. Therefore, when cornerData is set to 
    False, a warning will appear. For optimization reasons, if corner data is not selected, the corresponding elements 
    in the results dictionary will be filled with None and the results will only be obtained in the centroid. 

    It is important to note that, if cornerData is set to False and there are actually results in the corner, the 
    program should function correctly (just not taking into account this data). Similarly, if cornerData is set to True 
    but there is no corner data in the results, the dictionaries corresponding to the corner forces will be filled with 
    nan. This is not problematic (it just takes longer), but it could be bad if this data is used for the bypass 
    calculations for obvious reasons. 

    Calling example: 
        >>> myResults = get_results(model1, model1.LoadCases[0:10])
    """

    # Warning if Corner data is not selected
    if not cornerData: 
        N2PLog.Warning.W511()

    resultsDict = {}
    brokenLC = []

    solver = model.Solver 
    # The results and components template will be diferent depending on whether the solver is Nastran or Optistruct 
    # Note: depending on whether the joint is a CFAST, CWELD or CBUSH, the template will also be different. For 
    # Nastran 'CFAST' and 'CBUSH' everything works fine. For Nastran 'CWELD' everything works (perhaps not fine, 
    # but it works) and for Optistruct everything, it hasn't been tried yet. 
    if solver == "InputFileNastran" and jointType != "CWELD": 
        results = ["FORCES", "FORCES",  "FORCES"]
        components = ["FX", "FY", "FZ", "FX", "FY", "FXY", "MX", "MY", "MXY"] 
    elif solver == "InputFileNastran": 
        results = ["FORCES(CWELD)", "FORCES(CWELD)",  "FORCES(CWELD)"]
        components = ["FX", "FY", "FZ", "FX", "FY", "Mz-A", "MX", "My-A", "Mz-A"] 
    elif solver == "InputFileAbaqus":
        results = ["FORCES (1D)", "FORCES", "MOMENTS"]
        components = ["X", "Y", "Z", "XX", "YY", "XY", "XX", "YY", "XY"]
    else:
        N2PLog.Critical.C500()
        return 0

    lclist = [(i, i.ActiveN2PIncrement) for i in loadcase]

    fx1D = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[0], components[0]).items()}
    fy1D = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[0], components[1]).items()}
    fz1D = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[0], components[2]).items()}
    fx = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[1], components[3]).items()}
    fy = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[1], components[4]).items()}
    fxy = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[1], components[5]).items()}
    mx = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[2], components[6]).items()}
    my = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[2], components[7]).items()}
    mxy = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[2], components[8]).items()}

    model.clear_results_memory() 
    lcid = [i.ID for i in loadcase]

    if cornerData: 
        # If cornerData = True, results are also obtained using this corner data 
        fxC = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[1], components[3], cornerData = True, aveNodes = 0).items()}
        fyC = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[1], components[4], cornerData = True, aveNodes = 0).items()}
        fxyC = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[1], components[5], cornerData = True, aveNodes = 0).items()}
        mxC = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[2], components[6], cornerData = True, aveNodes = 0).items()}
        myC = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[2], components[7], cornerData = True, aveNodes = 0).items()}
        mxyC = {i[0]: j for i,j in model.get_result_by_LCs_Incr(lclist, results[2], components[8], cornerData = True, aveNodes = 0).items()}

        # Correction for CTRIA elements: 
        # When obtaining results from trias, only results in the centroid are supported. Therefore, when the option 
        # of Corner Data is selected, the results of the tria obtained in the centroid are translated to the 3 
        # nodes which form it.
        elementNodal = model.elementnodal() 
        unsewElementsID = [elementNodal.get(i)[2] for i in elementNodal.keys()]
        unsewElementsPartID = [elementNodal.get(i)[0] for i in elementNodal.keys()]
        unsewElements = [model.get_elements((unsewElementsID[i], unsewElementsPartID[i])) for i in range(len(unsewElementsID))]

        for i, j in enumerate(unsewElements): 
            if isinstance(j, N2PElement) and j.TypeElement == "CTRIA3":
                for k in lcid: 
                    fxC[k][i] = fx[k][j.InternalID]
                    fyC[k][i] = fy[k][j.InternalID]
                    fxyC[k][i] = fxy[k][j.InternalID]
                    mxC[k][i] = mx[k][j.InternalID]
                    myC[k][i] = my[k][j.InternalID]
                    mxyC[k][i] = mxy[k][j.InternalID]

    brokenLC = [] 
    for i in loadcase: 
        isBroken = False 
        fx1Di = fx1D.get(i.ID) 
        fy1Di = fy1D.get(i.ID) 
        fz1Di = fz1D.get(i.ID) 
        fxi = fx.get(i.ID) 
        fyi = fy.get(i.ID) 
        fxyi= fxy.get(i.ID) 
        mxi = mx.get(i.ID) 
        myi = my.get(i.ID) 
        mxyi = mxy.get(i.ID) 
        if cornerData: 
            fxCi = fxC.get(i.ID)
            fyCi = fyC.get(i.ID)
            fxyCi = fxyC.get(i.ID)
            mxCi = mxC.get(i.ID)
            myCi = myC.get(i.ID)
            mxyCi = mxyC.get(i.ID)
        else: 
            fxCi = None 
            fyCi = None 
            fxyCi = None 
            mxCi = None 
            myCi = None 
            mxyCi = None 
        if (fx1Di is None or fy1Di is None or fz1Di is None or 
            fxi is None or fyi is None or fxyi is None or 
            mxi is None or myi is None or mxyi is None): 
            isBroken = True 
            N2PLog.Warning.W521(i.ID) 
        if isBroken: 
            brokenLC.append(i)
        else: 
            resultsDict[i.ID] = {"FX1D": fx1Di, "FY1D": fy1Di, "FZ1D": fz1Di, 
                                "FX": fxi, "FY": fyi, "FXY": fxyi, 
                                "MX": mxi, "MY": myi, "MXY": mxyi, 
                                "FX CORNER": fxCi, "FY CORNER": fyCi, "FXY CORNER": fxyCi,
                                "MX CORNER": mxCi, "MY CORNER": myCi, "MXY CORNER": mxyCi,
                                "cornerData": cornerData, "Name": i.Name}
    return resultsDict, brokenLC 
# ----------------------------------------------------------------------------------------------------------------------