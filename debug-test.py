import debugpy
import sys
# sys.path.append("C:\Program Files\TechnoStar\Jupiter-Pre_5.0")
sys.path.append("./")
import JPT

exe = sys.executable
try:
    # sys.executable = "C:\Program Files\TechnoStar\Jupiter-Pre_5.0\python.exe"
    debugpy.listen(5689)

    print("Waiting for debugger attach")
    debugpy.wait_for_client()
    debugpy.breakpoint()
    print('break on this line 1')
    print('break on this line 2')
    print('break on this line 3')
    print('break on this line 4')
    print(JPT)
    # propPath = JPT.GetAppPathInfo(JPT.PathType.PROGRAM_PATH)
    propPath = JPT.fib2(1000)
    print(propPath)
    # Geometry.Part.Cube(dlVdOrigin=[0,0,0], dlVdLength=[0.01,0.01,0.01], ilVlNodeCnt=[10,10,10], strPartName="Cube_1", iColPart=7105764, crCoord=None)
finally:
    sys.executable = exe
# 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1

