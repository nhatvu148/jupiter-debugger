
import os
import sys
import JPT
from macro_defs import *
from macroTypes import *

# FUNCTION FOR FATIGUE EVALUATION

def line2RFSPC(block):
    # the block contains only 1 line
    [nodeID, type, forceX, forceY, forceZ, torqueX, torqueY, torqueZ] = block.split()
    return {'ID': nodeID,
            'RFSPC': [float(forceX), float(forceY), float(forceZ), float(torqueX), float(torqueY), float(torqueZ)]
            }


def line2SE(block):
    # the block contains 16 lines
    elementID = block[0].split()[0]
    nodalDataList = []
    try:
        for i in range(1, 15, 3):
            nodeID = block[i][0:24].strip()
            if nodeID == 'CENTER':
                continue

            xxStress = block[i][27:43].strip()
            xyStress = block[i][47:63].strip()
            pA = block[i][67:83].strip()
            misesStress = block[i][120:-1].strip()

            yyStress = block[i + 1][27:43].strip()
            yzStress = block[i + 1][47:63].strip()
            pB = block[i + 1][67:83].strip()

            zzStress = block[i + 2][27:43].strip()
            zxStress = block[i + 2][47:63].strip()
            pC = block[i + 2][67:83].strip()

            # To save memory, symmetric tensor is stored as a list of xx, xy, xz, yy, yz, zz stress components
            nodalDataList.append({'ID': nodeID,
                                  'StressTensor': [float(xxStress), float(xyStress), float(zxStress), float(yyStress),
                                                   float(yzStress), float(zzStress)],
                                  'PrincipalStress': [float(pA), float(pB), float(pC)],
                                  'MisesStress': float(misesStress)})
    except:
        print(block)
    return {'ID': elementID, 'nodalDataList': nodalDataList}


def readPRT(prtFilePath, average=True):
    print('Importing stress data from {}'.format(prtFilePath))
    totalNodalData = {}
    totalElementalData = {}
    with open(prtFilePath, 'r') as f:
        lines = f.readlines()
        # Read reaction forces at single-point constraint
        zeroToReadSPCRF = 2
        for line in lines:
            if line.strip() == '':
                continue
            if 'F O R C E S   O F   S I N G L E - P O I N T   C O N S T R A I N T' in line:
                zeroToReadSPCRF += -1
                continue
            if 'POINT ID' in line:
                zeroToReadSPCRF += -1
                continue
            if zeroToReadSPCRF == 0:
                try:
                    iNodalData = line2RFSPC(line)
                    iNodeID = iNodalData.pop('ID')
                    totalNodalData.update({iNodeID: iNodalData})
                except:
                    continue
            if zeroToReadSPCRF == 0 and 'SUBCASE' in line:
                break

        # Read Stress@NodeOnElement
        zeroToReadStress = 2
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip() == '':
                i += 1
                continue
            if 'S T R E S S E S   I N    T E T R A H E D R O N   S O L I D   E L E M E N T S   ( C T E T R A )' in line:
                zeroToReadStress -= 1
                i += 1
                continue
            if 'ELEMENT-ID' in line:
                zeroToReadStress -= 1
                i += 1
                continue
            if zeroToReadStress == 0:
                block = lines[i:i + 16]
                iElementalData = line2SE(block)
                elementID = iElementalData.pop('ID')
                # Update totalElementalData
                totalElementalData.update({elementID: iElementalData})
                # Update totalNodalData
                for iNodalData in iElementalData['nodalDataList']:
                    iNodalData.update({'belongingElementID': elementID})
                    iNodeID = iNodalData.pop('ID')
                    if iNodeID not in totalNodalData:
                        totalNodalData[iNodeID] = {}
                        totalNodalData[iNodeID].update({'Stress@NodeOnElement': []})
                    totalNodalData[iNodeID]['Stress@NodeOnElement'].append(iNodalData)
                i += 16
                continue

            if zeroToReadStress == 0 and 'SUBCASE' in line:
                # Stop reading
                break
            i += 1
        if average:
            for iNodeID, nodalData in totalNodalData.items():
                if 'Stress@NodeOnElement' in nodalData:
                    averagedMisesStress = sum(
                        [iNodalStress['MisesStress'] for iNodalStress in nodalData['Stress@NodeOnElement']]) / len(
                        nodalData['Stress@NodeOnElement'])
                    totalNodalData[iNodeID].update({'MisesStress': averagedMisesStress})
    print('Finished reading stress data.')
    return [totalNodalData, totalElementalData]


def evaluateSFA(totalNodalData, enduranceLimit, ultimateStress):
    for iNodeID, iNodalData in totalNodalData.items():
        if 'MisesStress' in iNodalData:
            amplitudeStress = iNodalData['MisesStress']
            meanStress = 0.0  # This is specified for fully reserved loading
            safetyFactor = 1.0 / (amplitudeStress / enduranceLimit + meanStress / ultimateStress)
            iNodalData.update({'SafetyFactor': safetyFactor})


def ModifyEnduranceLimit(enduranceLimit, influenceFactors={}):
    for factorLabel, factorValue in influenceFactors.items():
        print('Modifying endurance limit by consider {}.'.format(factorLabel))
        enduranceLimit *= factorValue
    return enduranceLimit


# Reliability
def Reliability(deviationMultiplicationFactor):
    return {'reliability': (1.0 - 0.08 * deviationMultiplicationFactor)}


# SizeEffect
def SizeEffect(diameter):
    if 51.0 >= diameter >= 2.79:
        return {'size_condition': 1.24 * pow(diameter, -0.107)}
    elif 245.0 >= diameter > 51:
        return {'size_condition': 0.859 - 0.000837}
    else:
        return 1.0


# SurfaceConditions
def SurfaceConditions(ultimateStress, a, b):
    return {'surface_factor': a * pow(ultimateStress, b)}


# CLASS FOR SHAFT MODELING
class ShaftModeling:
    def __init__(self, name, length, diameter):
        self.name = name
        self.length = length
        self.sections = []
        self.sections.append({'axialCoord': 0.0, 'diameter': diameter, 'length': length, 'filletRadius': 0.0})
        self.bearings = []
        self.bearingMasterNodes = []  # to calculate reaction force on bearing
        self.gears = []
        self.innerDiameter = 0.0
        self.keyways = []

    def StepDown(self, axialCoord, adjustment, filletRadius=0.0):
        if self.length > axialCoord > self.sections[-1]['axialCoord']:
            self.sections[-1]['length'] = axialCoord - self.sections[-1]['axialCoord']
            if filletRadius > adjustment:
                print('Fillet radius is larger than the step. It can not be modelled.')
                filletRadius = 0.0
            self.sections.append({'axialCoord': axialCoord, 'pre-diameter': self.sections[-1]['diameter'],
                                  'diameter': self.sections[-1]['diameter'] - 2 * adjustment,
                                  'length': self.length - axialCoord, 'filletRadius': filletRadius})

    def StepUp(self, axialCoord, adjustment, filletRadius=0.0):
        if self.length > axialCoord > self.sections[-1]['axialCoord']:
            self.sections[-1]['length'] = axialCoord - self.sections[-1]['axialCoord']
            if filletRadius > adjustment:
                print('Fillet radius is larger than the step. It can not be modelled.')
                filletRadius = 0
            self.sections.append({'axialCoord': axialCoord, 'pre-diameter': self.sections[-1]['diameter'],
                                  'diameter': self.sections[-1]['diameter'] + 2 * adjustment,
                                  'length': self.length - axialCoord, 'filletRadius': filletRadius})

    def DrillAxialHole(self, diameter):
        if diameter < self.sections[-1]['diameter']:
            self.innerDiameter = diameter
        else:
            print('Hole diameter is oversize.\nShaft can not be drilled.')

    def AddBearing(self, axialCoord, width):
        if axialCoord < self.length:
            self.bearings.append({'front': axialCoord - width / 2, 'back': axialCoord + width / 2, 'master': []})
            # self.bearings.append([axialCoord-width/2,axialCoord+width/2])

    def AddGear(self, axialCoord, width, verticalForce=0.0, horizontalForce=0, axialForce=0, torque=0, idle=False):
        if axialCoord < self.length:
            self.gears.append(
                {'axialCoord': axialCoord, 'front': axialCoord - width / 2.0, 'back': axialCoord + width / 2.0,
                 'verticalForce': verticalForce, 'horizontalForce': horizontalForce, 'axialForce': axialForce,
                 'torque': torque, 'idle': idle})

    def AddKeyway(self, axialCoord, length, width, depth):
        if axialCoord < self.length:
            # Calculate keyway location in shaft radial direction                            
            self.keyways.append(
                {'axialCoord': axialCoord, 'front': axialCoord - length / 2.0, 'back': axialCoord + length / 2.0,
                 'length': length, 'width': width, 'depth': depth})

    def CreateModel(self, averageElemSize=3, bTet10=False):
        # Create shaft sections
        for i, section in enumerate(self.sections):
            Geometry.Part.Cylinder(dlOrigin=[0.0, section['axialCoord'] * 1e-3, 0.0],
                                   dTopRadius=section['diameter'] / 2.0 * 1e-3,
                                   dBotRadius=section['diameter'] / 2.0 * 1e-3, dHeight=section['length'] * 1e-3,
                                   strName="SECTION_{}".format(i))

        # Merge sections to one
        for i in range(len(JPT.GetAllParts()) - 1):
            parts = JPT.GetAllParts()
            JPT.Exec('AssembleBoolean2([3:{}, 3:{}], 0, 1e-06, 0)'.format(parts[0].id, parts[1].id))
        # Fillet shaft edges
        for section in self.sections:
            if section['filletRadius'] > 0.0:
                edges = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_EDGE, 0.0, section['axialCoord'],
                                                  min(section['diameter'], section['pre-diameter']) / 2.0)
                # Geometry.MakeFillet(crlEdges=[Edge(edges[1].id)], dRadius=section['filletRadius'])
                JPT.Exec('MakeFillet([5: {}], {})'.format(edges[1].id, section['filletRadius'] * 1e-3))

        # Imprint lines for bearings
        for bearing in self.bearings:
            Geometry.Edge.PlanarLine(veclPosition=[[0.0, bearing['front'] * 1e-3, 0.0]],
                                     crlTargetFace=[Face(face.id) for face in JPT.GetAllFaces()], iType=1)
            Geometry.Edge.PlanarLine(veclPosition=[[0.0, bearing['back'] * 1e-3, 0.0]],
                                     crlTargetFace=[Face(face.id) for face in JPT.GetAllFaces()], iType=1)

        # Imprint lines for gears
        for gear in self.gears:
            Geometry.Edge.PlanarLine(veclPosition=[[0.0, gear['front'] * 1e-3, 0.0]],
                                     crlTargetFace=[Face(face.id) for face in JPT.GetAllFaces()], iType=1)
            Geometry.Edge.PlanarLine(veclPosition=[[0.0, gear['back'] * 1e-3, 0.0]],
                                     crlTargetFace=[Face(face.id) for face in JPT.GetAllFaces()], iType=1)

        # Keyway cut
        for keyway in self.keyways:
            Geometry.Part.Cube(dlOrigin=[-keyway['width'] / 2.0 * 1e-3, keyway['front'] * 1e-3, (
                    self.FindDiameterAtAxialCoord(keyway['front']) / 2.0 - keyway['depth']) * 1e-3],
                               dlLength=[keyway['width'] * 1e-3, keyway['length'] * 1e-3, 2 * keyway['depth'] * 1e-3])
            # Create fillet on keyway
            edges = []
            keywayFilletRadius = keyway['width'] * 1e-3 / 2.01
            edge1 = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_EDGE, -keyway['width'] / 2.0, keyway['front'],
                                              (self.FindDiameterAtAxialCoord(keyway['front']) / 2.0))
            JPT.Exec('MakeFillet([5:{}], {})'.format(edge1[1].id, keywayFilletRadius))

            edge2 = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_EDGE, keyway['width'] / 2.0, keyway['front'],
                                              (self.FindDiameterAtAxialCoord(keyway['front']) / 2.0))
            JPT.Exec('MakeFillet([5:{}], {})'.format(edge2[1].id, keywayFilletRadius))

            edge3 = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_EDGE, -keyway['width'] / 2.0, keyway['back'],
                                              (self.FindDiameterAtAxialCoord(keyway['front']) / 2.0))
            JPT.Exec('MakeFillet([5:{}], {})'.format(edge3[1].id, keywayFilletRadius))

            edge4 = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_EDGE, keyway['width'] / 2.0, keyway['back'],
                                              (self.FindDiameterAtAxialCoord(keyway['front']) / 2.0))
            JPT.Exec('MakeFillet([5:{}], {})'.format(edge4[1].id, keywayFilletRadius))

            parts = JPT.GetAllParts()
            JPT.Exec('AssembleBoolean2([3:{}, 3:{}], 1, 1e-06, 0)'.format(parts[0].id, parts[1].id))

            # Offset imprint for iso mesh
            Geometry.Edge.PlanarLine(veclPosition=[[0.0, (keyway['front'] - averageElemSize) * 1e-3, 0.0]],
                                     crlTargetFace=[Face(face.id) for face in JPT.GetAllFaces()], iType=1)
            Geometry.Edge.PlanarLine(veclPosition=[[0.0, (keyway['back'] + averageElemSize) * 1e-3, 0.0]],
                                     crlTargetFace=[Face(face.id) for face in JPT.GetAllFaces()], iType=1)

            # Create constrains at bearings
        for i, bearing in enumerate(self.bearings):
            faces = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_FACE, 0, (bearing['front'] + bearing['back']) / 2.0,
                                              -self.FindDiameterAtAxialCoord(
                                                  (bearing['front'] + bearing['back']) / 2.0) / 2.0)
            try:
                JPT.Exec('Rbe2(18, [], [6:{}], 2, "RBE2_BR{}", 0:0, 0, 7, [0.0, {}, 0.0], 0, 0:0, 1, 0, 1, -1)'.format(
                    faces[1].id, i, (bearing['front'] + bearing['back']) * 1e-3 / 2.0))
                nodes = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_NODE, 0,
                                                  (bearing['front'] + bearing['back']) / 2.0, 0.0)
                BoundaryConditions.FixedConstraint(strName='CONST_BR{}'.format(i), iDwDof=47,
                                                   crlTarget=[Node(nodes[0].id)])
                self.bearingMasterNodes.append(nodes[0].id)

            except:
                print('Internal error: RBE2 for bearing #{} @ axialCoord={} can not be defined.'.format(i, (
                        bearing['front'] + bearing['back']) / 2.0))

        # Create node group to export reaction force
        strCursorBearingMasterNodes = '['
        for iNode in self.bearingMasterNodes:
            strCursorBearingMasterNodes += '10:{},'.format(iNode)
        strCursorBearingMasterNodes += ']'
        strCursorBearingMasterNodes.replace(',]', ']')
        JPT.Exec('CreateGroup("SPC_BR", {}, 0:0)'.format(strCursorBearingMasterNodes))

        # Create load at gears
        for i, gear in enumerate(self.gears):
            faces = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_FACE, 0, (gear['front'] + gear['back']) / 2.0,
                                              -self.FindDiameterAtAxialCoord(
                                                  (gear['front'] + gear['back']) / 2.0) / 2.0)
            try:
                JPT.Exec('Rbe2(18, [], [6:{}], 2, "RBE2_GR{}", 0:0, 0, 7, [0.0, {}, 0.0], 0, 0:0, 1, 0, 1, -1)'.format(
                    faces[1].id, i, (gear['front'] + gear['back']) * 1e-3 / 2.0))
                nodes = JPT.GetEntitiesByPosition(JPT.AssociateType.AS_NODE, 0.0, (gear['front'] + gear['back']) / 2.0,
                                                  0.0)
                BoundaryConditions.Force.General(strName='LOAD_GR{}'.format(i),
                                                 vecForce=[gear['horizontalForce'], gear['axialForce'],
                                                           gear['verticalForce']],
                                                 vecMoment=[0.0, gear['torque'] * 1e-3, 0.0],
                                                 crlTarget=[Node(nodes[0].id)])
                if gear['idle']:
                    BoundaryConditions.FixedConstraint(strName='ROTFIX_GR'.format(i), iDwDof=16,
                                                       crlTarget=[Node(nodes[0].id)])
            except:
                print('Internal error: RBE2 for gear #{} @ axialCoord={} can not be defined.'.format(i, (
                        gear['front'] + gear['back']) / 2.0))

                # Drill axial hole
        if self.innerDiameter > 0.0:
            Geometry.Part.Cylinder(dlOrigin=[0.0, 0.0, 0.0], dTopRadius=self.innerDiameter / 2.0 * 1e-3,
                                   dBotRadius=self.innerDiameter / 2.0 * 1e-3, dHeight=self.length * 1e-3,
                                   strName="HOLE".format(i))
            parts = JPT.GetAllParts()
            Assemble.Boolean(crlPart=[Part(parts[0].id, parts[1].id)], iBooleanType=1, dToleranceAlignment=0.001)

        # Create mesh
        Meshing.SurfaceMeshing(crlPart=[Part(1)], surfaceMesh=SURFACE_MESH(dAvgElemSize=averageElemSize * 1e-3,
                                                                           dMaxElemSize=averageElemSize * 1.4e-3,
                                                                           iPerformanceMode=1, bGeomApprox=True,
                                                                           iNextEntityOffsetId=0))

        Meshing.SolidMeshing(crlPart=[Part(1)], bTet10=bTet10, dGradingFactor=1.05, dStretchLimit=0.1, iSpeedVsQual=1,
                             iRegion=1, bSafeMode=False, iParallel=8, bInternalMeshOnly=False)

    def DefineMaterial(self, elasticModulus=2e11, poisonRatio=0.3):
        # This function was not yet fully developed due to some of PSJ macros do not work properly. 
        # Input parameters are dummy.
        # Create and assign material to the shaft
        JPT.Exec(
            'CreateMaterial([[1104, "<?xml version=#1.0#?><JPT-MATERIAL-LIBRARY Version=#3#><Material Name=#Structural_Steel# Description=## Id=#1# NasId=#1# DBId=#0# IsCompositeMaterial=#false# CId=#0#><Layer Thick=# # Angle=# # Id=#0#><Density temperatureDependency=#0# dependencies=#0#><Table Row=#1# Col=#1#><Data>7.850000000000001e+03</Data></Table></Density><Elastic Type=#0# temperatureDependency=#0# dependencies=#0# Moduli=#LONG_TERM# SubOption=#Fail_Strain# noCompression=#0# noTension=#0#><Table Row=#1# Col=#3#><Data>2.000000000000000e+11, ,3.000000000000000e-01</Data></Table><Table Row=#1# Col=#3#><Data> , , </Data></Table></Elastic><Expansion Type=#0# userSubroutine=#0# zero=#0# temperatureDependency=#0# dependencies=#0#><Table Row=#1# Col=#1#><Data>1.200000000000000e-05</Data></Table></Expansion><Conductivity Type=#0# temperatureDependency=#0# dependencies=#0#><Table Row=#1# Col=#1#><Data>5.900000000000000e+01</Data></Table></Conductivity><SpecificHeat temperatureDependency=#0# dependencies=#0#><Table Row=#1# Col=#1#><Data>4.610000000000000e+02</Data></Table></SpecificHeat></Layer></Material></JPT-MATERIAL-LIBRARY>"]], 1)')
        Properties.Solid(strName=self.name, crMaterial=Material(1), iCordM=-2, dDynaRemeshVal1=DFLT_DBL,
                         dDynaRemeshVal2=DFLT_DBL, dDispHG=DFLT_DBL, crlTarget=[Part(1)], iFLG=-1)

    def FindDiameterAtAxialCoord(self, axialCoord):
        for section in self.sections:
            if section['axialCoord'] > axialCoord:
                break
            diameterAtAxialCoord = section['diameter']

        print('{}:{}'.format(axialCoord, diameterAtAxialCoord))
        return diameterAtAxialCoord


    def ExportAbaqusJob(self, dataPath):
        jobFile = os.path.join(dataPath, self.name+'.inp')
        JPT.Exec('AbaqusStaticStep("Static", "", 1, 100, 1, 1e-05, 1, 0, 0, 0, 8, 1, 30, 0, 0.0002, 1, 0.05, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, [""], [], 0:0)')
        JPT.Exec('AbaModifyLbcToStep([(134:1, 29:1, 3, 2), (134:1, 29:2, 3, 2), (134:1, 37:1, 2, 0), (134:1, 37:2, 2, 0), (134:1, 37:3, 2, 0)])')
        JPT.Exec('CreateAbaqusJob("{}", 1, 0, 0, 1, 1, 0, "", [134:1], 0:0, [], 1, 1, 1, 0, 0, 22:1)'.format(self.name))
        JPT.Exec('ExportAbaqusInp(143:1, [], "{}")'.format(jobFile))


    def ExportSunshineJob(self, dataPath):
        # This is a temporary function
        jobFile = os.path.join(dataPath, '{}.bdf'.format(self.name))

        Analysis.TSSS.LinearStatic(strName=self.name,
                                   nastranAnalysis=NASTRAN_ANALYSIS(iSolverType=6, iGridFormatType=1, dEpsilon=DFLT_DBL,
                                                                    iMaxNumOfIter=DFLT_INT, iNumberOfThreads=1, iMemory=2,
                                                                    iNcpu=1, iSolNo=101, nastranEigen=NASTRAN_EIGEN(),
                                                                    nastranEigen126=NASTRAN_EIGEN126(),
                                                                    nastranFrequency=NASTRAN_FREQUENCY(),
                                                                    nastranFreqTimestep=NASTRAN_FREQ_TIMESTEP(
                                                                        iModalDampingTableId=0),
                                                                    nastranOutputRequest=NASTRAN_OUTPUT_REQUEST(
                                                                        iValueSpcforces=1, iTypeSpcforces=2,
                                                                        iTypeStress=3, iTypeStrain=0),
                                                                    nastranExecControl=NASTRAN_EXEC_CONTROL(),
                                                                    nastranCaseControl=NASTRAN_CASE_CONTROL(),
                                                                    nastranMainLbcSet=NASTRAN_MAIN_LBC_SET(),
                                                                    nastranSettings=NASTRAN_SETTINGS(),
                                                                    nastranNonlinear=NASTRAN_NONLINEAR(iKMETHOD=3,
                                                                                                       iMAXITER=DFLT_INT,
                                                                                                       bUseEPSW=True,
                                                                                                       dEPSU=DFLT_DBL,
                                                                                                       dEPSP=DFLT_DBL),
                                                                    nastranNonlinearTimestep=NASTRAN_NONLINEAR_TIMESTEP()),
                                   iRadialReturn=DFLT_INT,
                                   strPath=jobFile)

    def SaveJTDB(self, dataPath):
        if dataPath == '':
            dataPath = os.getcwd()
        JPT.Exec('SaveJTDB("{}")'.format(os.path.join(dataPath, '{}.jtdb'.format(self.name))))

# ----------------------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------------------

# SHAFT MODELING

modelName = 'SHAFT_CALC'
dataPath = os.getcwd()
shaft = ShaftModeling(name=modelName, length=364.0, diameter=75.0)
shaft.StepUp(axialCoord=48.0, adjustment=12.5, filletRadius=6.0)
shaft.StepDown(axialCoord=58.0, adjustment=10.0)
shaft.StepUp(axialCoord=62.0, adjustment=2.5)
shaft.StepDown(axialCoord=158.0, adjustment=1.5)
shaft.StepDown(axialCoord=261.0, adjustment=4.0, filletRadius=3.0)
shaft.StepDown(axialCoord=296.0, adjustment=7.5)
shaft.DrillAxialHole(15)
shaft.AddGear(axialCoord=107.0, width=60, verticalForce=-25784, torque=836421)
shaft.AddKeyway(axialCoord=107.0, length=80, width=20, depth=3)
shaft.AddGear(axialCoord=328.0, width=40, verticalForce=863.22, idle=True)
shaft.AddKeyway(axialCoord=328.0, length=52, width=16, depth=3)
shaft.AddBearing(axialCoord=24.0, width=20.0)
shaft.AddBearing(axialCoord=278.5, width=20.0)
shaft.CreateModel(averageElemSize=5, bTet10=False)
shaft.DefineMaterial(elasticModulus=2e11, poisonRatio=0.3)
shaft.ExportSunshineJob(dataPath)
shaft.ExportAbaqusJob(dataPath)
shaft.SaveJTDB(dataPath)

# SOLVE FOR STRESS USING SUNSHINE
import subprocess
sunshinePath = '"C:\Program Files\TechnoStar\Jupiter-Pre_5.0\SunShine\sunshine.exe"'
# os.system('{} --progress --stdlog {}'.format(sunshinePath, os.path.join(dataPath, modelName + '.bdf')))
subprocess.call('{} --progress --stdlog {}'.format(sunshinePath, os.path.join(dataPath, modelName + '.bdf')))

###########################################################################
# FATIGUE EVALUATION
# Calculate averaged nodal stress to determine fatigue life
# Fully reserved cyclic loading is assumed, and hence, effect of mean stress is neglect.
# In addition, directions of principal stresses among load steps
# are assumed to be identical between maximum and minimum loading
# Only Mises stress is considered in this calculation

prtFilePath = os.path.join(dataPath, modelName+'.prt')

# Import stress data
[totalNodalData, totalElementalData] = readPRT(prtFilePath)


print('Begin calculating safety factor:')
# Define ultimate stress and influence factors
ultimateStress = 420.0  # MPa
# For cast steel:
enduranceLimit = 0.4 * ultimateStress
# Define influence factors
influenceFactors = {}
influenceFactors.update(Reliability(0.99))
influenceFactors.update(SizeEffect(50))  # assume that the shaft has diameter of 50 mm
influenceFactors.update(
    SurfaceConditions(ultimateStress, 4.51, -0.265))  # assume that the shaft is machined or cold-drawn

enduranceLimit = ModifyEnduranceLimit(enduranceLimit, influenceFactors)

# Evaluate safety factor
evaluateSFA(totalNodalData, enduranceLimit, ultimateStress)

outputFilePath = os.path.join(dataPath, modelName+'_SFA.csv')
print('Write out nodal equivalent stress and safety factor to\n{}'.format(outputFilePath))

with open(outputFilePath, 'w') as fSFA:
    fSFA.write('ALTAIR ASCII FILE\n')
    fSFA.write('$TITTLE = Static Analysis\n')
    fSFA.write('$SUBCASE = 1 Subcase 1\n')
    fSFA.write('$BINDING = NODE\n')
    fSFA.write('$COLUMN_INFO = ENTITY_ID\n')
    fSFA.write('$RESULT_TYPE = MisesStress(s), SafetyFactor(s)\n')

    for iNodeID, iNodalData in totalNodalData.items():
        if 'Stress@NodeOnElement' in iNodalData:
            fSFA.write('{},{},{}\n'.format(iNodeID, iNodalData['MisesStress'], iNodalData['SafetyFactor']))
print(len(totalNodalData))
print('Finished calculating safety factor.')

