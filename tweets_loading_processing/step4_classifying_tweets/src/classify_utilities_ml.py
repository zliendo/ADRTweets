# Author: Zenobia Liendo 
# code based on programs provided by DIEGO lab at Arizona University

from sklearn import metrics
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem.porter import *
import string,nltk,codecs
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

import sys
sys.path.append("../../step3_building_classifier/src")
from featureextractionmodules.FeatureExtractionUtilities import FeatureExtractionUtilities


def buildFeatures (data):
    stemmer = PorterStemmer()
    # Generate the test set features...
    data_set = defaultdict(list)
    unstemmed_texts = []
    for i in range (len(data)):
        #processRecord(dev_data[i], dev_labels[i], test_set, unstemmed_texts)
        _text = data[i]
        #_class = dev_labels[i]
        #data_set = test_set
        _text = _text.decode('utf8','ignore').encode('ascii','ignore')
        senttokens = nltk.word_tokenize(_text)
        stemmed_text = ''
        for t in senttokens:
            stemmed_text += ' ' + stemmer.stem(t)
        unstemmed_texts.append(_text)
               
        data_set['synsets'].append(FeatureExtractionUtilities.getSynsetString(_text, None))
        data_set['clusters'].append(FeatureExtractionUtilities.getclusterfeatures(_text))

        data_set['text'].append(stemmed_text)          
        #data_set['class'].append(_class)
    print 'Generating test set sentiment features .. '            
    data_set['sentiments'] = FeatureExtractionUtilities.getsentimentfeatures(unstemmed_texts)
    data_set['structuralfeatures'] = FeatureExtractionUtilities.getstructuralfeatures(unstemmed_texts)    
    data_set['adrlexicon'] = FeatureExtractionUtilities.getlexiconfeatures(unstemmed_texts) 
    data_set['topictexts'],data_set['topics'] = FeatureExtractionUtilities.gettopicscores(data_set['text'])
    data_set['goodbad'] = FeatureExtractionUtilities.goodbadFeatures(data_set['text'])
    
    return data_set

def vectorizeConcatenate(data_set, text_vectorizer,synsetvectorizer, clustervectorizer,topicvectorizer, scaler1):
    data_structural_features = scaler1.transform(data_set['structuralfeatures'])
    
    # Vectorize information
    data_text = text_vectorizer.transform(data_set['text']).toarray()
    data_synset_vectors = synsetvectorizer.transform(data_set['synsets']).toarray()
    data_cluster_vectors = clustervectorizer.transform(data_set['clusters']).toarray()
    data_topic_vectors = topicvectorizer.transform(data_set['topictexts']).toarray()
    
    
    # Concatenate resulting features    

    data_features = np.concatenate((data_text,data_synset_vectors),axis=1)
    data_features = np.concatenate((data_features,data_set['sentiments']),axis=1)
    data_features = np.concatenate((data_features,data_cluster_vectors),axis=1)
    data_features = np.concatenate((data_features,data_structural_features),axis=1)
    data_features = np.concatenate((data_features,data_set['adrlexicon']),axis=1)
    data_features = np.concatenate((data_features,data_set['topics']),axis=1)
    data_features = np.concatenate((data_features,data_topic_vectors),axis=1)
    data_features = np.concatenate((data_features,data_set['goodbad']),axis=1)
    
    return data_features

def predict(data,  adr_classifier,text_vectorizer,synsetvectorizer, clustervectorizer,topicvectorizer, scaler1):
    data_set = buildFeatures (data)
    data_features = vectorizeConcatenate(data_set, text_vectorizer,synsetvectorizer, clustervectorizer,topicvectorizer, scaler1)
    predicted_labels = adr_classifier.predict(data_features)
    return predicted_labels