import tweepy

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import explorerhat
import picamera
import sys, subprocess, urllib, time, tweepy, json, datetime
import config

tardisstats = 0

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

def replywithpic(tweetdata, status):
	if status == 'turned-on':
		msg = '@%s Lights, camera, action! Current Tardis time is: %s' % (tweetdata['username'], tweetdata['date'])
	if status == 'turned-off':
		msg = '@%s Lightsout time for sleep! Current Tardis time is: %s' % (tweetdata['username'], tweetdata['date'])
	file = 'tweetthis.jpg'
        if len(msg) <= 140:
		api.update_with_media(file, status=msg, in_reply_to_status_id=tweetdata['tweetId'])
        else:
		print "tweet not sent. Too long. 140 chars Max."

class StdOutListener(StreamListener):
	
        def on_data(self, data):
		tweet = json.loads(data)
		global tardisstats 
		# Print Usernam[Be 
		print(tweet['user']['name']).encode('utf-8')
		# Print Text from tweet *note* encode is used because of speical charaters causing exception
		print(tweet['text']).encode('utf-8')
 		# ----- do something
		tweetdata = parsetweet(tweet)
		if "#tardislightson" in tweetdata['text']:
			status = "turned-on"
			explorerhat.motor.backwards(100)
			takeshot()
			replywithpic(tweetdata, status)
		 	tardisstats = tweetdata
			tardisstats['status'] = status
                if "#tardislightsoff" in tweetdata['text']:
			status = "turned-off"
                	explorerhat.motor.backwards(0)
			takeshot()
			replywithpic(tweetdata, status)
			tardisstats = tweetdata
                       	tardisstats['status'] = status
		#if "tardisligthson" and "tardislightsoff" in tweetdata['text']:
		#	msg = '@%s stop confusing me... Lights off, lights on... Make up your mind!' % tweetdata['username']
		#	replywithtext(tweetdata, msg)
		if "#tardisstatus" in tweetdata['text']:
			msg = '@%s I was last turned %s by %s at %s' % (tweetdata['username'], tardisstats['status'], tardisstats['username'], tardisstats['date'])
			replywithtext(tweetdata, msg) 
        	return True

        def on_error(self, status):
		# Print errors numbers
		if status == '403':
			print('User forcing duplication:  %s' % status)
		else:
			print(status)

if __name__ == '__main__':
	# OAuth to Twitter
	l = StdOutListener()   
 	auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    	auth.secure = True
    	auth.set_access_token(config.access_token, config.access_token_secret)
	api = tweepy.API(auth)

	# Start Stream Tracking
    	stream = Stream(auth, l)
	#user = ["robinjamberlin"]
	keywords = ["#tardislightson", "#tardislightsoff", "#tardisstatus", "#testtestest"]
    	stream.filter(track=keywords)
