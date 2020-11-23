import sys
# sys.path.append("C:\Program Files\TechnoStar\Jupiter-Pre_5.0")
sys.path.append("./")
import JPT
from client import get_res_from_socket
from PSJ_Wrapper import get_res_from_jupiter

print(JPT)
# propPath = get_res_from_socket()
propPath = get_res_from_jupiter()
print(propPath)
