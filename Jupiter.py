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
    def RemoveEntitiesByID():
        message = "JPT.RemoveEntitiesByID()"
        return get_res_from_jupiter(message)
    def RemoveEntitiesByName():
        message = "JPT.RemoveEntitiesByName()"
        return get_res_from_jupiter(message)
    def RemoveAllConnections():
        message = "JPT.RemoveAllConnections()"
        return get_res_from_jupiter(message)
    def RemoveAllLoadsBCs():
        message = "JPT.RemoveAllLoadsBCs()"
        return get_res_from_jupiter(message)
    def RemoveAllContacts():
        message = "JPT.RemoveAllContacts()"
        return get_res_from_jupiter(message)
    def RemoveAllLoadCases():
        message = "JPT.RemoveAllLoadCases()"
        return get_res_from_jupiter(message)
    def RemoveAllCoordinates():
        message = "JPT.RemoveAllCoordinates()"
        return get_res_from_jupiter(message)
    def RemoveAllMaterials():
        message = "JPT.RemoveAllMaterials()"
        return get_res_from_jupiter(message)
    def RemoveAllMeshSettings():
        message = "JPT.RemoveAllMeshSettings()"
        return get_res_from_jupiter(message)
    def RemoveWSProperties():
        message = "JPT.RemoveWSProperties()"
        return get_res_from_jupiter(message)
    def RemoveAllFieldTables():
        message = "JPT.RemoveAllFieldTables()"
        return get_res_from_jupiter(message)
    def RemoveAllAbaqusStep():
        message = "JPT.RemoveAllAbaqusStep()"
        return get_res_from_jupiter(message)
    def RemoveAllSolverjob():
        message = "JPT.RemoveAllSolverjob()"
        return get_res_from_jupiter(message)
    def RemoveAllByTableType():
        message = "JPT.RemoveAllByTableType()"
        return get_res_from_jupiter(message)
    def CreateSubAssembly():
        message = "JPT.CreateSubAssembly()"
        return get_res_from_jupiter(message)
    def DeleteSubAssembly():
        message = "JPT.DeleteSubAssembly()"
        return get_res_from_jupiter(message)
    def FindSubAssemblyByName():
        message = "JPT.FindSubAssemblyByName()"
        return get_res_from_jupiter(message)
    def FindSubAssemblyByID():
        message = "JPT.FindSubAssemblyByID()"
        return get_res_from_jupiter(message)
    def DeleteSubAssemblyRecursively():
        message = "JPT.DeleteSubAssemblyRecursively()"
        return get_res_from_jupiter(message)
    def GetAllPartsInSubAssembly():
        message = "JPT.GetAllPartsInSubAssembly()"
        return get_res_from_jupiter(message)
    def CastToDItem():
        message = "JPT.CastToDItem()"
        return get_res_from_jupiter(message)
    def CastDItemToDBody():
        message = "JPT.CastDItemToDBody()"
        return get_res_from_jupiter(message)
    def CastDItemToDEdge():
        message = "JPT.CastDItemToDEdge()"
        return get_res_from_jupiter(message)
    def CastDItemToDGroup():
        message = "JPT.CastDItemToDGroup()"
        return get_res_from_jupiter(message)
    def CastDItemToDNode():
        message = "JPT.CastDItemToDNode()"
        return get_res_from_jupiter(message)
    def CastDItemToDElem():
        message = "JPT.CastDItemToDElem()"
        return get_res_from_jupiter(message)
    def DItemToMacroTCursor():
        message = "JPT.DItemToMacroTCursor()"
        return get_res_from_jupiter(message)
    def DItemListToMacroListTCursor():
        message = "JPT.DItemListToMacroListTCursor()"
        return get_res_from_jupiter(message)
    def DItemToMacroListTCursor():
        message = "JPT.DItemToMacroListTCursor()"
        return get_res_from_jupiter(message)
    def MacroResultParser():
        message = "JPT.MacroResultParser()"
        return get_res_from_jupiter(message)
    def MacroListTCursorToListDItem():
        message = "JPT.MacroListTCursorToListDItem()"
        return get_res_from_jupiter(message)
    def MacroTCursorToDItem():
        message = "JPT.MacroTCursorToDItem()"
        return get_res_from_jupiter(message)
    def ConvertRGBToJPTColor():
        message = "JPT.ConvertRGBToJPTColor()"
        return get_res_from_jupiter(message)
    def GetJTDBVersion():
        message = "JPT.GetJTDBVersion()"
        return get_res_from_jupiter(message)
    def CopyToClipBoard():
        message = "JPT.CopyToClipBoard()"
        return get_res_from_jupiter(message)
    def CheckLicense():
        message = "JPT.CheckLicense()"
        return get_res_from_jupiter(message)
    def IsDefaultDouble():
        message = "JPT.IsDefaultDouble()"
        return get_res_from_jupiter(message)
    def IsDefaultInt():
        message = "JPT.IsDefaultInt()"
        return get_res_from_jupiter(message)
    def ConvertFromDocUnit():
        message = "JPT.ConvertFromDocUnit()"
        return get_res_from_jupiter(message)
    def ConvertValueToDocUnit():
        message = "JPT.ConvertValueToDocUnit()"
        return get_res_from_jupiter(message)
    def ConvertFromMacroUnit():
        message = "JPT.ConvertFromMacroUnit()"
        return get_res_from_jupiter(message)
    def ConvertValueToMacroUnit():
        message = "JPT.ConvertValueToMacroUnit()"
        return get_res_from_jupiter(message)
    def GetJPTTempPath():
        message = "JPT.GetJPTTempPath()"
        return get_res_from_jupiter(message)
    def ListDoubleToMacroVector():
        message = "JPT.ListDoubleToMacroVector()"
        return get_res_from_jupiter(message)
    def GetCurrentDocumentPath():
        message = "JPT.GetCurrentDocumentPath()"
        return get_res_from_jupiter(message)
    def QuitApplication():
        message = "JPT.QuitApplication()"
        return get_res_from_jupiter(message)
    def GetAppPathInfo():
        message = "JPT.GetAppPathInfo()"
        return get_res_from_jupiter(message)
    def GetSelectedNodes():
        message = "JPT.GetSelectedNodes()"
        return get_res_from_jupiter(message)
    def GetSelectedElems():
        message = "JPT.GetSelectedElems()"
        return get_res_from_jupiter(message)
    def GetSelectedFaces():
        message = "JPT.GetSelectedFaces()"
        return get_res_from_jupiter(message)
    def GetSelectedEdges():
        message = "JPT.GetSelectedEdges()"
        return get_res_from_jupiter(message)
    def GetSelectedParts():
        message = "JPT.GetSelectedParts()"
        return get_res_from_jupiter(message)
    def GetSelectedGroups():
        message = "JPT.GetSelectedGroups()"
        return get_res_from_jupiter(message)
    def GetAllParts():
        message = "JPT.GetAllParts()"
        return get_res_from_jupiter(message)
    def GetAllFaces():
        message = "JPT.GetAllFaces()"
        return get_res_from_jupiter(message)
    def GetAllEdges():
        message = "JPT.GetAllEdges()"
        return get_res_from_jupiter(message)
    def GetAllElems():
        message = "JPT.GetAllElems()"
        return get_res_from_jupiter(message)
    def GetAllNodes():
        message = "JPT.GetAllNodes()"
        return get_res_from_jupiter(message)
    def GetAllGroups():
        message = "JPT.GetAllGroups()"
        return get_res_from_jupiter(message)
    def GetAllByTableTypeID():
        message = "JPT.GetAllByTableTypeID()"
        return get_res_from_jupiter(message)
    def GetAllByTypeID():
        message = "JPT.GetAllByTypeID()"
        return get_res_from_jupiter(message)
    def GetAllByType():
        message = "JPT.GetAllByType()"
        return get_res_from_jupiter(message)
    def GetCountByType():
        message = "JPT.GetCountByType()"
        return get_res_from_jupiter(message)
    def GetAllSelected():
        message = "JPT.GetAllSelected()"
        return get_res_from_jupiter(message)
    def GetLastCreatedCursor():
        message = "JPT.GetLastCreatedCursor()"
        return get_res_from_jupiter(message)
    def GetCenterOfEntities():
        message = "JPT.GetCenterOfEntities()"
        return get_res_from_jupiter(message)
    def GetSharedFaces():
        message = "JPT.GetSharedFaces()"
        return get_res_from_jupiter(message)
    def GetSharedElements():
        message = "JPT.GetSharedElements()"
        return get_res_from_jupiter(message)
    def GetSharedNodes():
        message = "JPT.GetSharedNodes()"
        return get_res_from_jupiter(message)
    def GetAllLoadsBCs():
        message = "JPT.GetAllLoadsBCs()"
        return get_res_from_jupiter(message)
    def GetMaterialXML():
        message = "JPT.GetMaterialXML()"
        return get_res_from_jupiter(message)
    def GetMaterialOriginalXML():
        message = "JPT.GetMaterialOriginalXML()"
        return get_res_from_jupiter(message)
    def GetMaxMaterialID():
        message = "JPT.GetMaxMaterialID()"
        return get_res_from_jupiter(message)
    def GetMaterialDBById():
        message = "JPT.GetMaterialDBById()"
        return get_res_from_jupiter(message)
    def GetSelectedNodesCr():
        message = "JPT.GetSelectedNodesCr()"
        return get_res_from_jupiter(message)
    def GetSelectedElemsCr():
        message = "JPT.GetSelectedElemsCr()"
        return get_res_from_jupiter(message)
    def GetSelectedFacesCr():
        message = "JPT.GetSelectedFacesCr()"
        return get_res_from_jupiter(message)
    def GetSelectedEdgesCr():
        message = "JPT.GetSelectedEdgesCr()"
        return get_res_from_jupiter(message)
    def GetSelectedPartsCr():
        message = "JPT.GetSelectedPartsCr()"
        return get_res_from_jupiter(message)
    def GetSelectedGroupsCr():
        message = "JPT.GetSelectedGroupsCr()"
        return get_res_from_jupiter(message)
    def GetUndoCount():
        message = "JPT.GetUndoCount()"
        return get_res_from_jupiter(message)
    def ClearUndo():
        message = "JPT.ClearUndo()"
        return get_res_from_jupiter(message)
    def GetRedoCount():
        message = "JPT.GetRedoCount()"
        return get_res_from_jupiter(message)
    def ClearRedo():
        message = "JPT.ClearRedo()"
        return get_res_from_jupiter(message)
    def GetOpnList():
        message = "JPT.GetOpnList()"
        return get_res_from_jupiter(message)
    def GetMacroLog():
        message = "JPT.GetMacroLog()"
        return get_res_from_jupiter(message)
    def GetPythonAPILog():
        message = "JPT.GetPythonAPILog()"
        return get_res_from_jupiter(message)
    def ShowHideEntitiesByID():
        message = "JPT.ShowHideEntitiesByID()"
        return get_res_from_jupiter(message)
    def ShowHideAllParts():
        message = "JPT.ShowHideAllParts()"
        return get_res_from_jupiter(message)
    def InverseHideBodies():
        message = "JPT.InverseHideBodies()"
        return get_res_from_jupiter(message)
    def ViewFitToModel():
        message = "JPT.ViewFitToModel()"
        return get_res_from_jupiter(message)
    def Exec():
        message = "JPT.Exec()"
        return get_res_from_jupiter(message)
    def GetMaxIDEntity():
        message = "JPT.GetMaxIDEntity()"
        return get_res_from_jupiter(message)
    def GetMinIDEntity():
        message = "JPT.GetMinIDEntity()"
        return get_res_from_jupiter(message)
    def GetEntitiesByName():
        message = "JPT.GetEntitiesByName()"
        return get_res_from_jupiter(message)
    def GetEntitiesByID():
        message = "JPT.GetEntitiesByID()"
        return get_res_from_jupiter(message)
    def GetEntitiesByPosition():
        message = "JPT.GetEntitiesByPosition()"
        return get_res_from_jupiter(message)
    def GetEntitiesByAssociation():
        message = "JPT.GetEntitiesByAssociation()"
        return get_res_from_jupiter(message)
    def GetEntitiesByAdjacent():
        message = "JPT.GetEntitiesByAdjacent()"
        return get_res_from_jupiter(message)
    def MsgOut():
        message = "JPT.MsgOut()"
        return get_res_from_jupiter(message)
    def PrintAppPathInfo():
        message = "JPT.PrintAppPathInfo()"
        return get_res_from_jupiter(message)
    def PrintPSJUtilityManual():
        message = "JPT.PrintPSJUtilityManual()"
        return get_res_from_jupiter(message)
    def Debugger():
        message = "JPT.Debugger()"
        return get_res_from_jupiter(message)
    def GetElemsByKind():
        message = "JPT.GetElemsByKind()"
        return get_res_from_jupiter(message)
    def GetRandomJPTColor():
        message = "JPT.GetRandomJPTColor()"
        return get_res_from_jupiter(message)
    def ConvertJPTColorToRGB():
        message = "JPT.ConvertJPTColorToRGB()"
        return get_res_from_jupiter(message)
    def ClearLog():
        message = "JPT.ClearLog()"
        return get_res_from_jupiter(message)
    def SetSelectMethod():
        message = "JPT.SetSelectMethod()"
        return get_res_from_jupiter(message)
    def MacroTCursorPairToDItemPair():
        message = "JPT.MacroTCursorPairToDItemPair()"
        return get_res_from_jupiter(message)
    def MessageBoxPSJ():
        message = "JPT.MessageBoxPSJ()"
        return get_res_from_jupiter(message)
    def CastDItemToDFace():
        message = "JPT.CastDItemToDFace()"
        return get_res_from_jupiter(message)
    def DItemToMacroTCursorPair():
        message = "JPT.DItemToMacroTCursorPair()"
        return get_res_from_jupiter(message)
    def GetProgramPath():
        message = "JPT.GetProgramPath()"
        return get_res_from_jupiter(message)


