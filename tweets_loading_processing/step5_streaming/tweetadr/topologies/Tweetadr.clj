(ns Tweetadr 
  (:use     [streamparse.specs])
  (:gen-class))

(defn Tweetadr [options]
   [
    ;; spout configuration
    {"tweet-spout" (python-spout-spec
          options
          "spouts.tweets.Tweets"
          ["medication" "tweet_id", "twitter_user_id", "tweet_date_string", "tweet_text"]          
          )
    }
    ;; bolt configuration
    {"parse-tweet-bolt" (python-bolt-spec
          options
          {"tweet-spout" :shuffle}
          "bolts.parse.ParseTweet"
          ["tweet_id" "tweet_text"]
          )
    } 
  ]
)
