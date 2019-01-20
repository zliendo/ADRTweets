# w205-Project - Setup Environment

## Pre-requisites

The database has already been created and it is up and running

We provide two databases:


```
psql -h ********.rds.amazonaws.com -p 5432 -U *****
```

```
psql -h ********.rds.amazonaws.com -p 5432 -U ****** -d w205_sandbox
```
* w205_final has all the tweets ingested for January and February 2015, as well data downloaded from the FDA for 2015 Q1 
* w205_sandbox is an empty database where all this information can be recreated by executing a set of scripts 

pw=**********

## Setup Environment

Execute the following script
```
load_setup_env.sh 
```

The load_setup_env.sh script setups the environment for processing tweets, 
* it downloads Python packages, 
* creates the tweets_medication table if it doesn't exist and 
* installs the aws client to connect to S3

