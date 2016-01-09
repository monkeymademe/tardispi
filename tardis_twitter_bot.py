import tweepy

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import explorerhat
import sys, subprocess, urllib, time, tweepy, json
import config

class StdOutListener(StreamListener):
	
	def spintardis():
                explorerhat.motor.forwards(10)
                time.sleep(10)
                explorerhat.motor.forwards(0)	
		return True

        def on_data(self, data):
		text = json.loads(data)
		# Print Username 
		print(text['user']['name']).encode('utf-8')
		# Print Text from tweet *note* encode is used because of speical charaters causing exception
		print(text['text']).encode('utf-8')
 		# If I wanted to add something to pipsta its gonna be here
		if "tardislightson" in text['text'].encode('utf-8'):
			explorerhat.motor.backwards(100)
                if "tardislightsoff" in text['text'].encode('utf-8'):
                	explorerhat.motor.backwards(0)
        	return True

        def on_error(self, status):
		# Print errors numbers
        	print(status)

		

if __name__ == '__main__':
	# OAuth to Twitter
	l = StdOutListener()   
 	auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    	auth.secure = True
    	auth.set_access_token(config.access_token, config.access_token_secret)

	# Start Stream Tracking
    	stream = Stream(auth, l)
	user = ["robinjamberlin"]
	keywords = ["#tardislightson", "#tardislightsoff"]
    	stream.filter(track=keywords)
