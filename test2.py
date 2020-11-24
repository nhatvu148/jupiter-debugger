from Jupiter import *

print(Analysis.AbaqusStep.DynamicStep())
print(JPT.RemoveEntitiesByID())
Analysis.Abaqus(strName="", bRBE2toMPC=False, bRenameProcess=False, iCodeType=0, iSurfDefType=0, iUnit=0, iWriteType=0, strDescription="", crlStepSequence=[], crEdit=None, strlUserText=[], bExptNdEleGroups=False, bDeleteFloatingNodes=False, bExptFaceElemGroups2Surface=False, bLoadCase=False, bAutoAssignDummyProperty=True, crDummyMat=None)
Analysis.AbaqusStep.DynamicStep(param=ABAQUS_DYNAMIC(), crEdit=None)
Connections.BarBeam(strName="", iEType=10, iMethod=1, crProp=None, dlOrient=[], crlMasterTarget=[], crlSlaveTarget=[])