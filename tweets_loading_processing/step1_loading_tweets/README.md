# w205-Project - loading tweets 


The load_tweet_data.sh  script loads the tweets for a boundary of dates using the input parameters provided.

For example, the tweets arleady loaded into the w205_final database are for January and February 2015,
they were ingested using the following commands: 

```
load_tweet_data.sh  year-month 2015 01
load_tweet_data.sh  range 2015-02-01 2015-02-03
load_tweet_data.sh  range 2015-02-03 2015-02-15
load_tweet_data.sh  range 2015-02-15 2015-03-01  
```

the **year-month** option looks for all the tweets in that month,
while the **range** option uses the 'since' and 'until' ranges from twitter (the second date is the upper limit, not included )


This script peforms the following actions:
* executes the get-tweets.py program that connects to twitter.com, insert tweets into the database and creates output files
* the output files are copied to the S3 repository 

which medications are searched for?
the ones included in the following file:
```
w205-project-adr\tweets_loading_processing\step1_loading_tweets\input_data\input_medication_list.txt
```

## get-tweets.py 

The python program peforms the following:

``` python
# This program gets tweets for a list of medications by accessing twitter.com (search option).
#
# The input parameters are date boundaries for searching tweets. Two ways to provide date boundaries:
# * by providing a range of dates (since, until); example:  python get-tweets.py range YYYY-MM-DD YYYY-MM-DD
# * by providing a year and month. example: python get-tweets.py year-month YYYY MM 
#   (the 'since' and 'until' dates are calculated based on the year-month provided)
# (note: the until-date is the upper limit, tweets LESS than this date are included.)
#
# For each medication, the program performs the following:
# (1) gets HTML pages with the tweets. It can be more than one page, the program simulates pagination in the web site
#     by using the oldest tweet-id in the last page retrieved. It stops when there are no more tweets in the data-range.
# (3) parses HTML pages and gets required information
# (2) creates three output files, all of them named: medicationName-sinceDate--untilDate
#     - the *.html files contain the HTML pages, 
#     - the *.csv  files contain the data parsed from these HTML pages,
#     - the *.log  files contain log information indicating the tweet-ids ranges for each of the many HTML pages
#       (this tweet-id can be potentially used for automatic re-starting options)

```
This is an example of what the console or log file will show when running this program for a list of 4 medications.
Each line represents an HTML page ingested. 
 
```
***************** medication_name: humira, since: 2015-02-01, until: 2015-02-07
processing - refreshCursor (tweet-id):   , count by page: 20, oldest_date: 2015-02-05
processing - refreshCursor (tweet-id):  563521565292515330 , count by page: 20, oldest_date: 2015-02-05
processing - refreshCursor (tweet-id):  563328707591303169 , count by page: 20, oldest_date: 2015-02-05
processing - refreshCursor (tweet-id):  563313614548107263 , count by page: 20, oldest_date: 2015-02-04
processing - refreshCursor (tweet-id):  563105667670478847 , count by page: 20, oldest_date: 2015-02-04
processing - refreshCursor (tweet-id):  563059666935349247 , count by page: 20, oldest_date: 2015-02-04
processing - refreshCursor (tweet-id):  562943167319015423 , count by page: 20, oldest_date: 2015-02-04
processing - refreshCursor (tweet-id):  562905383300501503 , count by page: 17, oldest_date: 2015-02-03
processing - refreshCursor (tweet-id):  562791206594547713 , count by page: 17, oldest_date: 2015-02-03
processing - refreshCursor (tweet-id):  562742900946399234 , count by page: 17, oldest_date: 2015-02-03
processing - refreshCursor (tweet-id):  562728912049168387 , count by page: 20, oldest_date: 2015-02-02
processing - refreshCursor (tweet-id):  562456931382468607 , count by page: 20, oldest_date: 2015-02-01
processing - refreshCursor (tweet-id):  562087507073183744 , count by page: 17, oldest_date: 2015-01-31
tweet date:  2015-02-01
the end
***************** medication_name: dronedarone, since: 2015-02-01, until: 2015-02-07
the end
***************** medication_name: lamictal, since: 2015-02-01, until: 2015-02-07
processing - refreshCursor (tweet-id):   , count by page: 13, oldest_date: 2015-02-05
processing - refreshCursor (tweet-id):  563527331386384384 , count by page: 12, oldest_date: 2015-02-05
processing - refreshCursor (tweet-id):  563387046106906624 , count by page: 12, oldest_date: 2015-02-04
processing - refreshCursor (tweet-id):  563152570529890304 , count by page: 15, oldest_date: 2015-02-03
processing - refreshCursor (tweet-id):  562764410725629951 , count by page: 20, oldest_date: 2015-02-02
processing - refreshCursor (tweet-id):  562472633808068607 , count by page: 13, oldest_date: 2015-02-02
processing - refreshCursor (tweet-id):  562262687434829823 , count by page: 17, oldest_date: 2015-01-31
tweet date:  2015-02-01
the end
***************** medication_name: pradaxa, since: 2015-02-01, until: 2015-02-07
processing - refreshCursor (tweet-id):   , count by page: 5, oldest_date: 2015-02-03
the end

```

* refreshCursor (tweet-id) : is the max-tweet-id to search for, which is the oldest tweet-id from the previous page
* count by page: number of tweets in that page
* oldest_date: the oldest tweet-date retrieved in that page (used by the program to check if it reached the lower date boundary)

## Re-starting options

If for some reason the program stops, the process can be re-started by:

* looking at the console or log file to see what was the last medication and date loaded
* update the input_medication_list by removing the medications that had already been loaded
* execute the load_tweet_data.sh again but with a different range of dates, to point to what is pending to be loaded 

example: 
```
load_tweet_data.sh range 2015-01-05 2015-01-15 
```
The re-starting option can be developed much more to make it automatic.
The program could be aware of what was the last medication, date and tweet-id downloaded and re-start from there.
