# Building the adr Training Set

The DIEGO lab provided a list of 10K tweet-ids with labels indicating if  the tweet is an adr or not. 
 http://diego.asu.edu/
 http://diego.asu.edu/Publications/ADRMine.html
 
This module takes this list and gets the corresponding tweets from twitter.com

To get the training tweets, run the following script
```
build_training_set.sh
```



 The following few customization were made to the original python script:
 * store training data set in a CSV file for later use
 * counting number of tweets retrieved successfully
 * showing a log with progress of retrieving tweets (it takes about half an hour to run, makes 10K access to twitter)


From the 10K tweet-ids provided by DIEGO lab, only about 4K were found.
I contacted the researcher and he confirmed that many tweets probably had been deleted.. 


The python script performs the following actions:

 * opens the file with the list of tweet-ids and twitter-ids
 * for each row, takes the tweet-id and makes a search in twitter.com to look for the tweet
 * if the tweet is found, it is stored in a csv file
 
 The console will display the following messages.
 

 ```
  error: list index out of range
count :  1
count :  2
count :  3
count :  4
count :  5
 error: list index out of range
count :  6
 error: list index out of range
 error: list index out of range
count :  7
count :  8
count :  9
count :  10
count :  11
 error: list index out of range
count :  12
count :  13
 error: list index out of range
 error: list index out of range
 error: list index out of range
 error: list index out of range
 ```
  Whenever a tweet is not found, the 'error; list index out of range' is displayed
