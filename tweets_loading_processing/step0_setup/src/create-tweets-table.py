import psycopg2
import json
		
# read configuration options
# ------------------------------
with open('../../config.json') as config_file:    
    config_data = json.load(config_file)
    
dbdata = config_data["dbdata"].encode('utf8')

# create table
# --------------

conn = psycopg2.connect(dbdata)

cur = conn.cursor()

# create table if it does not exist 
cur.execute("""CREATE TABLE IF NOT EXISTS  tweets_medications
              (pk           bigserial PRIMARY KEY ,
		medication_name text NOT NULL,
		tweeter_id   text NOT NULL,
		tweet_id     text NOT NULL,
		tweet_date   date NOT NULL,
		tweet_text   text NOT NULL,
		adr_label    varchar(1),
		adr_classifier_version integer,
		last_classified_date date
		);""")

cur.execute("CREATE  INDEX medication_name_idx ON tweets_medications (medication_name);");
cur.execute("CREATE  INDEX tweet_date_idx ON tweets_medications (tweet_date);");
cur.execute("CREATE  INDEX adr_label_idx ON tweets_medications (adr_label);");
cur.execute("CREATE  UNIQUE INDEX tweet_idx ON tweets_medications (medication_name, tweet_id);");

        
conn.commit()
cur.close()
conn.close()
