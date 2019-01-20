# Author: Zenobia Liendo 

import psycopg2
import numpy as np
import classify_utilities_ml

def get_tweets_not_classified(medication_name, conn):

    cur = conn.cursor()
    
    # get pkey and text of tweets not classified yet
    data_text= []
    data_pkey = []
    
    cur.execute("SELECT pk, tweet_text from tweets_medications where medication_name = %s and adr_label is NULL", 
                        (medication_name, ))

    records = cur.fetchall()
    for rec in records:
        data_text.append(rec[1])
        data_pkey.append(rec[0])
    conn.commit()

    print "number of records to classify: ", len(records) 
    return data_text, data_pkey
    
def update_tweets_db (data_pkey,predicted_labels, classifier_version, conn):
    # create list of tuples to insert in temporary tble
    data_pkey = [ int(x) for x in data_pkey ]
    values = zip(data_pkey, predicted_labels)

    cur = conn.cursor()
    # create temp table
    cur.execute("""CREATE TEMP TABLE tweets_adr_label_temp
              (pk           int PRIMARY KEY ,
               adr_label    varchar(1)) ON COMMIT DROP;""")


    # insert into temp table

    values_str = str(values).strip("[").strip("]")
    cur.execute("INSERT INTO tweets_adr_label_temp (pk, adr_label) VALUES " + values_str + ";") 

    # update 
    # TODO update the version fields
    cur.execute("""UPDATE tweets_medications  t 
           SET adr_label = tt.adr_label , adr_classifier_version = %s, last_classified_date = now() 
          FROM tweets_adr_label_temp  tt 
         WHERE t.pk = tt.pk """, (classifier_version, ))
    conn.commit()

def predict_adr_for_medication (medication_name, conn,classifier_version, adr_classifier,text_vectorizer,
                                                  synsetvectorizer, clustervectorizer,topicvectorizer, scaler1):
    
    print '\nMedication name: %s' % medication_name 
    # get pkey and text of tweets not classified yet
    data_text, data_pkey = get_tweets_not_classified(medication_name, conn)
    
    #predict using classifier
    predicted_labels = classify_utilities_ml.predict(data_text,adr_classifier,text_vectorizer,
                                                  synsetvectorizer, clustervectorizer,topicvectorizer, scaler1)
    
    dpkey = np.array(data_pkey)
    n_adr = len(dpkey[np.where(predicted_labels  == '1')])
    print 'number of adr tweets found for %s : %d' %(medication_name, n_adr)
    
    # update tweet db with the corresponding predicted label
    update_tweets_db (data_pkey,predicted_labels, classifier_version, conn)

def predict_adr (dbdata, classifier_version, adr_classifier,text_vectorizer,
                                                  synsetvectorizer, clustervectorizer,topicvectorizer, scaler1):
    
    # connect to database
    conn = psycopg2.connect(dbdata)
    cur = conn.cursor()
    
    #get list of medications
    medication_list = []
    cur.execute("SELECT medication_name from tweets_medications where adr_label is NULL group by medication_name")
    records = cur.fetchall()
    for rec in records:
        medication_list.append(rec[0])
    conn.commit()
    

    
    # predict for each of them
    for medication_name in medication_list:
        predict_adr_for_medication (medication_name, conn, classifier_version, adr_classifier,text_vectorizer,
                                                  synsetvectorizer, clustervectorizer,topicvectorizer, scaler1)   

    
    conn.close()
    print 'the end'

