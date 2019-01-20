#
# This program classifies tweets, updating the corresponding adr_label indicator in the database
#  
# This are the steps in this process:
#
# (1) loads vectorizers and classifiers from pkl files into memory
# (2) finds the list of medications with tweets not classified yet
# (3) for each medication: gets a list of tweets-ids and tweets-text for the tweets not classified
# (4) executes the ML classifer for this set of tweets
# (5) updates the database table (adr_label) with the result of the classification,
#     to keep performance levels high, it uses
#     a batch INSERT and then a UPDATE JOIN to avoid multiple single updates 
#
# Author: Zenobia Liendo 



import pickle
import numpy as np
import psycopg2
import classify_utilities
import sys
import json 

sys.path.append("../../step3_building_classifier/src")
from featureextractionmodules.FeatureExtractionUtilities import FeatureExtractionUtilities

#read configuration file
#--------------------------------------------------------------------------------------
with open('../../config.json') as config_file:    
    config_data = json.load(config_file)
    
dbdata = config_data["dbdata"].encode('utf8')
classifier_version = config_data["classifier_version"].encode('utf8')

#get vectorizers and classifiers from pkl files 
#--------------------------------------------------------------------------------------

file = open('../../step3_building_classifier/output_files/vectorizer.pkl', 'rb')
text_vectorizer = pickle.load(file)
file.close()

file = open('../../step3_building_classifier/output_files/synsetvectorizer.pkl', 'rb')
synsetvectorizer = pickle.load(file)
file.close()

file = open('../../step3_building_classifier/output_files/clustervectorizer.pkl', 'rb')
clustervectorizer = pickle.load(file)
file.close()

file = open('../../step3_building_classifier/output_files/topicvectorizer.pkl', 'rb')
topicvectorizer =  pickle.load(file)
file.close()

#scaler1
file = open('../../step3_building_classifier/output_files/scaler1.pkl', 'rb')
scaler1 =  pickle.load(file)
file.close()

#get classifier 

file = open('../../step3_building_classifier/output_files/adr_classifier.pkl', 'rb')
adr_classifier = pickle.load(file)
file.close()

# perform classification
# ---------------------------------------------------------------------------------------------

classify_utilities.predict_adr ( dbdata, classifier_version,  adr_classifier,text_vectorizer,
                                                  synsetvectorizer, clustervectorizer,topicvectorizer, scaler1)

