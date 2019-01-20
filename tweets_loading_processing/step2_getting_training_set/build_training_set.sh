# run program
#------------
cd src
python get_training_tweets.py

# authentication credentials for S3 repository
#-------------------------------------------------
export AWS_ACCESS_KEY_ID=***********
export AWS_SECRET_ACCESS_KEY=***********
export AWS_DEFAULT_REGION=us-east-1


# copy file to S3 directory
#-------------------------
cd ../output_file 
aws s3 sync . s3://w205final/training_set  --include '*.csv'