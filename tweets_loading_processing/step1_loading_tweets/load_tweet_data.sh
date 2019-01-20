
# run python program that ingest and load tweets
#-----------------------------------------------
cd src 
python get-tweets.py $1 $2 $3



# authentication credentials for S3 repository
#-------------------------------------------------
export AWS_ACCESS_KEY_ID=*************
export AWS_SECRET_ACCESS_KEY=*************
export AWS_DEFAULT_REGION=us-east-1

# move output_files to S3 repository
#---------------------------------------------
cd ../output_data/html 
aws s3 sync . s3://w205final/tweet_html_files  --include '*.html'

cd ../csv 
aws s3 sync . s3://w205final/tweet_csv_files  --include '*.csv'

cd ../logs

aws s3 sync . s3://w205final/loading_tweets_logs  --include '*.logs'
cd ..
cd .. 






