import psycopg2
import json
		
# read configuration options
# ------------------------------
with open('../../tweets_loading_processing/config.json') as config_file:    
    config_data = json.load(config_file)
    
dbdata = config_data["dbdata"].encode('utf8')



conn = psycopg2.connect(dbdata)

cur = conn.cursor()

# create tweets_medications_search table if it does not exist
#------------------------------------------------------------

cur.execute("""CREATE TABLE  IF NOT EXISTS tweets_medications_search 
                (pk           bigserial PRIMARY KEY ,
		medication_name text NOT NULL);""")

cur.execute("DELETE from tweets_medications_search;")

cur.execute(""" INSERT INTO tweets_medications_search ( medication_name) 
select medication_name from tweets_medications group by medication_name;""")    

cur.execute("CREATE  INDEX  IF NOT EXISTS medication_name_search_idx ON tweets_medications_search(medication_name);")    
conn.commit()

# create tweets_medications_search table if it does not exist
#------------------------------------------------------------

cur.execute("""CREATE TABLE IF NOT EXISTS medications_tweets_fda 
(pk           bigserial PRIMARY KEY , 
 medication_name text NOT NULL,
 type text NOT NULL,
 fda_drug_name text NOT NULL);""");

cur.execute("DELETE FROM medications_tweets_fda;")

cur.execute("""INSERT INTO  medications_tweets_fda (type, medication_name, 
fda_drug_name)
select 'brand_name' ,  medication_name, drug_name fda_medication_product
from fda_brands lb, tweets_medications_search tm 
where lower(lb.brand_name) = tm.medication_name 
group by medication_name , drug_name
UNION 
select 'generic_name' , medication_name, drug_name fda_medication_product
from fda_generics lg, tweets_medications_search tm 
where lower(lg.generic_name) = tm.medication_name 
group by medication_name, drug_name ;""");

cur.execute("""CREATE  INDEX IF NOT EXISTS medication_tweet_fda_search_idx 
ON medications_tweets_fda(medication_name);""")
conn.commit()
cur.close()
conn.close()
