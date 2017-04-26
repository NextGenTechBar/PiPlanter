import tweepy
import schedule
import time
import os
from picamera import PiCamera
from auth import consumer_key, consumer_secret, key, secret
from time import strftime, localtime

cam = PiCamera()
cam.resolution = (1024, 1024)
cam.framerate = 30
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)
# All the code relating to twitter lies here. Before you make your own changes,
# make sure you've added your own API keys.

# positive and negative reflect the possible responses to vote with.
# These can be changed as needed/desired.
positive = 'yes', 'yep', 'yepp', 'yeppers', 'yup', 'yupp', 'yuuup', 'ye', 'yee', 'ofc', 'yass'
negative = 'no', 'nope', 'nop', 'not on your nelly', 'no way', 'not a chance', 'hell no', 'no please', 'nu', 'nein'
# where is the image we're uploading going to be at? this case: it's nested. heavily.
videoRaw = '~/pi.h264'
video = '~/pi.mp4'
global lastDayWatered
lastDayWatered = "N/A"

def cameraCapture():  # this is the part that takes the photo at a specified resolution
    # and saves it the image to be uploaded to Twitter
    # It'll also convert the resulting raw .h264 file to a more proper .mp4 file via MP4box
    cam.start_recording(videoRaw)
    cam.wait_recording(10)
    cam.stop_recording()
    time.sleep(30)
    os.system('MP4Box -fps 30 -add {} {}', videoRaw, video)

def startPeriod():  # this is the tweet that signifies the start of the voting period.
    timeNow = strftime('%a, %b %d %Y', localtime())
    global timeStartPeriod
    timeStartPeriod = strftime('%Y-%m-%d', localtime())
    # Your message. We need this to update every time we tweet, hence why it's here.
    # If you don't change anything (add/remove search terms), keep the piplant.cu.cc link, it's there to help users on what they can tweet.
    # If you do change anything (add/remove search terms), feel free to put in your own website or some short way of describing how people can respond.
    message = "It's {} now! Last watered on {}. Vote using #waterbecky and a word like YES or NO! Learn more @ piplant.cu.cc".format(
        timeNow, lastDayWatered)
    api.update_with_media(filename=video, status=message)
    print(message)


def pollPeriod():  # this is the hard part: searching for relevant tweets, comparing the users of found tweets to sets to ensure they don't get counted for multiple votes, etc.
    # the basis of pollPeriod(). if yes>no, we water. if no>yes, we don't. if yes=no, we issue a tiebreaker.
    yes = 0
    no = 0
    # sets an end time should tweepy's since and until tags work correctly
    timeEndPeriod = strftime('%Y-%m-%d', localtime())
    ignoreUserY = set()
    ignoreUserN = set()

    # runs the search queries to gather the votes for positive and negative votes, adds 1 to their respective variable (positive adds to yes, negative adds to no)
    # and if the user has been caught voting already, counts only the most recent vote.
    print('Yes from:')
    for votes in positive:
        votesPos = api.search(q='waterbecky {}'.format(votes))
        for content in votesPos:
            # print(content.author._json['screen_name'])
            username = content.author._json['screen_name']
            if username not in ignoreUserY:
                print(username)
                ignoreUserY.add(username)
                yes += 1
            else:
                yes = yes
    time.sleep(900)  # To help prevent Twitter errors from searching too many damn times in a row, we wait at least 15 minutes until we start the negative searches
                    # Without this, it's highly likely we'd encounter an error from Twitter due to us searching too many times
    print('No from:')
    for votes in negative:
        votesNeg = api.search(q='watertaila {}'.format(votes))
        for content in votesNeg:
            # print(content.author._json['screen_name'])
            username = content.author._json['screen_name']
            if username not in ignoreUserN:
                print(username)
                ignoreUserN.add(username)
                no += 1
            else:
                no = no

    # Just printing to the console/terminal what the results of the votes are. Feel free to comment this code out after you've done
    # initial testing to verify that it works for you.
    print()
    print('=====Total Votes=====')
    print('{} to water.'.format(yes))
    print('{} to not water.'.format(no))

    # The actual decision making process.
    # If we get more votes to water, we'll tweet out that we got more votes to water than not.
    if yes > no:
        print("\nWe're watering today!")
        api.update_status(status="We had more votes to water than to not. We're watering today!")
        lastDayWatered = strftime("%a")
    # If we got more votes to not water, we'll tweet out that we got more votes to not water than to water.
    if no > yes:
        print("\nWe're not watering today!")
        api.update_status(status="We had more votes to not water than to. We're not watering today!")
    # If somehow an equal amount of people voted to water and to not water, we'll run a simple tiebreaker that will determine
    # we water or if we don't water. If tiebreaker returns 1, we water. If 0, we don't.
    if yes == no:
        print("\nWe had equal votes today.")
        random.seed(version=2)
        tiebreaker = random.randrange(0, 1)
        if tiebreaker == 1:
            print("\nWe're watering today!")
            api.update_status(status="We had more votes to water than to not. We're watering today!")
            lastDayWatered = strftime("%a")
        if tiebreaker == 0:
            print("\nWe're not watering today!")
            api.update_status(status="We had more votes to not water than to. We're not watering today!")


# The schedule code to say when we'll run the code and at what time of day. If you want to run the code at different times, feel free to change it.
# Keep in mind schedule relies on your SYSTEM TIME, not the time of Twitter or anything else. Make sure your system time is in the correct timezone
# before complaining that this doesn't work.
schedule.every().day.at("07:00").do(cameraCapture())
schedule.every().day.at("03:00").do(pollPeriod)
schedule.every().day.at("07:30").do(startPeriod)

while True:
    schedule.run_pending()
    time.sleep(1)
