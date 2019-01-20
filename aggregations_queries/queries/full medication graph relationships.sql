select t1.medication_name,  t2.medication_name, t2.type , array_agg(t1.fda_drug_name) fda_drug_name_link
from tweets_medications_search ml, medications_tweets_fda t1, medications_tweets_fda t2 
where ml.medication_name = t1.medication_name and  t1.fda_drug_name = t2.fda_drug_name 
group by t1.medication_name, t2.medication_name, t2.type
order by t1.medication_name;