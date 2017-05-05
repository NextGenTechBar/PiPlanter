import MySQLdb
from datetime import datetime
import time
import os
#import RPI.GPIO as GPIO
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import shutil
import smbus

import Log
import RenderData
LogType = 'Master'

bus = smbus.SMBus(1)
address = 0x04

def FirstTimeSetup():
	global cycle
 
	Log.ConsoleDebug(LogType,'---------------- NEW INSTANCE OF TESTPIPIPLANTER ----------------')
 
	MySQL_Commands = {1 : 'CREATE DATABASE IF NOT EXISTS TestPiPlanter_DB', 2: "GRANT ALL ON `TestPiPlanter_DB`.* TO 'piplanter'@'localhost' IDENTIFIED BY 'password'", 3: 'USE TestPiPlanter_DB' }
	for i in MySQL_Commands.itervalues():
		Log.ConsoleDebug(LogType,'MYSQL COMMAND: ' + i)
		cursor.execute(i)

	MySQLTableSetup(False,'Daily',True)
	VisualLocationSetup(True,'dontcare')
	cycle = 0
	
	#Hardware.WriteLEDs(0,0,0)
	#Hardware.WriteLEDs(255,0,255)
	Log.ConsoleDebug(LogType,'Setup Complete')


def MySQLTableSetup(full,kind,first):
	global MySQL_Tables
	now = datetime.now().strftime("%m_%d_%Y__%I_%M_%S%p")
	if first == True:
		#MySQL_Tables = { 'MySQLTable_Daily' : 'DailyTable' + now, 'MySQLTable_Weekly' : 'WeeklyTable' + now, 'MySQLTable_Monthly' : 'MonthlyTable' + now}
		MySQL_Tables = { 'MySQLTable_Daily' : 'DailyTable', 'MySQLTable_Weekly' : 'WeeklyTable', 'MySQLTable_Monthly' : 'MonthlyTable'}

                #Uncomment later
		#CreateTables = {0: "CREATE TABLE " + MySQL_Tables['MySQLTable_Daily'] + "(Sample_Number INT NOT NULL AUTO_INCREMENT PRIMARY KEY,Time VARCHAR(100),soil_water VARCHAR(100))", 1 : "CREATE TABLE " + MySQL_Tables['MySQLTable_Weekly'] + "(Sample_Number INT NOT NULL AUTO_INCREMENT PRIMARY KEY,Time VARCHAR(100),soil_water VARCHAR(100))" , 2 : "CREATE TABLE " + MySQL_Tables['MySQLTable_Monthly'] + "(Sample_Number INT NOT NULL AUTO_INCREMENT PRIMARY KEY,Time VARCHAR(100),soil_water VARCHAR(100))"}
		#for i in CreateTables.itervalues():
			#Log.ConsoleDebug(LogType,'MYSQL COMMAND: ' + i)
			#cursor.execute(i)

	elif first == False:
		if kind == 'Daily':
			Log.ConsoleDebug(LogType,'Daily Database Name Has Been Updated')
			MySQL_Tables['MySQLTable_Daily'] = 'DailyTable_' + now
			Log.ConsoleDebug(LogType,MySQL_Tables['MySQLTable_Daily'])
			CreateTable = "CREATE TABLE " + MySQL_Tables['MySQLTable_Daily'] + "(Sample_Number INT NOT NULL AUTO_INCREMENT PRIMARY KEY,Time VARCHAR(100),P_MST0 VARCHAR(100),P_MST1 VARCHAR(100),A_TMP0 VARCHAR(100),A_LDR0 VARCHAR(100))"
		elif kind == 'Weekly':
			Log.ConsoleDebug(LogType,'Daily Database Name Has Been Updated')
			MySQL_Tables['MySQLTable_Weekly'] = 'WeeklyTable_' + now
			Log.ConsoleDebug(LogType,MySQL_Tables['MySQLTable_Weekly'])
			CreateTable = "CREATE TABLE " + MySQL_Tables['MySQLTable_Weekly'] + "(Sample_Number INT NOT NULL AUTO_INCREMENT PRIMARY KEY,Time VARCHAR(100),P_MST0 VARCHAR(100),P_MST1 VARCHAR(100),A_TMP0 VARCHAR(100),A_LDR0 VARCHAR(100))"
		elif kind == 'Monthly':
			Log.ConsoleDebug(LogType,'Daily Database Name Has Been Updated')
			MySQL_Tables['MySQLTable_Monthly'] = 'MonthlyTable_' + now
			Log.ConsoleDebug(LogType,MySQL_Tables['MySQLTable_Monthly'])
			CreateTable = "CREATE TABLE " + MySQL_Tables['MySQLTable_Monthly'] + "(Sample_Number INT NOT NULL AUTO_INCREMENT PRIMARY KEY,Time VARCHAR(100),P_MST0 VARCHAR(100),P_MST1 VARCHAR(100),A_TMP0 VARCHAR(100),A_LDR0 VARCHAR(100))"

		Log.ConsoleDebug(LogType,'MYSQL: ' + CreateTable)
		cursor.execute(CreateTable)

	Log.ConsoleDebug(LogType,'Current Daily: ' + MySQL_Tables['MySQLTable_Daily'])
	Log.ConsoleDebug(LogType,'Current Weekly: ' + MySQL_Tables['MySQLTable_Weekly'])
	Log.ConsoleDebug(LogType,'Current Monthly: ' + MySQL_Tables['MySQLTable_Monthly'])
 

def VisualLocationSetup(first,kind):
        global VisualLocation
        now = datetime.now().strftime("%m_%d_%Y__%I_%M_%S%p")
 
        runninglocation = str(os.getcwd())
        if first == True:
 
                Log.ConsoleDebug(LogType,'Creating Video Directory')
                if not os.path.exists(runninglocation + '/videos/'):
                        os.makedirs(runninglocation + '/videos/')
                        Log.ConsoleDebug(LogType,'Video Directory Created')
                else:
                        Log.ConsoleDebug(LogType,'Video Directory Already Exists')
 
                Log.ConsoleDebug(LogType,'Creating Daily Video Directory')
                if not os.path.exists(runninglocation + '/videos/dailys/'):
                        os.makedirs(runninglocation + '/videos/dailys/')
                else:
                        Log.ConsoleDebug(LogType,'Daily Video Directory Already Exists')
 
                Log.ConsoleDebug(LogType,'Creating Image Directory')
                if not os.path.exists(runninglocation + '/images/'):
                        os.makedirs(runninglocation + '/images/')
                else:
                        Log.ConsoleDebug(LogType,'Image Directory Already Exists')
 
                Log.ConsoleDebug(LogType,'Creating Daily Image Directory')
                if not os.path.exists(runninglocation + '/images/dailys/'):
                        os.makedirs(runninglocation + '/images/dailys/')
                else:
                        Log.ConsoleDebug(LogType,'Daily Image Directory Already Exists')
 
                Log.ConsoleDebug(LogType,'Creating Graph Directory')
                if not os.path.exists(runninglocation + '/graphs/'):
                        os.makedirs(runninglocation + '/graphs/')
                else:
                        Log.ConsoleDebug(LogType,'Graph Directory Already Exists')
 
                Log.ConsoleDebug(LogType,'Updating All Current Visual Directories')
                VisualLocation = {'CurrentImageDirectory' : runninglocation + '/images/dailys/' + 'CurrentImageDirectory_' + now + '/' , 'CurrentVideoDirectory' : runninglocation + '/videos/dailys/' + 'CurrentVideoDirectory_' + now + '/' , 'CurrentGraphDirectory' : runninglocation + '/graphs/' + 'CurrentGraphDirectory_' + now + '/' }
 
                for i in VisualLocation.itervalues():
                        Log.ConsoleDebug(LogType,'Making Directory: ' + i)
                        os.makedirs(i)
 
        if first == False:
                Log.ConsoleDebug(LogType,'Updating Location Of ' + kind + ' Directory')
                if kind == 'Image':
                        VisualLocation['CurrentImageDirectory'] = runninglocation + '/images/dailys/' + 'CurrentImageDirectory_' + now + '/'
                        Log.ConsoleDebug(LogType,'Making Directory: ' + VisualLocation['CurrentImageDirectory'])
                        os.makedirs(VisualLocation['CurrentImageDirectory'])
 
                elif kind == 'Video':
                        VisualLocation['CurrentVideoDirectory'] = runninglocation + '/videos/dailys/' + 'CurrentVideoDirectory_' + now + '/'
                        Log.ConsoleDebug(LogType,'Making Directory: ' + VisualLocation['CurrentVideoDirectory'])
                        os.makedirs(VisualLocation['CurrentVideoDirectory'])
 
                elif kind == 'Graph':
                        VisualLocation['CurrentGraphDirectory'] = runninglocation + '/graphs/' + 'CurrentGraphDirectory_' + now + '/'
                        Log.ConsoleDebug(LogType,'Making Directory: ' + VisualLocation['CurrentGraphDirectory'])
                        os.makedirs(VisualLocation['CurrentGraphDirectory'])
 
        Log.ConsoleDebug(LogType,'Current Image Directory' + VisualLocation['CurrentImageDirectory'])
        Log.ConsoleDebug(LogType,'Current Video Directory' + VisualLocation['CurrentVideoDirectory'])
        Log.ConsoleDebug(LogType,'Current Graph Directory' + VisualLocation['CurrentGraphDirectory'])
 
        return 0
 


def aLoop():
        Log.ConsoleDebug(LogType,"Starting aLoop")
        print("in aLoop")
        global cycle
        sampleSoilWater()
        #SampleAllSensors(10,'MySQL')
        Log.ConsoleDebug(LogType,str(sampleSoilWater()))
        
        #imagetext = SampleAllSensors(10,'Image Overlay') + ' ' + datetime.now().strftime("%I:%M:%S%p %m/%d/%Y")
        #image = Hardware.CaptureImage(VisualLocation['CurrentImageDirectory'],cycle,False,imagetext)
        
        time.sleep(5)
        #tweet = SampleAllSensors(10,'Twitter') + " #PiPlanter"
        
        #DataToWeb.TryTweet(True,image,tweet)
        
        cycle = cycle + 1
        Log.ConsoleDebug(LogType,'aLoop Complete')
        
def bloop():
	Log.ConsoleDebug(LogType,"Starting bLoop")
	
	graphlocation = RenderData.RenderGraph(MySQL_Tables['MySQLTable_Weekly'],VisualLocation['CurrentGraphDirectory'])
	
	#video = RenderData.RenderVideo(VisualLocation['CurrentImageDirectory'],VisualLocation['CurrentVideoDirectory'])
 	
	#yt_url = DataToWeb.UploadVideo(video,"","")

	#tweet1 = 'Graph of Week So Far: Moisture % - Blue, Ambient Light % - Yellow, Temp DF - Red  http://www.esologic.com/piplanter'
	#tweet2 = 'Time Lapse Video of Previous Three Days: ' + yt_url
 
	#DataToWeb.TryTweet(True,graphlocation,tweet1)
	#DataToWeb.TryTweet(False,'',tweet2)
  
	Log.ConsoleDebug(LogType,'Removing Old Images, Graphs and Videos')
	
	os.system("rm -rf " + VisualLocation['CurrentImageDirectory'])
	os.system("rm -rf " + VisualLocation['CurrentGraphDirectory'])
	os.system("rm -rf " + VisualLocation['CurrentVideoDirectory'])
	
	Log.ConsoleDebug(LogType,'Old Images, Graphs and Videos Removed')
	
	VisualLocationSetup(False,'Image')
	VisualLocationSetup(False,'Video')
	VisualLocationSetup(False,'Graph')
	
	Log.ConsoleDebug(LogType,'bLoop Complete')


def sampleSoilWater():
        global MySQL_Tables
        number = bus.read_byte(address)
        #cursor.execute("INSERT INTO " + MySQL_Tables['MySQLTable_Daily'] + "(Time, soil_water)" + " VALUES(NOW()" + "," + str(number) + ')')
        cursor.execute("INSERT INTO " + MySQL_Tables['MySQLTable_Daily'] + "(Time, soil_water)" + " VALUES(NOW()"  +"," + str(number) +')')
        user.commit()
        cursor.execute("INSERT INTO " + MySQL_Tables['MySQLTable_Weekly'] + "(Time, soil_water)" + " VALUES(NOW()" + "," + str(number) +')')
        user.commit()
        cursor.execute("INSERT INTO " + MySQL_Tables['MySQLTable_Monthly'] + "(Time, soil_water)" + " VALUES(NOW()" +  "," + str(number) +')')
        user.commit()
        return number
        IOErrorIOError

        
if __name__ == '__main__':
        global MySQLTables
        global VisualLocation


        user = MySQLdb.connect(host="localhost",user="root",passwd="")
        cursor = user.cursor()

        scheduler = BlockingScheduler()
        scheduler.add_job(aLoop, 'interval', minutes=5)
        scheduler.add_job(aLoop, 'interval', days=1)

        FirstTimeSetup()

        aLoop()
        bloop()

        scheduler.start()

