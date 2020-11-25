# from PSJ_Intepreter import JupiterListener, SendMessageToJupiter
# import win32gui

def get_res_from_jupiter(message):
    # connector = JupiterListener()
    msg_to_jupiter = 'line; {0}; false'.format(message)
    # val = SendMessageToJupiter(msg_to_jupiter)
    return msg_to_jupiter

class AbaqusStep:
    def __init__(self):
        pass
    def DynamicStep(self):
        return 1234

class Analysis:
    B = 5
    AbaqusStep = AbaqusStep()
    def Abaqus(strName="", bRBE2toMPC=False, bRenameProcess=False, iCodeType=0, iSurfDefType=0, iUnit=0, iWriteType=0, strDescription="", crlStepSequence=[], crEdit=None, strlUserText=[], bExptNdEleGroups=False, bDeleteFloatingNodes=False, bExptFaceElemGroups2Surface=False, bLoadCase=False, bAutoAssignDummyProperty=True, crDummyMat=None):
        message = "Analysis.Abaqus('{}', {}, {}, {}, {}, {}, {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {})".format(strName, bRBE2toMPC, bRenameProcess, iCodeType, iSurfDefType, iUnit, iWriteType, strDescription, crlStepSequence, crEdit, strlUserText, bExptNdEleGroups, bDeleteFloatingNodes, bExptFaceElemGroups2Surface, bLoadCase, bAutoAssignDummyProperty, crDummyMat)
        return get_res_from_jupiter(message)

class EntityType:
    BODY = 0
    FACE = 1
    ELEM = 2
    EDGE = 3
    GROUP = 4
    NODE = 5
    INST = 6

class JPT:
    EntityType = EntityType()
    """
    Function: JPT.RemoveAllLoadCases
    Description: Remove all load cases in models
    Input1: None
    Return: None
    Example: JPT.RemoveAllLoadCases()
    """
    def RemoveEntitiesByID():
        return "RemoveEntitiesByID"
    def RemoveEntitiesByName():
        return "RemoveEntitiesByName"
    def RemoveAllLoadsBCs():
        return "RemoveAllLoadsBCs"
    def RemoveAllContacts():
        return "RemoveAllContacts"
    def RemoveAllConnections():
        return "RemoveAllConnections"
    def RemoveAllLoadCases():
        return "RemoveAllLoadCases"
    def RemoveAllMaterials():
        return "RemoveAllMaterials"
    def RemoveWSProperties():
        return "RemoveWSProperties"
    def RemoveAllCoordinates():
        return "RemoveAllCoordinates"
    def RemoveAllMeshSettings():
        return "RemoveAllMeshSettings"
    def RemoveAllFieldTables():
        return "RemoveAllFieldTables"
    def RemoveAllAbaqusStep():
        return "RemoveAllAbaqusStep"

