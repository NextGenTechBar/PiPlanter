import os
from datetime import datetime
import time
import subprocess

import Log
LogType = 'RenderData'

def RenderGraph(table,location):
    Log.ConsoleDebug(LogType,'Rendering Graph')
    rendercommand = 'php ' + str(os.getcwd()) + '/WPI_PChart_0_0_1.php ' + table + ' ' + location
    Log.ConsoleDebug(LogType,'Running Command: ' + rendercommand)
    proc = subprocess.Popen(rendercommand, shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()
    Log.ConsoleDebug(LogType,'Output File: ' + script_response)
    Log.ConsoleDebug(LogType,'Rendering Complete')
    return script_response
  
def RenderVideo(infolder,outfolder):
	Log.ConsoleDebug(LogType,'Rendering Video')
	outputfile = outfolder + str(datetime.now().strftime("%m_%d_%Y__%I_%M_%S%p")) + '_VIDEO.avi'
	Log.ConsoleDebug(LogType,'Attempting To Render: ' + outputfile)
	render_command = 'sudo mencoder mf://' + str(infolder) + '*.jpg -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -mf type=jpeg:fps=15 -o ' + outputfile
	os.system(render_command)
	Log.ConsoleDebug(LogType,'Deleting frames')
	deletefiles = 'sudo rm -rf ' + infolder
	os.system(deletefiles)
	Log.ConsoleDebug(LogType,'Video Render Complete, File: ' + outputfile)
	return outputfile
