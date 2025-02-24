from NaxToPy.Core import N2PModelContent
from NaxToPy.Modules.Fasteners.Joints.N2PJoint import N2PJoint
from NaxToPy.Modules.Fasteners.Joints.N2PAttachment import N2PAttachment
from NaxToPy import N2PLog

# Method used to obtain a model's attachments --------------------------------------------------------------------------
def get_attachments(model: N2PModelContent, jointList: list[N2PJoint]) -> list[N2PAttachment]: 

    """
    Method that obtains a model's N2PAttachments and fills some of their attributes. 

    Args: 
        model: N2PModelContent
        jointList: list[N2PJoint] -> list of all N2PJoints to be analyzed.

    Returns: 
        attachmentList: list[N2PAttachment]

    Calling example: 
        >>> myAttachments = get_attachments(model1, JointsList) 
    """

    # STEP 0. Obtain the model's CQUAD4 and CTRIA3 elements
    supportedElements = ["CQUAD4", "CTRIA3"]
    domain = [i for i in model.get_elements() if i.TypeElement in supportedElements]

    # Auxiliary variables 
    seenPlates = [] 
    seenPlatesDict = {} 
    plateIDIterator = 0 
    oldToNewPlateIDDict = {} 
    jointAttachingPlates = {}

    # STEP 1. Loop over all joints
    for i, j in enumerate(jointList): 
        jointAttachingPlatesSet = set()
        # STEP 1.1. Loop over every plate in the joint 
        for p in j.PlateList: 
            if len(p.ElementList) == 0: 
                N2PLog.Warning.W505(j)
                continue
            # In order to assess whether two bolts connect the same plate or not, the only method found is to label 
            # the plate with the set of all 2D element IDS that conform that plate. This is done using the NaxToPy 
            # function get_attached (this may be slow for big models)
            plateElement = p.ElementList[0]
            allElementsID = {k.ID for k in model.get_elements_attached(cells = plateElement, domain = domain)}

            if allElementsID not in seenPlates: 
                # If this is the first time the plate is seen, it is given a new ID
                plateIDIterator += 1 
                seenPlates.append(allElementsID)
                newPlateID = plateIDIterator 
                seenPlatesDict[newPlateID] = allElementsID
                oldToNewPlateIDDict[p.AttachmentID] = newPlateID 
                p._attachment_id = newPlateID

            else: 
                # If the plate has already been seen, it is given its corresponding ID
                newPlateID = [k for k, l in seenPlatesDict.items() if l == allElementsID][0]
                oldToNewPlateIDDict[p.AttachmentID] = newPlateID 
                p._attachment_id = newPlateID
            # The joint is given the set of plates it is attached to
            jointAttachingPlatesSet.add(newPlateID)
        
        jointAttachingPlates[j] = jointAttachingPlatesSet

    # STEP 2 At this stage, all the information needed to classify the joints into attachments is already stored inside
    # them. Another loop over the list creates the N2PAttachment instances.
    seenAttachments = [] 
    attachmentList = [] 
    attachmentIndexDict = {}
    attachmentIDIterator = 0 
    for i in jointList: 
        attachment = tuple(jointAttachingPlates.get(i))
        if attachment not in seenAttachments: 
            # STEP 2.1. The attachment is new
            attachmentIDIterator += 1 
            newAttachment = N2PAttachment(id = attachmentIDIterator)
            newAttachment._attached_plates_id_list = list(attachment)
            newAttachment._attached_plates_list = i.PlateList 
            newAttachment._joints_list.append(i) 

            attachmentList.append(newAttachment)
            attachmentIndexDict[attachment] = attachmentList.index(newAttachment)
            seenAttachments.append(attachment)
        else: 
            # STEP 2.2. The attachment already exists 
            existingAttachmentIndex = attachmentIndexDict.get(attachment) 
            existingAttachment = attachmentList[existingAttachmentIndex]
            existingAttachment._joints_list.append(i)
    return attachmentList 
# ----------------------------------------------------------------------------------------------------------------------