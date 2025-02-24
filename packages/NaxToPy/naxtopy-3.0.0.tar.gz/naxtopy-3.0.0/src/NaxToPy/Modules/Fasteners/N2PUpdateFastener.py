import time
import csv
import numpy as np
from typing import Union
from NaxToPy.Core.Errors.N2PLog import N2PLog
from NaxToPy.Core.N2PModelContent import N2PModelContent, N2PProperty, N2PNastranInputData, N2PNode
from NaxToPy.Core.N2PModelContent import N2PElement


class N2PUpdateFastener:
    """
    This class stores information about fasteners and provides methods to update their stiffness and generate a new
    FEM Input File (.bdf, .fem, .dat, etc.) file with the updated data.

    Fastener information can be input either as a dictionary (for a single type of fastener) or as a list of dictionaries
    (for multiple types). Each dictionary must include at least the keys for diameter ["D"] and elastic modulus ["E"].
    Optional keys include head height ["h_head"], nut height ["h_nut"], Poisson ratio ["nu"], shear modulus ["G"],
    connection type ("bolt" or "rivet") ["connection_type"], shear type ("simple" or "double") ["shear_type"], and the
    beta value for Nelson method ["beta"].

    IDs of fasteners to be updated can be provided as either a single list (for a single type of fastener) or as a list
    of lists (for multiple types). If no list of IDs is provided, all fasteners in the model will be updated.

    When multiple types of fasteners are used, the order of the list of dictionaries must match the order of the list
    of ID lists to ensure proper mapping of variables.

    Supported methods for stiffness calculation include HUTH, TATE_ROSENFELD, SWIFT, BOEING, GRUMMAN, and NELSON.

    Example:
        Example 1:

        >>> import NaxToPy as n2p
        >>> model = n2p.load_model("model.dat")
        >>> info1 = {"D": 4.8,
        ...         "E": 110000}
        >>> info2 = {"D": 7.2,
        ...         "E": 70000,
        ...         "connection_type": "rivet",
        ...         "shear_type": "double"}
        >>> ele1 = [1000, 1001, 1002]
        >>> ele2 = [2000, 2001, 2002]
        >>> update1 = N2PUpdateFastener(model, [info1, info2], [ele1, ele2], "BOEING")
        >>> update1.calculate() # This will update the model in memory with the information of the object.
        >>> model.ModelInputData.rebuild_file() # With the model updated, the model is rewritten

        Example 2:

        >>> model = n2p.load_model("model.dat")
        >>> update2 = N2PUpdateFastener(model, {}) # Create the object without information
        >>> update2.IDList = [3000, 3001, 3002] # Add the information using it properties
        >>> update2.StiffnessMethod = "GRUMMAN"
        >>> update2.FastenerInformation = {3000: {"D": 4.8, "E": 70000, "connection_type": "rivet"},
        ...                                3001: {"D": 6.8, "E": 70000, "connection_type": "bolt"},
        ...                                3002: {"D": 7.2, "E": 70000, "shear_type": "double"}}
        >>> update2.calculate() # This will update the model in memory with the information of the object.
        >>> model.ModelInputData.rebuild_file() # With the model updated, the model is rewritten

    """

    def __init__(self, model: N2PModelContent, information: Union[dict, list], id_list: list = None,
                 stiffness_method: str = "HUTH"):
        self.__model = model
        self.__stiffness_method = stiffness_method

        # Extract information from the model
        tinit = time.time()
        self.__c_rivet, self.__p_rivet, self.__nodes_crivet = self.__info_extraction()
        N2PLog.Debug.D504(time.time(), tinit)

        # If the list of fasteners to be updated is not provided, all the fasteners of the model are considered and the
        # entry of the information is just a simple dictionary, so we overwrite it in order to have a list of length one,
        # hence matching both lengths (IDs list and information list)

        if id_list is None:
            id_list = [list(self.__c_rivet.keys())]
            if type(information) == dict:
                info_list = [information]
            else:
                raise TypeError("IF FASTENER LIST IS NOT PROVIDED, THE INFORMATION OF THE FASTENER MUST BE A DICTIONARY")

        elif isinstance(id_list[0], list) and type(information) == list:
            info_list = information

        else:
            if isinstance(id_list[0],int) and type(information)==dict: #Check if it is a single list or a list of lists
                id_list = [id_list]
                info_list = [information]

            else:
                raise TypeError("IF THERE IS A SINGLE TYPE OF FASTENER, THE FASTENERS MUST BE INTRODUCED AS A SINGLE LIST AND INFORMATION AS A DICTIONARY.")

        self.__id_list = id_list
        self.__info_list = info_list

        # Check that the info_list is equal to the number of lists
        if len(info_list) != len(id_list):
            raise ValueError("LENGTH OF FASTENER INFORMATION DICT MUST MATCH WITH LENGTH OF FASTENER LIST")

        # Complete information about fasteners with default values when not provided
        for info_fasteners in info_list:
            if 'connection_type' not in info_fasteners or not info_fasteners['connection_type']:
                info_fasteners['connection_type'] = "bolt"

            if 'shear_type' not in info_fasteners or not info_fasteners['shear_type']:
                info_fasteners['shear_type'] = "simple"

            if 'h_head' not in info_fasteners or not info_fasteners['h_head']:
                info_fasteners['h_head'] = 0

            if 'h_nut' not in info_fasteners or not info_fasteners['h_nut']:
                info_fasteners['h_nut'] = 0

            if 'nu' not in info_fasteners or not info_fasteners['nu']:
                info_fasteners['nu'] = 0.33

            if 'G' not in info_fasteners or not info_fasteners['G']:
                info_fasteners['G'] = info_fasteners['E'] / (2 * (1 + info_fasteners['nu']))

            if 'beta' not in info_fasteners or not info_fasteners['beta']:
                info_fasteners['beta'] = 0.5


        # Map each fastener with its properties
        self.__mapping_fastener_properties()

    def __mapping_fastener_properties(self):
        self.__fastener_properties = {fastener: prop for prop, IDs in zip(self.__info_list, self.__id_list) for fastener
                                      in IDs}

    def __read_bolts(self, path: str) -> dict:
        """
        Reads a csv containing the information about fasteners to be updated
        Args:
            path (str): path to BDF file
    
        Returns:
            dict: A dictionary where keys are fastener IDs (int) and values are lists containing
                  fastener information.
        """
        with open(path, "r") as file:
            content = csv.reader(file)
            return {int(row[0]): [_.strip() for _ in row] for row in content}

    def __axial_stiffness(self, fastener_ID: int, plate1_thickness: float, plate2_thickness: float) -> float:
        """
        Calculate the axial stiffness of a fastener, based on its elastic modulus, diameter, and the thicknesses of the
        plates it joins, along with optional parameters for the height of the head and nut.
    
        Args:
            fastener_ID (int): ID of the fastener to be updated.
            plate1_thickness (float): Thickness of the first plate.
            plate2_thickness (float): Thickness of the second plate.

        Returns:
            axial_stiffness (float): Axial stiffness of the fastener.
        """

        info_rivet = self.__fastener_properties[fastener_ID]
        head_height = info_rivet["h_head"]
        nut_height = info_rivet["h_nut"]
        E_f = info_rivet["E"]
        diameter = info_rivet["D"]

        # Effective length
        effective_length = plate1_thickness + plate2_thickness + head_height / 3 + nut_height / 3

        # Calculation of axial stiffness
        axial_stiffness = E_f * np.pi * (diameter ** 2) / (4 * effective_length)

        return axial_stiffness

    def __huth_shear(self, fastener_ID: int, E_1: float, t_1: float, plate1_property_type: str, E_2: float,
                     t_2: float, plate2_property_type: str) -> float:
        """
        Calculate the shear stiffness of a fastener by using Huth formula, based on its elastic modulus, diameter,
        the elastic moduli and thicknesses of the plates it joins, along with other parameters.
    
        Args:
            fastener_ID (int): ID of the fastener to be updated
            E_1 (float): Elastic modulus of plate 1 oriented in fastener coordinates system.
            t_1 (float): Thickness of plate 1.
            plate1_property_type (str): Type of property of plate 1 ("PSHELL" or "PCOMP").
            E_2 (float): Elastic modulus of plate 2 oriented in fastener coordinates system.
            t_2 (float): Thickness of plate 2.
            plate2_property_type (str): Type of property of plate 2 ("PSHELL" or "PCOMP").
    
        Returns:
            ksi (float): Shear stiffness of the fastener.
        """
        info_rivet = self.__fastener_properties[fastener_ID]
        connection_type = info_rivet["connection_type"]
        shear_type = info_rivet["shear_type"]
        E_f = info_rivet["E"]
        d = info_rivet["D"]

        # Calculate parameters based on connection type
        if connection_type == "bolt":
            a = 2 / 3
            b1 = 3 if (plate1_property_type == "PSHELL") else 4.2
            b2 = 3 if (plate2_property_type == "PSHELL") else 4.2
        elif connection_type == "rivet":
            a = 2 / 5
            b1 = 2.2 if (plate1_property_type == "PSHELL") else 4.2
            b2 = 2.2 if (plate2_property_type == "PSHELL") else 4.2

        # Determine shear type
        if shear_type == "simple":
            n = 1
        elif shear_type == "double":
            n = 2

        # Calculate Ec0
        Ec0 = ((t_1 + t_2) / (2 * d)) ** a
        # Calculate Ec1
        Ec1 = ((1 / (t_1 * E_1)) + (1 / (2 * t_1 * E_f))) * (b1 / n)
        # Calculate Ec2
        Ec2 = ((1 / (t_2 * n * E_2)) + (1 / (2 * t_2 * E_f * n))) * (b2 / n)
        # Calculate ksi
        ksi = 1 / ((Ec1 + Ec2) * Ec0)

        return ksi

    def __boeing_shear(self, fastener_ID: int, E_1: float, t_1: float, E_2: float, t_2: float) -> float:
        """
        Calculate the shear stiffness of a fastener by using Boeing formula, based on its elastic modulus, diameter and
        the elastic moduli and thicknesses of the plates it joins.
    
        Args:
            fastener_ID (int): ID of the fastener to be updated.
            E_1 (float): Elastic modulus of plate 1 oriented in fastener coordinates system.
            t_1 (float): Thickness of plate 1.
            E_2 (float): Elastic modulus of plate 2 oriented in fastener coordinates system.
            t_2 (float): Thickness of plate 2.

        Returns:
            ksi (float): Shear stiffness of the fastener.
        """
        info_rivet = self.__fastener_properties[fastener_ID]
        shear_type = info_rivet["shear_type"]
        E_f = info_rivet["E"]
        d = info_rivet["D"]

        if shear_type == "simple":
            numerator = 2
        elif shear_type == "double":
            numerator = 1.25

        # Calculate both flexibilities
        f1 = (numerator ** ((t_1 / d) ** 0.85) / t_1) * ((1 / E_1) + (3 / (8 * E_f)))
        f2 = (numerator ** ((t_2 / d) ** 0.85) / t_2) * ((1 / E_2) + (3 / (8 * E_f)))

        # Add flexibilities
        f = f1 + f2

        # Converts into stiffness
        ksi = 1 / f

        return ksi

    def __swift_shear(self, fastener_ID: int, E_1: float, t_1: float, E_2: float, t_2: float) -> float:
        """
        Calculate the shear stiffness of a fastener by using Swift (Douglas Aircraft) formula, based on its elastic
        modulus, diameter and the elastic moduli and thicknesses of the plates it joins.
    
        Args:
            fastener_ID (int): ID of the fastener to be updated
            E_1 (float): Elastic modulus of plate 1 oriented in fastener coordinates system.
            t_1 (float): Thickness of plate 1.
            E_2 (float): Elastic modulus of plate 2 oriented in fastener coordinates system.
            t_2 (float): Thickness of plate 2.

        Returns:
            ksi (float): Shear stiffness of the fastener.
        """

        info_rivet = self.__fastener_properties[fastener_ID]
        E_f = info_rivet["E"]
        d = info_rivet["D"]
        f = (5 / (d * E_f)) + (0.8 * (1 / (t_1 * E_1)) + (1 / (t_2 * E_2)))

        ksi = 1 / f
        return ksi

    def __tate_rosenfeld_shear(self, fastener_ID: int, E_1: float, t_1: float, E_2: float, t_2: float) -> float:

        """Calculate the shear stiffness of a fastener by using Tate & Rosenfeld formula, based on its elastic modulus,
        diameter and the elastic moduli and thicknesses of the plates it joins.
    
        Args:
            fastener_ID (int): ID of the fastener to be updated
            E_1 (float): Elastic modulus of plate 1 oriented in fastener coordinates system.
            t_1 (float): Thickness of plate 1.
            E_2 (float): Elastic modulus of plate 2 oriented in fastener coordinates system.
            t_2 (float): Thickness of plate 2.
    
        Returns:
            ksi (float): Shear stiffness of the fastener.
        """
        info_rivet = self.__fastener_properties[fastener_ID]
        E_f = info_rivet["E"]
        nu_f = info_rivet["nu"]
        d = info_rivet["D"]

        f = (1 / (E_f * t_1)) + (1 / (E_f * t_2)) + (1 / (E_1 * t_1)) + (1 / (E_2 * t_2)) + (
                32 / (9 * E_f * np.pi * d ** 2)) * (1 + nu_f) * (t_1 + t_2) + \
            (8 / (5 * E_f * np.pi * d ** 4)) * (t_1 ** 3 + 5 * (t_1 ** 2) * t_2 + 5 * (t_2 ** 2) * t_1 + t_2 ** 3)

        ksi = 1 / f

        return ksi

    def __grumman_shear(self, fastener_ID: int, E_1: float, t_1: float, E_2: float, t_2: float) -> float:
        """Calculate the shear stiffness of a fastener by using Grumman formula, based on its elastic modulus,
        diameter and the elastic moduli and thicknesses of the plates it joins.
    
        Args:
            fastener_ID (int): ID of the fastener to be updated
            E_1 (float): Elastic modulus of plate 1 oriented in fastener coordinates system.
            t_1 (float): Thickness of plate 1.
            E_2 (float): Elastic modulus of plate 2 oriented in fastener coordinates system.
            t_2 (float): Thickness of plate 2.

        Returns:
            ksi (float): Shear stiffness of the fastener.
        """
        info_rivet = self.__fastener_properties[fastener_ID]
        E_f = info_rivet["E"]
        d = info_rivet["D"]

        f = (((t_1 + t_2) ** 2) / (E_f * d ** 3)) + 3.72 * ((1 / (E_1 * t_1)) + ((1 / (E_2 * t_2))))

        ksi = 1 / f

        return ksi

    def __nelson_shear(self, fastener_ID: int, E_1: float, t_1: float, E_2: float, t_2: float, E_L1: float = None,
                       E_LT1: float = None, E_L2: float = None, E_LT2: float = None) -> float:
        """Calculate the shear stiffness of a fastener by using Grumman formula, based on its elastic modulus,
        diameter and the elastic moduli and thicknesses of the plates it joins.
    
        Args:
            fastener_ID (int): ID of the fastener to be updated
            E_1 (float): Elastic modulus of plate 1 oriented in fastener coordinates system.
            t_1 (float): Thickness of plate 1.
            E_2 (float): Elastic modulus of plate 2 oriented in fastener coordinates system.
            t_2 (float): Thickness of plate 2.

        Returns:
            ksi (float): Shear stiffness of the fastener.
        """
        info_rivet = self.__fastener_properties[fastener_ID]
        shear_type = info_rivet["shear_type"]
        E_f = info_rivet["E"]
        d = info_rivet["D"]
        G_f = info_rivet["G"]
        beta = info_rivet["beta"]

        if E_L1 is None:
            E_L1 = E_1
        if E_LT1 is None:
            E_LT1 = E_1
        if E_L2 is None:
            E_L2 = E_2
        if E_LT2 is None:
            E_LT2 = E_2

        E_eq1 = np.sqrt(E_L1 * E_LT1)
        E_eq2 = np.sqrt(E_L2 * E_LT2)
        A_f = np.pi * (d ** 2) / 4
        I_f = np.pi * (d ** 4) / 64

        if shear_type == "simple":
            f = (2 * (t_1 + t_2) / (3 * G_f * A_f)) + (2 * (t_1 + t_2) / (t_1 * t_2 * E_f)) + 1 / (t_1 * E_eq1) + (
                    1 + 3 * beta) / (t_2 * E_eq2)

        elif shear_type == "double":
            f = (8 * (t_2 ** 3) + 16 * (t_2 ** 2) * t_1 + 8 * (t_1 ** 2) * t_2 + t_1 ** 3) / (192 * E_f * I_f) + (
                    2 * (t_1 + t_2) / (3 * G_f * A_f)) + (2 * (t_1 + t_2) / (t_1 * t_2 * E_f)) + 2 / (
                        t_1 * E_eq1) + 1 / (t_2 * E_eq2)

        ksi = 1 / f
        return ksi

    def __info_extraction(self):
        """Extracts information from BDF files.

        This function loads data from BDF files and creates dictionaries
        containing information related to different types of fasteners and their nodes.

        Args:
            "None"

        Returns:
            tuple: A tuple containing:
                crivet (dict): Dictionary of CRIVET and CBUSH cards.
                privet (dict): Dictionary of PFAST and PBUSH cards.
                nodos_crivet (dict): Dictionary mapping CRIVET/CBUSH IDs to their corresponding node IDs.
                model (N2PModelContent): Model loaded from the BDF file.
        """
        # Record the initial time
        t_init = time.time()

        # Extract CRIVET and CBUSH cards
        crivet = {card.EID: card for card in self.__model.ModelInputData.get_cards_by_field(["CFAST", "CBUSH"])}

        # Extract PFAST and PBUSH cards
        privet = {pfast.PID: pfast for pfast in self.__model.ModelInputData.get_cards_by_field(["PFAST", "PBUSH"])}

        # Create a dictionary mapping CRIVET/CBUSH IDs to their corresponding node IDs
        nodos_crivet = {key: [self.__model.get_nodes((card.GA, 0)), self.__model.get_nodes((card.GB, 0))] for key, card in
                        crivet.items()}

        # Log information about the extraction time
        N2PLog.Debug.D500(time.time(), t_init)

        return crivet, privet, nodos_crivet

    def __elastic_calculus(self, property_obj: N2PProperty, vector2, theta, axis_mat_X) -> tuple[float, float]:
        """
        Calculate the elastic modulus of a shell or the equivalent elastic modulus of a laminate in the
        fastener Y and Z directions.
    
        Args:
            property_obj (N2PProperty): Property object.
            vector2 (ndarray (3,)): Vector Y in the fastener axes.
            theta (float): Angle between material and G1-G2.
            axis_mat_X (ndarray (3,)): X vector of the material of the two elements to be joined.
    
        Returns:
            Ez (float): Young's modulus of the element in the Z direction of the fastener.
            Ey (float): Young's modulus of the element in the Y direction of the fastener.
        """

        t_init = time.time()
        material_dict = self.__model.MaterialDict

        # Calculate plate properties if defined as PSHELL
        if property_obj.PropertyType == "PSHELL":
            material = material_dict[property_obj.MatMemID]

            if material.MatType == "MAT1":
                E1 = material.Young
                E2 = material.Young
                nu = material.Poisson
                G = material.Shear if material.Shear != 0 else E1 / (2 * (1 + nu))

            elif material.MatType == "UNDEF":
                q11 = material.QualitiesDict.get("G11")
                q22 = material.QualitiesDict.get("G22")
                q12 = material.QualitiesDict.get("G12")
                q66 = material.QualitiesDict.get("G33")
                E1, E2, nu, G = self.__q_to_engineering(q11, q22, q12, q66)

            elif material.MatType == "MAT8":
                E1 = material.YoungX
                E2 = material.YoungY
                nu = material.PoissonXY
                G = material.ShearXY if material.ShearXY != 0 else E1 / (2 * (1 + nu))

            else:
                N2PLog.Error.E311(property_obj.ID)

        # Calculate equivalent properties if the plate is a PCOMP
        elif property_obj.PropertyType == "PCOMP":
            equivalent_Q = property_obj.EqQMatrix

            E1, E2, nu, G = self.__q_to_engineering(equivalent_Q[0][0], equivalent_Q[1][1], equivalent_Q[0][1],
                                                    equivalent_Q[2][2])

        # Orient properties in the fastener axes.
        # Calculation of the angle between G1-G2 of the element (material_axis_X) and the "Y" axis of the fastener.
        alpha = self.__angle_between_vectors(vector2, axis_mat_X)

        # Angle between the material and the fastener x-axis. Theta is the angle between the material and G1-G2.
        angle = alpha - theta

        s = np.sin(np.radians(angle))
        c = np.cos(np.radians(angle))


        # Orient element properties in the fastener axes.
        Ey = (1 / E1 * c ** 4 +
              (1 / G - 2 * nu / E1) * s ** 2 * c ** 2 +
              1 / E2 * s ** 4) ** -1

        Ez = (1 / E1 * s ** 4 +
              (1 / G - 2 * nu / E1) * s ** 2 * c ** 2 +
              1 / E2 * c ** 4) ** -1

        N2PLog.Debug.D501(time.time(), t_init)
        return Ey, Ez

    def __angle_between_vectors(self, vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        cos_angle = dot_product / norm_product
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))  # Use clip to avoid numerical errors
        return np.degrees(angle)

    def __q_to_engineering(self, q11, q22, q12, q66) -> tuple[float, float, float, float]:
        """Calculate the engineering constants (E1, E2, nu, G) from the material matrix.
    
            Args:
                q11 (float): Modulus in the 1 direction.
                q22 (float): Modulus in the 2 direction.
                q12 (float): Modulus in the 1-2 plane.
                q66 (float): Shear modulus in the 1-2 plane.
    
            Returns:
                tuple[float, float, float, float]: Engineering constants (E1, E2, nu, G).
            """
        Q = np.array([[q11, q12, 0],
                      [q12, q22, 0],
                      [0, 0, q66]])

        S = np.linalg.inv(Q)

        e1 = 1 / S[0, 0]
        e2 = 1 / S[1, 1]
        nu12 = -S[0, 1] * e1
        g = 1 / S[2, 2]

        return e1, e2, nu12, g

    def __CBUSH_connected_RBE3(self, card: N2PNastranInputData, nodoA: N2PNode, nodoB: N2PNode):
        """
        Returns the input that will be used to compute the elastic modulus of a fastener.
        This function is developed for the specific case of a connector CBUSH connected to a RBE3
    
        Args:
            card (N2PModelContent): Card associated to the fastener
            nodoA (N2PModelContent): First node at which the fastener is connected
            nodoB (N2PModelContent): Second node at which the fastener is connected
    
        Returns:
            propA, propB (N2PComp): Properties of the components
            vector2 (ndarray (3,)): Y axis in rivet coordinates
            thetaA, thetaB (float): Orientation of the material of the two elements to be joined
            axis_matA_X, axis_matB_X (ndarray (3,)): X axis of the material of the two elements to be joined
        """

        # Define vector 0 based on GA-G0 or its components
        if card.X2 is None:
            nodo0 = self.__model.NodesDict[(card.G0, 0)]
            vector0 = np.array([nodo0.X - nodoA.X,
                                nodo0.Y - nodoA.Y,
                                nodo0.Z - nodoA.Z])
        else:
            vector0 = np.array([card.X1, card.X2, card.X3])

        vector0 /= np.linalg.norm(vector0)

        # Define fastener orientation vectors
        vector1 = np.array([nodoB.X - nodoA.X,
                            nodoB.Y - nodoA.Y,
                            nodoB.Z - nodoA.Z])
        vector1 /= np.linalg.norm(vector1)

        vector3 = np.cross(vector1, vector0)
        vector2 = np.cross(vector3, vector1)

        # Find element connected to RBE3 for both nodes A and B
        rbe3A = nodoA.Connectivity[0]
        rbe3B = nodoB.Connectivity[0]

        ######### METHODOLOGY
        # We need to find out to which element the RBE3 is connected. To do this, we need to find out to which nodes it
        # is connected, and then find out to which elements those nodes are connected. The element we are looking for
        # will be linked to those nodes. However, there is one node that we do not need to consider, and that is the
        # reference node. To do this:
        # We go through all the nodes in rbe3A.FreeNodes except rbe3A.RefGrid, and for each of them, we find their
        # connectivity, obtaining a set of elements for each node of the RBE3. Finally, we apply the intersection of the
        # sets, that is, we keep a set containing the items repeated in all the sets, which is the element we
        # are looking for.

        t_a = time.time()

        componentA = set.intersection(*[{elem for elem in node.Connectivity
                                         if isinstance(elem, N2PElement)} for node in
                                        self.__model.get_nodes(
                                            [node for node in rbe3A.FreeNodes if node != rbe3A.RefGrid])]).pop()

        componentB = set.intersection(*[{elem for elem in node.Connectivity
                                         if isinstance(elem, N2PElement)} for node in
                                        self.__model.get_nodes(
                                            [node for node in rbe3B.FreeNodes if node != rbe3B.RefGrid])]).pop()

        N2PLog.Debug.D502(time.time(), t_a)

        # Extract axes and orientation angles
        thetaA = componentA.AngleMat
        axis_matA_X = (componentA.Nodes[1].X - componentA.Nodes[0].X,
                       componentA.Nodes[1].Y - componentA.Nodes[0].Y,
                       componentA.Nodes[1].Z - componentA.Nodes[0].Z)

        thetaB = componentB.AngleMat
        axis_matB_X = (componentB.Nodes[1].X - componentB.Nodes[0].X,
                       componentB.Nodes[1].Y - componentB.Nodes[0].Y,
                       componentB.Nodes[1].Z - componentB.Nodes[0].Z)

        # Retrieve properties of the components
        propA = self.__model.PropertyDict.get(componentA.Prop)
        propB = self.__model.PropertyDict.get(componentB.Prop)

        return propA, propB, vector2, thetaA, thetaB, axis_matA_X, axis_matB_X

    def __CBUSH_connected_nodes(self, card: N2PNastranInputData, nodoA: N2PNode, nodoB: N2PNode):
        """
        Returns the input that will be used to compute the elastic modulus of a fastener.
        This function is developed for the specific case of a connector CBUSH connected to two nodes
    
        Args:
            card (N2PModelContent): Card associated to the fastener
            nodoA (N2PModelContent): First node at which the fastener is connected
            nodoB (N2PModelContent): Second node at which the fastener is connected
    
        Returns:
            propA, propB (N2PComp): Properties of the components
            vector2 (ndarray (3,)): Y axis in rivet coordinates
            thetaA, thetaB (float): Orientation of the material of the two elements to be joined
            axis_matA_X, axis_matB_X (ndarray (3,)): X axis of the material of the two elements to be joined
        """

        # Define vector 0 based on GA-G0 or its components
        if card.X2 is None:
            nodo0 = self.__model.NodesDict[(card.G0, 0)]
            vector0 = np.array([nodo0.X - nodoA.X,
                                nodo0.Y - nodoA.Y,
                                nodo0.Z - nodoA.Z])
        else:
            vector0 = np.array([card.X1, card.X2, card.X3])

        vector0 /= np.linalg.norm(vector0)

        # Define fastener orientation vectors
        vector1 = np.array([nodoB.X - nodoA.X,
                            nodoB.Y - nodoA.Y,
                            nodoB.Z - nodoA.Z])
        vector1 /= np.linalg.norm(vector1)

        vector3 = np.cross(vector1, vector0)
        vector2 = np.cross(vector3, vector1)

        # Extract properties and axes of the connected components
        componentA = nodoA.Connectivity[0]
        thetaA = componentA.AngleMat
        axis_matA_X = (componentA.Nodes[1].X - componentA.Nodes[0].X,
                       componentA.Nodes[1].Y - componentA.Nodes[0].Y,
                       componentA.Nodes[1].Z - componentA.Nodes[0].Z)

        componentB = nodoB.Connectivity[0]
        thetaB = componentB.AngleMat
        axis_matB_X = (componentB.Nodes[1].X - componentB.Nodes[0].X,
                       componentB.Nodes[1].Y - componentB.Nodes[0].Y,
                       componentB.Nodes[1].Z - componentB.Nodes[0].Z)

        # Retrieve properties of the components
        propA = self.__model.PropertyDict.get(componentA.Prop)
        propB = self.__model.PropertyDict.get(componentB.Prop)

        return propA, propB, vector2, thetaA, thetaB, axis_matA_X, axis_matB_X

    def __CFAST_connected_ELEM(self, card: N2PNastranInputData, nodoA: N2PNode, nodoB: N2PNode):
        """
        Returns the input that will be used to compute the elastic modulus of a fastener.
        This function is developed for the specific case of a connector CFAST connected by ELEM type.
    
        Args:
            card (N2PModelContent): Card associated to the fastener.
            nodoA (N2PModelContent): First node at which the fastener is connected.
            nodoB (N2PModelContent): Second node at which the fastener is connected.
    
        Returns:
            propA, propB (N2PComp): Properties of the components.
            vector2 (ndarray (3,)): Y axis in rivet coordinates.
            thetaA, thetaB (float): Orientation of the material of the two elements to be joined.
            axis_matA_X, axis_matB_X (ndarray (3,)): X axis of the material of the two elements to be joined.
        """
        # Para sacar los ejes del remache, necesitamos acceder a la tarjeta PFAST
        pfast_ID = card.PID
        pfast_card = self.__p_rivet[pfast_ID]

        # Procedures followed as detailed in MSC Nastran 2021 Quick Reference Guide --> Bulk Data Entries --> PFAST)

        if pfast_card.MCID == -1:
            # Calculate vectors
            vector1 = np.array([nodoB.X - nodoA.X, nodoB.Y - nodoA.Y, nodoB.Z - nodoA.Z])
            vector1 /= np.linalg.norm(vector1)

            indice_min = np.argmin(np.abs(vector1))
            aux_vector = np.zeros(3)
            aux_vector[indice_min] = 1
            vector2 = aux_vector - (np.dot(aux_vector, vector1) / np.dot(vector1, vector1)) * vector1
            vector2 /= np.linalg.norm(vector2)
            #vector3 = np.cross(vector1, vector2)


        else:
            raise NotImplementedError("CODE IS ONLY PREPARED FOR CARD PFAST WHOSE MCID = -1")

        # Element A
        componentA = self.__model.ElementsDict[(card.IDA, 0)]
        axisA = componentA.ElemSystemArray
        elem_Z_A = np.array(axisA[6:])
        thetaA = componentA.AngleMat
        axis_matA_X = (componentA.Nodes[1].X - componentA.Nodes[0].X,
                       componentA.Nodes[1].Y - componentA.Nodes[0].Y,
                       componentA.Nodes[1].Z - componentA.Nodes[0].Z)

        # Element B
        componentB = self.__model.ElementsDict[(card.IDB, 0)]
        axisB = componentB.ElemSystemArray
        elem_Z_B = np.array(axisB[6:])
        thetaB = componentB.AngleMat
        axis_matB_X = (componentB.Nodes[1].X - componentB.Nodes[0].X,
                       componentB.Nodes[1].Y - componentB.Nodes[0].Y,
                       componentB.Nodes[1].Z - componentB.Nodes[0].Z)

        # Retrieve properties
        propA = self.__model.PropertyDict.get(componentA.Prop)
        propB = self.__model.PropertyDict.get(componentB.Prop)

        return propA, propB, vector2, thetaA, thetaB, axis_matA_X, axis_matB_X

    def __update_fastener(self, fastener_ID: int) -> None:
        """
        Returns the input that will be used to compute the elastic modulus of a fastener.
        This function is developed for the specific case of a connector CFAST connected by ELEM type.
    
        Args:
            fastener_ID (int): ID of fastener to be updated.

        Returns:
            None
        """

        tinit = time.time()

        # Check that the shear type and the connection type are valid
        if self.__fastener_properties[fastener_ID]['shear_type'] not in ["simple", "double"]:
            raise ValueError(f"{self.__fastener_properties['shear_type']} IS NOT A VALID SHEAR TYPE")

        if self.__fastener_properties[fastener_ID]['connection_type'] not in ["bolt", "rivet"]:
            raise ValueError(f"{self.__fastener_properties['connection_type']} IS NOT A SUPPORTED CONNECTION TYPE")

        # Retrieve the card from the dictionary
        card = self.__c_rivet[fastener_ID]

        # Joint model (CBUSH/CFAST)
        kind_union = card.CharName

        info_rivet = self.__fastener_properties[fastener_ID]

        # Nodes of the rivet
        nodoA, nodoB = self.__nodes_crivet[fastener_ID]

        # Types:
        if kind_union == "CBUSH":
            # There are two cases associated to CBUSH: connected to RBE3 and connected to two nodes
            # CBUSH connected to RBE3
            if hasattr(nodoA.Connectivity[0], 'TypeConnector') and nodoA.Connectivity[0].TypeConnector == "RBE3" and \
                    nodoB.Connectivity[0].TypeConnector == "RBE3":
                propA, propB, vector2, thetaA, thetaB, axis_matA_X, axis_matB_X = self.__CBUSH_connected_RBE3(card, nodoA, nodoB)

            # CBUSH connected to nodes
            elif hasattr(nodoA.Connectivity[0], 'TypeElement'):
                propA, propB, vector2, thetaA, thetaB, axis_matA_X, axis_matB_X = self.__CBUSH_connected_nodes(card, nodoA, nodoB)

            else:
                raise NotImplementedError("CBUSH FOR THIS TYPE OF CONNECTOR IS NOT SUPPORTED")

        elif kind_union == "CFAST":
            # There are two type of CFAST: connected by elements (ELEM) or connected by properties (PROP)
            # Connected by ELEM
            if card.TYPE == 'ELEM':
                propA, propB, vector2, thetaA, thetaB, axis_matA_X, axis_matB_X = self.__CFAST_connected_ELEM(card, nodoA, nodoB)

            # Connected by PROP
            elif card.TYPE == 'PROP':
                raise NotImplementedError("THE JOINT CFAST CONNECTED BY PROP IS NOT SUPPORTED")
        # Any other type of joint will raise an error
        else:
            raise NotImplementedError("THE TYPE OF JOINT SELECTED IS NOT SUPPORTED")

        # Compute the thickness of the components
        thickness = []
        for comp in [propA, propB]:
            if comp.PropertyType == "PSHELL":
                thickness.append(comp.Thickness)
            elif comp.PropertyType == "PCOMP":
                thickness.append(sum(comp.Thickness))
        thicknA, thicknB = thickness

        # Compute the elastic modulus in the direction of the rivet
        ExA, EyA = self.__elastic_calculus(propA, vector2, thetaA, axis_matA_X)
        ExB, EyB = self.__elastic_calculus(propB, vector2, thetaB, axis_matB_X)

        # Compute the axial stiffness
        axial = self.__axial_stiffness(fastener_ID,thicknA, thicknB)

        # In order to compute the shear stiffness, we have to consider the method

        if self.__stiffness_method == "HUTH":
            shear_Y = self.__huth_shear(fastener_ID, ExA, thicknA, propA.PropertyType, ExB, thicknB, propB.PropertyType)
            shear_Z = self.__huth_shear(fastener_ID, EyA, thicknA, propA.PropertyType, EyB, thicknB, propB.PropertyType)

        elif self.__stiffness_method == "TATE_ROSENFELD":
            nu_f = info_rivet["nu"]
            shear_Y = self.__tate_rosenfeld_shear(fastener_ID, ExA, thicknA, ExB, thicknB)
            shear_Z = self.__tate_rosenfeld_shear(fastener_ID, EyA, thicknA, EyB, thicknB)

        elif self.__stiffness_method == "BOEING":
            shear_Y = self.__boeing_shear(fastener_ID, ExA, thicknA, ExB, thicknB)
            shear_Z = self.__boeing_shear(fastener_ID, EyA, thicknA, EyB, thicknB)

        elif self.__stiffness_method == "GRUMMAN":
            shear_Y = self.__grumman_shear(fastener_ID, ExA, thicknA, ExB, thicknB)
            shear_Z = self.__grumman_shear(fastener_ID, EyA, thicknA, EyB, thicknB)

        elif self.__stiffness_method == "SWIFT":
            shear_Y = self.__swift_shear(fastener_ID, ExA, thicknA, ExB, thicknB)
            shear_Z = self.__swift_shear(fastener_ID, EyA, thicknA, EyB, thicknB)

        elif self.__stiffness_method == "NELSON":
            shear_Y = self.__nelson_shear(fastener_ID, ExA, thicknA, ExB, thicknB)
            shear_Z = self.__nelson_shear(fastener_ID, EyA, thicknA, EyB, thicknB)

        else:
            raise NotImplementedError(
                f"{self.__stiffness_method} IS NOT A SUPPORTED CALCULUS METHOD FOR FASTENER SHEAR STIFFNESS")

        # Update stiffness depending on the type of joint
        prop_card = self.__p_rivet[card.PID]
        if prop_card.CharName == "PBUSH":
            prop_card.K1 = axial
            prop_card.K2 = shear_Y
            prop_card.K3 = shear_Z

        elif prop_card.CharName == "PFAST":
            prop_card.KT1 = axial
            prop_card.KT2 = shear_Y
            prop_card.KT3 = shear_Z

        N2PLog.Debug.D503(time.time(), tinit)

    # --------------------------------Main function updating the PFAST and PBUSH cards --------------------------------------

    def calculate(self) -> None:
        """Update properties of fasteners in a model.
    
        Reads a model from a BDF file and updates the properties of PFAST and PBUSH elements.
        If a list of fastener IDs is provided, it updates the properties of those elements.
    
        Args:
            "None"
        Returns:
            "None"
        """

        for fastener_ID in self.__fastener_properties.keys():
            self.__update_fastener(fastener_ID)
            print(f"Fastener updated: {fastener_ID}")

    def write_bdf(self, out_folder: str):
        self.__model.ModelInputData.rebuild_file(out_folder)

    @property
    def StiffnessMethod(self) -> str:
        """
        Returns the name of the method used to calculate the fastener stiffness
        """
        return self.__stiffness_method

    @StiffnessMethod.setter
    def StiffnessMethod(self,stiffness_method: str) -> None:
        """
        Set the method used to calculate the fastener stiffness
        """
        self.__stiffness_method = stiffness_method

    @property
    def FastenerInformation(self) -> dict:
        """
        Returns the dictionary mapping each fastener with its properties
        """
        return self.__fastener_properties

    @FastenerInformation.setter
    def FastenerInformation(self, fastener_properties: dict) -> None:
        """
        Set the dictionary mapping each fastener with its properties
        """
        self.__fastener_properties = fastener_properties\

    @property
    def IDList(self) -> Union[list,list[list]]:
        """
        Returns the list of fasteners to be updated
        """
        return self.__id_list

    @IDList.setter
    def IDList(self, id_list: Union[list,list[list]]) -> None:
        """
        Set the list of fasteners to be updated
        """
        self.__id_list = id_list
        self.__mapping_fastener_properties()

    @property
    def InfoDicts(self) -> Union[dict,list[dict]]:
        """
        Returns the list of dictionaries containing the fastener information
        """
        if len(self.__info_list) == 1:
            return self.__info_list[0]
        else:
            return self.__info_list

    @InfoDicts.setter
    def InfoDicts(self, info_dict: Union[list,list[list]]) -> None:
        """
        Set the list of dictionaries containing the fastener information
        """
        if len(info_dict) == 1:
            self.__info_list = [info_dict]
        else:
            self.__info_list = info_dict



