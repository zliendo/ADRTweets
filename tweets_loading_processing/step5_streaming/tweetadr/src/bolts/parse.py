from __future__ import absolute_import, print_function, unicode_literals

import re
from streamparse.bolt import Bolt
import psycopg2 

################################################################################
# Function to check if the string contains only ascii chars
################################################################################
def ascii_string(s):
  return all(ord(c) < 128 for c in s)

class ParseTweet(Bolt):
    def initialize(self, conf, ctx):	
   
        dbdata = "dbname=w205_final  user=w205_final password=w205_final host=w205-final.cz7z0nmeyqpf.us-east-1.rds.amazonaws.com port=5432"
        self.conn = psycopg2.connect(dbdata)
      


    def process(self, tup):
	cur = self.conn.cursor()
	medication_name = tup.values[0]
        tweet_id = tup.values[1]
        twitter_user_id = tup.values[2]
        tweet_date_string= tup.values[3]
        tweet_text = tup.values[4].encode('utf8')



        if ascii_string(tweet_text):
            # insert into table
            cur = self.conn.cursor()
            cur.execute("INSERT INTO tweets_medications (medication_name,  tweet_id, tweeter_id, tweet_date, tweet_text) VALUES (%s, %s, %s, %s, %s)", 
                        (medication_name,tweet_id, twitter_user_id, tweet_date_string, tweet_text))
            self.conn.commit()	


            # Log the count - just to see the topology running
            self.log('%s: %s' % (medication_name, tweet_text))

        # Emit all the words ( for future bolt to classify tweet
        self.emit([tweet_id, tweet_text])

        # tuple acknowledgement is handled automatically
