import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
from datetime import datetime
import spidev
import os
import time
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import serial

import Log
LogType = 'Hardware'

portfas = "/dev/ttyACM0"

print portfas

Log.ConsoleDebug(LogType,'Opening Serial Port')
port =serial.Serial(
	portfas,
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	writeTimeout = 0,
	timeout = 10,
	rtscts=False,
	dsrdtr=False,
	xonxoff=False)

port.open() 
Log.ConsoleDebug(LogType,'Serial Port Opened')
 
def SerialHandShake(input):
	Log.ConsoleDebug(LogType,'Attempting to Send: ' + input)
	port.write(input)

	try:
		time.sleep(.01)
		serin = port.readline().rstrip()
		Log.ConsoleDebug(LogType,'Message sent, recived: ' + serin)
	except:
		pass
		
	while True:
		if len(serin) > 0:
			Log.ConsoleDebug(LogType,'Serial Handshake Successful!')
			return serin
			break

		else:
			Log.ConsoleDebug(LogType,'Serial Handshake Failed, Retrying.')
			serin = port.readline().rstrip()
	
	time.sleep(1)

#returns a usable numerical value from the ADC
def PollSensor(sensor,precision):
	Log.ConsoleDebug(LogType,'Polling ' + sensor + ' ' + str(precision) + ' Times')
	pins = {'P_MST0' : 0, 'P_MST1' : 1, 'A_LDR0' : 2, 'A_TMP0' : 3}
	send = "noise,0," + str( pins[sensor] )+ "," + str(precision) + "$"
	output = SerialHandShake(send)
	return str(output)
 
#pumps a given amount of water from a given pump
def PumpWater(pump,volume):
	Log.ConsoleDebug(LogType,'Pumping ' + str(volume) + 'L with ' + str(pump))
	pumps = {'PUMP0' : 0, 'PUMP1' : 1}
	send = "noise,2," + str(pumps[pump]) + ',' + str(volume) + "$" 
	output = SerialHandShake(send)
	return output
	
def WriteLEDs(R,G,B):
	Log.ConsoleDebug(LogType,'Changing LEDs to: R: ' + str(R) + ' G: ' + str(G) + ' B: ' + str(B))
	send = "noise,1," + str(R) + ',' + str(G) + "," + str(B) + "$"
	output = SerialHandShake(send)
 
def CaptureImage(dir,cycle,high_quality,text):
	image = dir + str(cycle).zfill(4) + '.jpg'
	if high_quality == False:
		picture_command = 'raspistill -q 10 -vf -o  ' + image
	if high_quality == True:
		picture_command = 'raspistill -q 100 -vf -o  ' + image
	WriteLEDs(255,255,255)
	os.system(picture_command)
	WriteLEDs(255,0,255)
	Log.ConsoleDebug(LogType,'Image Captured, High Quality = ' + str(high_quality) + ', Image: ' + str(image))

	Log.ConsoleDebug(LogType,'Start Image Edit')
	font = ImageFont.truetype("/srv/www/lib/pChart/fonts/pf_arma_five.ttf",60)
	Log.ConsoleDebug(LogType,'Opening Image for editing: ' + image)
	im1=Image.open(image)
	width,height = im1.size
	Log.ConsoleDebug(LogType,'Image Width: ' + str(width) + ' Image Height: ' + str(height))
	wloc = 20
	hloc = height - 110
	Log.ConsoleDebug(LogType,'Text Location (W,H): ' + str(wloc) + ',' + str(hloc))
	draw = ImageDraw.Draw(im1)
	draw.text((wloc, hloc),text,(255,255,0),font=font)
	draw = ImageDraw.Draw(im1)
	im1.save(image)
	Log.ConsoleDebug(LogType,'Image Processed')

	return image    