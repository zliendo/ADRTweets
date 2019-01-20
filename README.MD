
This repository contains code I implemented to detect Tweets that are reporting adverse drug reports (ADRs), collecting tweets in real time and historical ones to compare statistics with ADRs reported to the FDA. 
   
The code was implemented on December 2016, during my graduate studies at the Master of Information and Data Science (MIDS) program at UC Berkeley.   The class was: w205 - Architectural Components for Storing and Retrieving Data  

This is the project report: 

I implemented the following modules:

| Module | Description |   
|---|---|
| Batch Ingestion | Collects historical tweets for a list of medications in a date range and store them in a database. Python programs access the search page at Twitter.com and pulls historic data by programatically executing searches and scraping web content (HTML pages returned). Twitter provides an API to collect tweets, but only few days old, we needed tweets from past years|   
| Real Time Ingestion| Streaming was implemented using Apache Storm and Streamparse. Tweets captured are stored in the database.|   
| Model and Classification | Not all tweets collected are reporting ADRs, they can be just mentioning a medication. Building ML classification model using open source code and training data provided by DIEGO lab at Arizona University.  Classifying ADRs tweets from the database using the ML model |   
| Compare with FDA | SQL statements to compare statistics about ADRs found in Tweets and FDA ADRs reports in the same range of data|   
