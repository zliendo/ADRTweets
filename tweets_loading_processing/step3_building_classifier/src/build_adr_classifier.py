# This code is based on the classifier provided by Dr. Asarker
# https://bitbucket.org/asarker/adrbinaryclassifier
# from HLP @ UPenn IBI
# https://healthlanguageprocessing.org/
# formerly DIEGO lab at ASU
# http://diego.asu.edu/

# The following customizations were done:
# * read training data from csv file
# * split records into training and development sets
# * calculat RUC-AUC scores 
# * download nltk packages during setup 
# * write classifiers and vectorizers trained into PKL files for later use 
# * fixing a minor bug (sent fix to Dr. Asarker)
# * tuning c and w hyperparameters
# * some re-factoring
# * adding code to print some messages into console for tracking progress
#
# customizer: Zenobia Liendo

import csv
from random import shuffle
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pickle

import string,nltk,codecs
from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
import numpy as np
from nltk.corpus import stopwords
from sklearn import svm
from collections import defaultdict


# loading resources
#-------------------------------------------------------------

from featureextractionmodules.FeatureExtractionUtilities import FeatureExtractionUtilities
stemmer = PorterStemmer()
def loadFeatureExtractionModuleItems():
    FeatureExtractionUtilities.loadItems()

global good_words
global bad_words
global more_words
global less_words
global senti_words
global modals
global topic_dict
loadFeatureExtractionModuleItems()

# reading tweet corpus file and split in training and dev sets
#-------------------------------------------------------------

with open('../../step2_getting_training_set/output_file/Training_set.csv', 'rb') as f:
    reader = csv.reader(f)
    tweet_list = list(reader)
shuffle(tweet_list)

tweets = np.array(tweet_list)
number_of_tweets = len(tweets)

# splitting data: 80% for training, 20% for dev
training_size = int (0.8 * number_of_tweets)
dev_size  = number_of_tweets - training_size

print "number of examples:", number_of_tweets
print "training data examples:", training_size
print "dev data examples:",dev_size

training_info = tweets[0:training_size]
dev_info = tweets[training_size:]


training_data, training_labels = training_info[:,3] , training_info[:,2]
dev_data, dev_labels = dev_info[:,3] , dev_info[:,2]

# a function to do some of the processing
#-------------------------------------------------------------

def processRecord (_text, _class, data_set, unstemmed_texts) :
    #_text = string.lower(string.strip(items[1]))            
    #_class = string.strip(items[-1])
    _text = string.lower(string.strip(_text))
    _class = string.strip(_class)
    _text = _text.decode('utf8','ignore').encode('ascii','ignore')
    senttokens = nltk.word_tokenize(_text)
    stemmed_text = ''
    for t in senttokens:
        stemmed_text += ' ' + stemmer.stem(t)
    unstemmed_texts.append(_text)
               
    data_set['synsets'].append(FeatureExtractionUtilities.getSynsetString(_text, None))
    data_set['clusters'].append(FeatureExtractionUtilities.getclusterfeatures(_text))

    data_set['text'].append(stemmed_text)          
    data_set['class'].append(_class)

# Generate the training set features...
#------------------------------------------------------------------------

training_set = defaultdict(list)
unstemmed_texts = []
for i in range (len(training_data)):
    processRecord(training_data[i], training_labels[i], training_set, unstemmed_texts)
print 'Generating training set sentiment features .. '
training_set['sentiments'] = FeatureExtractionUtilities.getsentimentfeatures(unstemmed_texts)
training_set['structuralfeatures'] = FeatureExtractionUtilities.getstructuralfeatures(unstemmed_texts)  
scaler1 = preprocessing.StandardScaler().fit( training_set['structuralfeatures'])  
train_structural_features = scaler1.transform( training_set['structuralfeatures'])
training_set['adrlexicon'] = FeatureExtractionUtilities.getlexiconfeatures(unstemmed_texts)
training_set['topictexts'],training_set['topics'] = FeatureExtractionUtilities.gettopicscores(training_set['text'])
training_set['goodbad'] = FeatureExtractionUtilities.goodbadFeatures(training_set['text'])

print 'training features generated'

# Initialize the vectorizers
vectorizer = CountVectorizer(ngram_range=(1,3), analyzer = "word", tokenizer = None, preprocessor = None, max_features = 5000)
synsetvectorizer = CountVectorizer(ngram_range=(1,1),analyzer="word",tokenizer=None,preprocessor=None,max_features = 2000)
clustervectorizer = CountVectorizer(ngram_range=(1,1),analyzer="word",tokenizer=None,preprocessor=None,max_features = 1000)
topicvectorizer = CountVectorizer(ngram_range=(1,1),analyzer="word",tokenizer=None,preprocessor=None,max_features=500)

print 'vectorizers generated'

#    Generate the data vectors
trained_data = vectorizer.fit_transform(training_set['text']).toarray()
train_data_synset_vector = synsetvectorizer.fit_transform(training_set['synsets']).toarray()
train_data_cluster_vector = clustervectorizer.fit_transform(training_set['clusters']).toarray()
train_data_topic_vector = topicvectorizer.fit_transform(training_set['topictexts']).toarray()
    
#    Concatenate the various feature arrays
trained_data = np.concatenate((trained_data,train_data_synset_vector),axis=1)
trained_data = np.concatenate((trained_data,training_set['sentiments']),axis=1)
trained_data = np.concatenate((trained_data,train_data_cluster_vector),axis=1)
trained_data = np.concatenate((trained_data,train_structural_features),axis=1)
trained_data = np.concatenate((trained_data,training_set['adrlexicon']),axis=1)
trained_data = np.concatenate((trained_data,training_set['topics']),axis=1)
trained_data = np.concatenate((trained_data,train_data_topic_vector),axis=1)
trained_data = np.concatenate((trained_data,training_set['goodbad']),axis=1)

print 'features concatenated'

# save vectorizers into files
#-----------------------------------------------------------
output = open('../output_files/scaler1.pkl', 'wb')
pickle.dump(scaler1, output)
output.close()

output = open('../output_files/vectorizer.pkl', 'wb')
pickle.dump(vectorizer, output)
output.close()

output = open('../output_files/synsetvectorizer.pkl', 'wb')
pickle.dump(synsetvectorizer, output)
output.close()

output = open('../output_files/clustervectorizer.pkl', 'wb')
pickle.dump(clustervectorizer, output)
output.close()

output = open('../output_files/topicvectorizer.pkl', 'wb')
pickle.dump(topicvectorizer, output)
output.close()

print 'vectorizers saved into pkl files' 

# generate features for DEV data
#-----------------------------------------------------------

# Generate the test set features...
test_set = defaultdict(list)
unstemmed_texts = []
for i in range (len(dev_data)):
    processRecord(dev_data[i], dev_labels[i], test_set, unstemmed_texts)
print 'Generating test set sentiment features .. '            
test_set['sentiments'] = FeatureExtractionUtilities.getsentimentfeatures(unstemmed_texts)
test_set['structuralfeatures'] = FeatureExtractionUtilities.getstructuralfeatures(unstemmed_texts)
test_structural_features = scaler1.transform(test_set['structuralfeatures'])
test_set['adrlexicon'] = FeatureExtractionUtilities.getlexiconfeatures(unstemmed_texts) 
test_set['topictexts'],test_set['topics'] = FeatureExtractionUtilities.gettopicscores(test_set['text'])
test_set['goodbad'] = FeatureExtractionUtilities.goodbadFeatures(test_set['text'])

print 'dev features generated'

#        Fit the test data 
test_data = vectorizer.transform(test_set['text']).toarray()
test_data_synset_vectors = synsetvectorizer.transform(test_set['synsets']).toarray()
test_data_cluster_vectors = clustervectorizer.transform(test_set['clusters']).toarray()
test_data_topic_vectors = topicvectorizer.transform(test_set['topictexts']).toarray()
          

#        Concatenate the test feature arrays
test_data = np.concatenate((test_data,test_data_synset_vectors),axis=1)
test_data = np.concatenate((test_data,test_set['sentiments']),axis=1)
test_data = np.concatenate((test_data,test_data_cluster_vectors),axis=1)
test_data = np.concatenate((test_data,test_structural_features),axis=1)
test_data = np.concatenate((test_data,test_set['adrlexicon']),axis=1)
test_data = np.concatenate((test_data,test_set['topics']),axis=1)
test_data = np.concatenate((test_data,test_data_topic_vectors),axis=1)
test_data = np.concatenate((test_data,test_set['goodbad']),axis=1)

print 'dev vectorizers generated and features concatenated'

# functions for building the classifier
#-----------------------------------------------------------------------------------
def calculateScores(predicted_labels,test_gold_classes):
    try:
        tp=0.0
        tn=0.0
        fn=0.0
        fp=0.0
        #print result
        #print test_gold_classes
        for pred,gold in zip(predicted_labels,test_gold_classes):
            if pred == '1' and gold == '1':
                tp+=1
            if pred == '1' and gold == '0':
                fp+=1
            if pred == '0' and gold == '0':
                tn +=1
            if pred == '0' and gold == '1':
                fn+=1
        adr_prec = tp/(tp+fp)
        adr_rec = tp/(tp+fn)
        fscore = (2*adr_prec*adr_rec)/(adr_prec + adr_rec)
        print 'Precision for the ADR class .. ' + str(adr_prec)
        print 'Recall for the ADR class .. ' + str(adr_rec)
        print 'ADR F-score .. ' + str(fscore)
    except ZeroDivisionError:
        print 'There was a zerodivisionerror'
        print 'Precision for the ADR class .. ' + str(0)
        print 'Recall for the ADR class .. ' + str(0)
        print 'ADR F-score .. ' + str(0)

def classify(c, w):

    # training the svms
    svm_classifier = svm.SVC(C=c, cache_size=200, class_weight={'1':w,'0':1}, coef0=0.0, degree=3, 
                             gamma='auto', kernel='rbf', max_iter=-1, probability=True, random_state=None,
                             shrinking=True, tol=0.001, verbose=False)
    
    svm_classifier = svm_classifier.fit(trained_data, training_set['class'])
    
    # making the predictions    
    result = svm_classifier.predict(test_data)

    
    #print accuracy_score(test_data['class'],result)
    #compute the ADR F-score
    test_gold_classes = test_set['class']
    calculateScores(result,test_gold_classes)
    
    #calculate ROC AUC
    predicted_prob = svm_classifier.predict_proba(test_data) 
    #print (model.classes_)
    fpr, tpr, thresholds = metrics.roc_curve(test_gold_classes, predicted_prob[:,1], pos_label = '1')
    roc_auc = metrics.auc(fpr, tpr)
    print 'roc_auc', roc_auc
    return svm_classifier

#save training and test sets for re-starting options
#-----------------------------------------------------
output = open('../output_files/training_set.pkl', 'wb')
pickle.dump(training_set, output)
output.close()
output = open('../output_files/test_set.pkl', 'wb')
pickle.dump(test_set, output)
output.close()


# looking for the best c and w values
#-----------------------------------------------------------------------------------
f_scores = {}
#for c in [100,110,115,120,125,130,135,140,145,150,155,160]:
#    for w in [1,2,3,4]:
#        print 'c: %s, w: %s' %(c,w)
#        svm_classifier = classify(c,w)

# results can be seen at ../result-from-tuning-classifier.txt

# best performance scores for
# c= 100, w=3

print 'starting building classifier'

# building classifier
#-----------------------------
c = 100
w = 3
svm_classifier = classify(c,w)

# storing classifier
#------------------------
output = open('../output_files/adr_classifier.pkl', 'wb')
pickle.dump(svm_classifier, output)
output.close()

print 'classifier saved and pkl file'

print '*** END ***'


