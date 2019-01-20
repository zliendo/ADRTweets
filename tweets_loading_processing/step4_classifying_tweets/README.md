## Classifying Tweets using a Machine Learning Model 


to classify tweets from the database,
execute the following sh script
```
classify_tweets.sh
``` 
this script executes a python program that classifies tweets, updating the corresponding adr_label indicator in the database
  
 These are the steps in this program:

 1. loads vectorizers and classifiers from pkl files into memory
 2. finds the list of medications with tweets not classified yet
 3. for each medication: gets a list from the database of not classified tweets (tweet-id and tweet-text) 
 4. executes the ML classifer (SVM) for this set of tweets
 5. updates the database table (adr_label) with the result of the classification. In order to keep performance levels high, it uses
    a batch INSERT and then a UPDATE JOIN to avoid multiple single updates 


The program will produce a console log that looks like:
```
Medication name: humira
number of records to classify:  845
Generating test set sentiment features ..
count:  100
count:  200
count:  300
count:  400
count:  500
count:  600
count:  700
count:  800
number of adr tweets found for humira : 6

Medication name: venlafaxine
number of records to classify:  195
Generating test set sentiment features ..
count:  100
number of adr tweets found for venlafaxine : 5

Medication name: linagliptin
number of records to classify:  88
Generating test set sentiment features ..
number of adr tweets found for linagliptin : 0

Medication name: lamotrigine
number of records to classify:  151
Generating test set sentiment features ..
count:  100
number of adr tweets found for lamotrigine : 3
```


