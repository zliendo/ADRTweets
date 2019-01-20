import get_tweets_utility
import sys
import json

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

# author: Zenobia Liendo
# ==================================================================================================

#read configuration file
#--------------------------------------
with open('../../config.json') as config_file:    
    config_data = json.load(config_file)
    
output_directory_name = config_data["tweets_output_directory_name"].encode('utf8')
input_medications_file = config_data["medication_list_file"].encode('utf8')
dbdata = config_data["dbdata"].encode('utf8')

# get input parameters
#------------------------------
argv = sys.argv[1:]


#execute program
#-----------------------------------------------

# get the data range based on the input paramters
# (there are two ways to specify the date range in the input parameters)
since_date, until_date = get_tweets_utility.get_range_date ( argv)


# loop for each medication in the list of medications 
input_file = open(input_medications_file, 'rb')
for line in input_file:
    medication_name = line.strip()
    if (len(medication_name) == 0):continue;

    # gets the tweet information for a medication_name
    print '***************** medication_name: %s, since: %s, until: %s' % ( medication_name,since_date, until_date)
    get_tweets_utility.getTweetDataForMedication ( output_directory_name, dbdata, medication_name, since_date, until_date)

input_file.close()

