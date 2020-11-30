import os
import threading
import time
from jupiterutils import *

def open_Jupiter():
    path = r"C:\Program Files\TechnoStar\Jupiter-Pre_5.0"
    os.chdir(path)
    os.system("DCAD_main.exe")
    time.sleep(1)

t1 = threading.Thread(target=open_Jupiter) 
t1.start()

time.sleep(10)

JPT.ClearLog()

# list all message box types
JPT.Debugger(JPT.MsgBoxType.values)

# create message box type information-yes-no-cancel
anwser = JPT.MessageBoxPSJ("test message", JPT.MsgBoxType.MB_INFORMATION_YESNOCANCEL)

if anwser == "YES":
    print ("you selected yes")
elif anwser == "NO":
    print ("you selected no")
else: 
    print ("you selected cancel")    

JPT.QuitApplication()