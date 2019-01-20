# download python libraries
# -----------------------------------
pip install BeautifulSoup
pip install psycopg2
pip install bs4 
pip install nltk 
pip install numpy
pip install sklearn 
pip install scipy 
pip install gensim 
pip install pandas
pip install tweepy



# setting up the aws client to access S3 repository
# ---------------------------------------------------
pip install awscli 


cd src 

# create table
# (note: this script will delete the table if already exists)
#----------------------------------------------------------
python create-tweets-table.py

# download sme ntlk packages
#-------------------------------------------------
python nltk_downloads.py











