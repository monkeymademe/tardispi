#!/usr/bin/env python

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import explorerhat
import unicornhat as unicorn
#import picamera
import sys, subprocess, urllib, time, math, json, datetime
import config
import random

tardisstats = 0

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(1.0)
width,height=unicorn.get_shape()

def pooprainbows(pin):
        i = 0.0
        offset = 30
        explorerhat.motor.forwards(100)
        t_end = time.time() + 10
        while time.time() < t_end:
                i = i + 0.3
                for y in range(height):
                        for x in range(width):
                                r = 0
                                g = 0
                                r = (math.cos((x+i)/2.0) + math.cos((y+i)/2.0)) * 64.0 + 128.0
                                g = (math.sin((x+i)/1.5) + math.sin((y+i)/2.0)) * 64.0 + 128.0
                                b = (math.sin((x+i)/2.0) + math.cos((y+i)/1.5)) * 64.0 + 128.0
                                r = max(0, min(255, r + offset))
                                g = max(0, min(255, g + offset))
                                b = max(0, min(255, b + offset))
                                unicorn.set_pixel(x,y,int(r),int(g),int(b))
                unicorn.show()
                time.sleep(0.01)
        explorerhat.motor.forwards(0)
	unicorn.clear()
	unicorn.show()

def takeshot():
	with picamera.PiCamera() as camera:
		camera.resolution = (1024, 768)
                camera.start_preview()
		camera.hflip = True
		camera.vflip = True
                # Camera warm-up time
                time.sleep(2)
                camera.capture('tweetthis.jpg')

def parsetweet(tweet):
	tweetId = tweet['id']
        username = tweet['user']['screen_name'].encode('utf-8')
        now = datetime.datetime.now()
	date = now.strftime("%H:%M:%S %d-%m-%Y")
	text = tweet['text'].encode('utf-8')
	tweetdata = {'tweetId': tweetId, 'username': username, 'date': date, 'text': text};	
	return tweetdata

def replywithtext(tweetdata, msg):
	if len(msg) <= 140:
		api.update_status(status=msg, in_reply_to_status_id=tweetdata['tweetId'])
        else:
                print "tweet not sent. Too long. 140 chars Max."

def replywithpic(tweetdata):
	tweetnum = random.randint(1,5)
	if tweetnum == 1:
		msg = "Hey @%s you know the Tardis is bigger on the inside! Current Tardis time is: %s" % (tweetdata['username'], tweetdata['date'])
		file = 'tardis_1.jpg'
	if tweetnum == 2:
		msg = "@%s I have been this small before. Don't worry it worked out ok that time... Might have left a few people feeling a little flat. Current Tardis time is: %s" % (tweetdata['username'], tweetdata['date'])
		file = 'tardis_2.jpg'
	if tweetnum == 3:
                msg = '@%s At some point in the future I might explode... Well not today... maybe soon... Current Tardis time is: %s' % (tweetdata['username'], tweetdata['date'])
                file = 'tardis_3.jpg'
        if tweetnum == 4:
                msg = "@%s I don't like traffic! I am a timemachine not a old ford roadster! Current Tardis time is: %s" % (tweetdata['username'], tweetdata['date'])
                file = 'tardis_4.jpg'
        if tweetnum == 5:
                msg = "@%s Don't Blink! Current Tardis time is: %s" % (tweetdata['username'], tweetdata['date'])
                file = 'tardis_5.jpg'
	if len(msg) <= 280:
		api.update_with_media(file, status=msg, in_reply_to_status_id=tweetdata['tweetId'])
        else:
		print "tweet not sent. Too long. 280 chars Max."

class StdOutListener(StreamListener):

        def on_data(self, data):
		tweet = json.loads(data)
		# Print Username
		print(tweet['user']['name']).encode('utf-8')
		# Print Text from tweet *note* encode is used because of speical charaters causing exception
		print(tweet['text']).encode('utf-8')
 		# ----- do something
		tweetdata = parsetweet(tweet)
		if "#spintardis" in tweetdata['text']:
			pooprainbows(tweetdata)
			replywithpic(tweetdata)
        	return True

        def on_error(self, status):
		# Print errors numbers
		if status == '403':
			print('User forcing duplication:  %s' % status)
		else:
			print(status)

if __name__ == '__main__':
		# Button wait
	explorerhat.input.four.changed(pooprainbows)
		# OAuth to Twitter
	l = StdOutListener()   
 	auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    	auth.secure = True
    	auth.set_access_token(config.access_token, config.access_token_secret)
	api = tweepy.API(auth)

		# Start Stream Tracking
    	stream = Stream(auth, l)
		#user = ["robinjamberlin"]
	keywords = ["#spintardis"]
    	stream.filter(track=keywords)
