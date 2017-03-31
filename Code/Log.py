import sys
from datetime import datetime
import os

def ConsoleDebug(type,input):
    debug = '[' + datetime.now().strftime("%m-%d-%Y_%I-%M-%S-%p") + '] ' + type + ': ' + input
    print debug
    file = open(str(os.getcwd()) + "/PiPlanterLog.txt", "a")
    file.write(debug + "\n")
    file.close()
