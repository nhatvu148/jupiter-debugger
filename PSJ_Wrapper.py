from PSJ_Intepreter import JupiterListener, SendMessageToJupiter
import win32gui

def get_res_from_jupiter():
    connector = JupiterListener()

    VisualCodeMsg1 = 'file; file.py; false'
    VisualCodeMsg2 = 'line; JPT.PrintPSJUtilityManual(); false'
    codeMsg3 = 'line; Geometry.Part.Cylinder(dlOrigin=[0,0,0], dTopRadius=0.01, dBotRadius=0.01, dHeight=0.01, iCircleNodeCnt=36, iAxisNodeCnt=10, strName="Cylinder_1", iPartCol=7105764, crCoord=None); false'
    codeMsg4 = 'line; JPT.Exec(\'CreateCube([0, 0, 0], [0.01, 0.01, 0.01], [10, 10, 10], "Cube_1", 7105764, 0:0)\'); false'
    
    val = SendMessageToJupiter(codeMsg4)

    return val

    # win32gui.PumpMessages()  