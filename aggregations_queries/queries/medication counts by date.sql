select 'Tweets' source, count(*) from tweets_medications 
where medication_name in ( select  t2.medication_name from 
medications_tweets_fda t1, medications_tweets_fda t2 
where t1.medication_name = 'tamiflu' and t1.fda_drug_name = t2.fda_drug_name
group by t2.medication_name
) 
and to_char (tweet_date, 'YYYY-MM') = '2015-01' and adr_label = '1'
UNION
select 'FDA' source, count(*) 
from fda_report_drugs ld, medications_tweets_fda mtf 
where  mtf.medication_name= 'tamiflu' and  mtf.fda_drug_name  = ld.drug_name 
and  substring(report_date from 1 for 6) = '201501' ;