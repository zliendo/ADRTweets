# Tweets ingestion and adr classification

each folder in this section has a unix script for execution

## Config.json file 

The config.json file has information about the location of the database and where input and output files will be located.
This file is used by different modules like tweet-module-setup, tweets-ingestion, tweets-classification, etc.


config.json could be modified if necessary 
```
"dbdata": "dbname=w205_final  user=w205_final password=******* host=*****.us-east-1.rds.amazonaws.com port=5432",
"medication_list_file" : "../input_data/input_medication_list.txt" ,
"output_directory_name" : "../data/"
```

**dbdata:** The w205_final database is the one that already has tweeter and fda data loaded and classified.
(note: the setup script will only create a new table if it does not exist, making sure the table is not deleted when other setup tasks are executed) 

for testing replication, we provide a sandbox database that starts empty
```
"dbdata": "dbname=w205_sandbox  user=w205_final password=******* host=****.us-east-1.rds.amazonaws.com port=5432",
```
please change the configuration file if you would like to start from an empty database.

**medication_list_file:** it is the file that contains the list of medications-names that will be searched in twitter.com 
(tip: for testing purposes, the list can be shorten)

**output_directory_name:** the tweets ingestes are not only inserted in the database but the HTML information is stored in files, along with csv and log files

## Setup

It downloads Python packages, creates the tweets_medication table if it doesn't exist and installs the aws client to connect to S3 

## Process
1. pulls tweets from twitter.com (HTML web scrapping, paginating search results)
2. builds the training set
3. builds the classifier
4. classifies tweets in the database
5. streams tweets using Apache Storm 

there is a *.sh script for each step described above 


