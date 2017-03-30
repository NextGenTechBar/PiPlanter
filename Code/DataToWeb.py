import tweepy
from datetime import datetime
import time
import os
import subprocess

import Log
LogType = 'DataToWeb'

def TryTweet(image, imagelocation, text):
	for i in range(10):
		try:
			consumer_key=""
			consumer_secret=""
			access_token=""
			access_token_secret=""
			auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_token, access_token_secret)
			api = tweepy.API(auth)
		
			Log.ConsoleDebug(LogType,'Attempt [' + str(i) + '] To Tweet: ' + text + ' , image = ' + str(image)) 
			if image == True:
				output = api.update_with_media(imagelocation, text)
			if image == False:
				output = api.update_status(text)
			break
		
		except tweepy.error.TweepError as e:
			Log.ConsoleDebug(LogType,'Tweet Failed, Retrying')
			Log.ConsoleDebug(LogType,'Twitter Error: ' + str(e))
			i = i + 1
			time.sleep(15)

	if i < 10:
		Log.ConsoleDebug(LogType,'Tweet Sent After ' + str(i) + ' Attempts, Details: Actual Text [ ' + str(output.text) + '] URL: https://twitter.com/piplanter_bot/status/' + str(output.id) )

	if i == 10:
		Log.ConsoleDebug(LogType,'Tweet Was a Failure')

def UploadVideo(video,email,password):
    humantime = str(datetime.now().strftime("%m/%d/%Y"))
    title = 'Time Lapse of Plant Growth in the 24 Hours Before ' + str(humantime)
    description = 'Confused? http://www.esologic.com/piplanter'
    category = 'Tech'
    keywords = 'piplanter'
    uploadcommand = 'youtube-upload --email=' + email + ' --password=' + password + ' --title="' + title +'"'+ ' --description="' + description + '"' + ' --category=' + category + ' --keywords=' + keywords + ' ' + os.path.normpath(video)
    Log.ConsoleDebug(LogType,'Upload Command: ' + uploadcommand)
 
    for i in range(10):
        try:
            Log.ConsoleDebug(LogType,'Attempt [' + str(i) + '] To Upload: ' + str(video))
            proc = subprocess.Popen(uploadcommand, shell=True, stdout=subprocess.PIPE)
            output = proc.stdout.read()
            break
 
        except:
            Log.ConsoleDebug(LogType,'Upload Failed, Retrying')
            Log.ConsoleDebug(LogType,'Upload Error: ' + str(output))
            i = i + 1
            time.sleep(15)
 
    if i < 10:
        Log.ConsoleDebug(LogType,'Uploaded After ' + str(i) + ' Attempts, Details: URL [ ' + str(output) + ']' )
        return output
 
    if i == 10:
        Log.ConsoleDebug(LogType,'Upload Was a Failure')
        return 'Upload was a Failure'