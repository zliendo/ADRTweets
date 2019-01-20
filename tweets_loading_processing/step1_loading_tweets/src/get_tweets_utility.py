
import urllib,urllib2,json,re,datetime,sys,cookielib
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import psycopg2
import calendar
from datetime import timedelta

# ------------------------------------------------------------------------
# getTweetDataForMedication
# ------------------------------------------------------------------------

def getTweetDataForMedication( output_directory_name,dbdata, medication, since, until):
    
    since_date = datetime.strptime(since, '%Y-%m-%d')
        
    # output file definitions
    file_name = medication + "-" + since + "--" + until 
    file_html = open(output_directory_name + "html/" + file_name+ ".html", 'wb')    
    file_csv =open(output_directory_name + "csv/" + file_name+ ".csv", 'wb')
    csv_writer = csv.writer(file_csv)
    file_log = open (output_directory_name + "logs/" + file_name+ ".log", 'wb')
        
    # database connection 
    conn = psycopg2.connect(dbdata)
    cur = conn.cursor()
    
    # url request
    url = "https://twitter.com/search?f=tweets&vertical=default&q=%s&src=typd"
    urlGetData =  medication + ' since:' + since +' until:' + until + ' lang:en'
    
    # look for tweets that meet search criteria
    refreshCursor = ''
    get_next_page = True
    while(get_next_page):  
        #get HTML page
        dataHTML = getTweetsPageHTML(url, urlGetData, refreshCursor)
        if (len (dataHTML) ==  0): break
        file_html.write(dataHTML)
        
        #get tweets from HTML page 
        tweets, tweet_oldest_date, oldestTweetId= processTweetPageHTML(dataHTML, since_date, medication)
        number_of_tweets = len(tweets)
        if (number_of_tweets == 0): break
        
        # persist tweets to csv and db             
        for tweet in tweets:
            # store tweets into csv files
            csv_writer.writerow(tweet)
            # store tweets into db
            #     row  = [medication, tweet_id, tweet_user_id ,tweet_date_string, tweet_text]
            try:
                cur.execute("INSERT INTO tweets_medications (medication_name,  tweet_id, tweeter_id, tweet_date, tweet_text) VALUES (%s, %s, %s, %s, %s)", 
                        (tweet[0],tweet[1], tweet[2], tweet[3], tweet[4]))

            except psycopg2.IntegrityError as inst: 
                print '******EXCEPTION***********'
                print(type(inst))
                print(inst.args)
                print(inst)
                print ' exception for medication: %s, refreshCursor: %s, tweet_date: %s,  tweet_id: %s' % (medication, refreshCursor, tweet[3], tweet[1])
                print 'tweet_ids: ', [row[1] for row in tweets]
		conn.rollback()
                #file_log.write ( 'Exception ' + type(inst) )
                file_log.write(' exception for medication: %s, refreshCursor: %s, tweet_date: %s,  tweet_id: %s' % (medication, refreshCursor, tweet[3], tweet[1]))
                #break
                raise  

        conn.commit()        
              
        # Print log
        print 'processing - refreshCursor (tweet-id):  %s , count by page: %d, oldest_date: %s' %( refreshCursor,number_of_tweets,tweet_oldest_date.strftime('%Y-%m-%d'))
        file_log.write ('\nprocessing - refreshCursor (tweet-id):  %s, , count by page: %d, oldest_date: %s' %( refreshCursor,number_of_tweets,tweet_oldest_date.strftime('%Y-%m-%d')) )
        
        #if the oldest date is already less thatn 'since' date, no more tweets in this date-range    
        if ( tweet_oldest_date < since_date) :
            get_next_page =  False
            print 'tweet date: ', tweet[3]  
        else:
            refreshCursor = str(int(oldestTweetId) - 1 )
            
    # closing resources
    file_html.close()
    file_csv.close()
    file_log.close()
    cur.close()
    conn.commit()
    conn.close()

    print 'the end'


# ------------------------------------------------------------------------
# getTweetsPageHTML
# ------------------------------------------------------------------------
def getTweetsPageHTML(url, urlGetData, refreshCursor):

    if len(refreshCursor) != 0:
        urlGetData = urlGetData + ' max_id:' +  refreshCursor        

    url = url % (urllib.quote(urlGetData))

    headers = [ 
    ('Host', "twitter.com"), 
    ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"), 
    ('Accept', "application/json, text/javascript, */*; q=0.01"), 
    ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"), 
    ('X-Requested-With', "XMLHttpRequest"), 
    ('Referer', url), 
    ('Connection', "keep-alive") 
    ] 
    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    opener.addheaders = headers
    try: 
        response = opener.open(url) 
        htmlResponse = response.read() 
    except: 
        print "Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.quote(urlGetData) 
        sys.exit()

    return htmlResponse


# ------------------------------------------------------------------------
# processTweetPageHTML
# ------------------------------------------------------------------------
    
def processTweetPageHTML(items_html, since_date,  medication ): 
    soup = BeautifulSoup(items_html, 'html.parser')
    
    # get the html for the list of tweets in this page
    tweets_html = soup.find_all("li", "js-stream-item")

    # process each tweet 
    tweets = []
    for tweet in tweets_html:
        fields, tweet_date, tweet_id = parseTweetHTML(tweet)   
        if (tweet_date < since_date):
            break
        tweets.append([medication] + fields)     

    if (len(tweets) > 0) : 
        tweet_oldest_date = tweet_date  
        oldestTweetId = tweet_id
    else:
        tweet_oldest_date = ''
        oldestTweetId = '' 
        
   
    return (tweets,tweet_oldest_date,oldestTweetId)




# ------------------------------------------------------------------------
# parseTweetHTML
# ------------------------------------------------------------------------
def parseTweetHTML (tweet):
    #tweet_id
    tweet_id = tweet['id'].split("-")[-1]
    
    #tweeter_user_id
    tweet_user_tag = tweet.find("a", "js-user-profile-link")
    tweet_user_id = tweet_user_tag ['data-user-id']
       
    # tweet date
    tweet_date = tweet.find("span", "js-short-timestamp")
    tweet_date_int = tweet_date['data-time-ms']
    tweet_date_object = datetime.fromtimestamp(int(tweet_date_int) / float(1000))
    tweet_date_string = tweet_date_object.strftime('%Y-%m-%d')
    
    # tweet text 
    tweet_text_t = tweet.find("p", "TweetTextSize js-tweet-text tweet-text")
    tweet_text =  tweet_text_t.get_text().encode('utf8')
    row  = [tweet_id, tweet_user_id ,tweet_date_string, tweet_text]
    return row, tweet_date_object, tweet_id


# ------------------------------------------------------------------------
# get_range_date
# ------------------------------------------------------------------------

def get_range_date ( argv):
  
    if (argv[0] == "range"):
        since_date = argv[1]
        until_date = argv[2]
    else:
        year = int (argv[1])
        month = int (argv[2])

        range = calendar.monthrange(year,month)
        since_date = datetime( year, month,1).strftime('%Y-%m-%d')
        until_date = datetime(year, month, range[1])
        until_date += timedelta(days=1)
        until_date = until_date.strftime('%Y-%m-%d')
    return since_date, until_date
