# Original script was provided by DIEGO lab at Arizona State University
#
# http://diego.asu.edu/
# http://diego.asu.edu/Publications/ADRMine.html
#
# The original script had the following few modifications:
# * store training data set in a CSV file for later use
# * counting number of tweets retrieved successfully
# * showing a log with progress of retrieving tweets (it takes about half an hour to run, makes 10K access to twitter)
#
# This program performs the following actions: 
# * opens the file with the list of tweet-ids and twitter-ids
# * for each row, takes these ids and makes a search in twitter.com to look for the tweet
# * if the tweet is found, it is stored in a csv file
#
# customizations by: Zenobia Liendo

import sys, urllib, re, json, socket, string
import csv
from bs4 import BeautifulSoup

# define input andn out files
# ----------------------------------------------
inputFileName= "../input_file/Twitter_corpus_releaseset_external.txt"
outputFileName = "../output_file/Training_set.csv"
output_file =open(outputFileName, 'wb')
csv_writer = csv.writer(output_file)

# get tweets for each tweet-id
#-------------------------------------------
socket.setdefaulttimeout(20)
item_dict = {}
try:
    #for line in open(sys.argv[1]):
    count = 0 
    for line in open(inputFileName):
        fields = line.rstrip().split('\t')
        tweetid = fields[0]
        userid = fields[1]
        tweet = None
        text = "Not Available"
        if item_dict.has_key(tweetid):
            text = item_dict[tweetid]
        else:
            try:
                f = urllib.urlopen('http://twitter.com/'+str(userid)+'/status/'+str(tweetid))
                html = f.read().replace("</html>", "") + "</html>"
                soup = BeautifulSoup(html, 'html.parser')
                jstt   = soup.find_all("p", "js-tweet-text")
                tweets = list(set([x.get_text() for x in jstt]))
                if(len(tweets)) > 1:
                    other_tweets = []
                    cont   = soup.find_all("div", "content")
                    for i in cont:
                        o_t = i.find_all("p","js-tweet-text")
                        other_text = list(set([x.get_text() for x in o_t]))
                        other_tweets += other_text					
                    tweets = list(set(tweets)-set(other_tweets))
                text = tweets[0]
                item_dict[tweetid] = tweets[0]
                for j in soup.find_all("input", "json-data", id="init-data"):
                    js = json.loads(j['value'])
                    if(js.has_key("embedData")):
                        tweet = js["embedData"]["status"]
                        text  = js["embedData"]["status"]["text"]
                        item_dict[tweetid] = text
                        break
            except Exception as err:
                print (" error: {0}".format(err))
                continue
    
        if(tweet != None and tweet["id_str"] != tweetid):
                text = "This tweet has been removed or is not available"
                item_dict[tweetid] = "This tweet has been removed or is not available"
        text = text.replace('\n', ' ',)
        text = re.sub(r'\s+', ' ', text)
        count += 1
        print 'count : ', count 
        to_write = "\t".join(fields + [text]) + "\n"
        csv_writer.writerow(fields + [text.encode('utf-8')])
 
    output_file.close()
except IndexError:
    print 'Incorrect arguments specified (may be you didn\'t specify any arguments..'
    print 'Format: python [scriptname] [inputfilename] > [outputfilename]'

