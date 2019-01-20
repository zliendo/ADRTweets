from __future__ import absolute_import, print_function, unicode_literals

import itertools, time
import tweepy, copy 
import Queue, threading
from datetime import datetime
import json

from streamparse.spout import Spout

################################################################################
# Twitter credentials
################################################################################
twitter_credentials = {  

    "consumer_key"        :  "******",
    "consumer_secret"     :  "******",
    "access_token"        :  "******",
    "access_token_secret" :  "******",
}

def auth_get(auth_key):
    if auth_key in twitter_credentials:
        return twitter_credentials[auth_key]
    return None

################################################################################
# Class to listen and act on the incoming tweets
################################################################################
class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, listener):
        self.listener = listener
        super(self.__class__, self).__init__(listener.tweepy_api())

    #def on_status(self, status):
    def on_data(self, data):
        tweet = json.loads(data)
        twitter_id = tweet['user']['id']
        tweet_id = tweet['id']
        tweet_date = tweet['created_at']
        tweet_date_string =  datetime.strptime(tweet_date, '%a %b %d %X +0000 %Y').strftime('%Y-%m-%d')
        tweet_text = tweet['text']

        tweet_fields = (tweet_id, twitter_id, tweet_date_string, tweet_text)
        #self.listener.queue().put(status.text, timeout = 0.01)
        self.listener.queue().put(tweet_fields, timeout = 0.01)
        return True
  
    def on_error(self, status_code):
        return True # keep stream alive
  
    def on_limit(self, track):
        return True # keep stream alive

class Tweets(Spout):

    def initialize(self, stormconf, context):
        
        self._queue = Queue.Queue(maxsize = 100)

        consumer_key = auth_get("consumer_key") 
        consumer_secret = auth_get("consumer_secret") 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        if auth_get("access_token") and auth_get("access_token_secret"):
            access_token = auth_get("access_token")
            access_token_secret = auth_get("access_token_secret")
            auth.set_access_token(access_token, access_token_secret)

        self._tweepy_api = tweepy.API(auth)

        # Create the listener for twitter stream
        listener = TweetStreamListener(self)

        # get search option
        if "topic" in stormconf:
            search_topic = stormconf["topic"]
        else:
            search_topic = "tamiflu" #default 
        self.search_topic= search_topic
		
        # Create the stream and listen for english tweets
        stream = tweepy.Stream(auth, listener, timeout=None)

        # use search topic provided 
        stream.filter(languages=["en"], track=[search_topic], async=True)
       
    def queue(self):
        return self._queue

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        try:
            tweet = self.queue().get(timeout = 0.1) 
            if tweet:
                self.queue().task_done()
                tweet_id = tweet[0]
                twitter_user_id = tweet[1]
                tweet_date_string= tweet[2]
                tweet_text = tweet[3]
                self.emit([self.search_topic, tweet_id, twitter_user_id, tweet_date_string, tweet_text])
 
        except Queue.Empty:
            self.log("Empty queue exception ")
            time.sleep(0.1) 

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing
