## Building the ML Classifier 

execute the following *.sh script
```
build_adr_classifier.sh
```

the process of building a classifier takes time (2 to 4 hours),
it is recommended to use a large ec2 instance

This script runs a python program that customized an open source program provided by Dr. Asarker
https://bitbucket.org/asarker/adrbinaryclassifier
from HLP @ UPenn IBI
https://healthlanguageprocessing.org/
formerly DIEGO lab at ASU
http://diego.asu.edu/

The following customizations were done:
* read training data from csv file
* split records into training and development sets
* calculat RUC-AUC scores 
* download nltk packages during setup 
* write classifiers and vectorizers trained into PKL files for later use 
* fixing a minor bug (sent fix to Dr. Asarker)
* tuning c and w hyperparameters
* some re-factoring (not much)
* adding code to print some messages into console for tracking progress

the console will display the following log messages
```
[root@ip-172-31-7-6 step3_building_classifier]# sh build_adr_classifier.sh
/usr/lib64/python2.7/site-packages/gensim/utils.py:1015: UserWarning: Pattern library is not installed, lemmatization won't be available.
  warnings.warn("Pattern library is not installed, lemmatization won't be available.")
number of examples: 4830
training data examples: 3864
dev data examples: 966
/data/final_project/w205-project-adr/tweets_loading_processing/step3_building_classifier/src/featureextractionmodules/FeatureExtractionUtilities.py:263: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
  if t in FeatureExtractionUtilities.word_clusters[k]:
Generating training set sentiment features ..
count:  100
count:  200
count:  300
count:  400
count:  500
count:  600
count:  700
count:  800
count:  900
count:  1000
count:  1100
count:  1200
count:  1300
count:  1400
count:  1500
count:  1600
count:  1700
count:  1800
count:  1900
count:  2000
count:  2100
count:  2200
count:  2300
count:  2400
count:  2500
count:  2600
count:  2700
count:  2800
count:  2900
count:  3000
count:  3100
count:  3200
count:  3300
count:  3400
count:  3500
count:  3600
count:  3700
count:  3800
training features generated
vectorizers generated
features concatenated
vectorizers saved into pkl files
Generating test set sentiment features ..
count:  100
count:  200
count:  300
count:  400
count:  500
count:  600
count:  700
count:  800
count:  900
dev features generated
dev vectorizers generated and features concatenated
starting building classifier
Precision for the ADR class .. 0.559139784946
Recall for the ADR class .. 0.525252525253
ADR F-score .. 0.541666666667
roc_auc 0.874791746764
classifier saved and pkl file
*** END ***
upload: ./adr_classifier.pkl to s3://w205final/adr_ml_classifiers2/adr_classifier.pkl
upload: ./synsetvectorizer.pkl to s3://w205final/adr_ml_classifiers2/synsetvectorizer.pkl
upload: ./scaler1.pkl to s3://w205final/adr_ml_classifiers2/scaler1.pkl
upload: ./clustervectorizer.pkl to s3://w205final/adr_ml_classifiers2/clustervectorizer.pkl
upload: ./vectorizer.pkl to s3://w205final/adr_ml_classifiers2/vectorizer.pkl
upload: ./topicvectorizer.pkl to s3://w205final/adr_ml_classifiers2/topicvectorizer.pkl
upload: ./test_set.pkl to s3://w205final/adr_ml_classifiers2/test_set.pkl
upload: ./training_set.pkl to s3://w205final/adr_ml_classifiers2/training_set.pkl
```



