# running program that builds classifiers
# -----------------------------------------
cd src 
python build_adr_classifier.py


# authentication credentials for S3 repository
#-------------------------------------------------
cd ../output_files 
export AWS_ACCESS_KEY_ID=********
export AWS_SECRET_ACCESS_KEY=********
export AWS_DEFAULT_REGION=us-east-1


# copy file to S3 directory
#-------------------------

aws s3 sync . s3://w205final/adr_ml_classifiers  --include '*.pkl'
