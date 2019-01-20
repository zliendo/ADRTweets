## Streaming Tweets

The streaming module captures tweets that are being posted live and inserts them into the database.

### Database and Twitter credentials

The parse.py module is pointing to the following database:
```
dbdata = "dbname=w205_final  user=w205_final password=w205_final host=w205-final.cz7z0nmeyqpf.us-east-1.rds.amazonaws.com port=5432"
```
and the tweets.py has already tweets credentials in it. 

### Starting the Streaming Process

The script that executes the streaming process can receive one parameter indicating a medicaiton_name,
for example:
```
streaming.sh prozac
```

if no medication_name is provided, 'tamiflu' is the default.


**Future improvement**: 
* providing a list of medications instead of just one (or reading list of medications from db)
and matching arriving tweets to one or more medication-name search keys 
* adding a bolt to classify tweets on the fly