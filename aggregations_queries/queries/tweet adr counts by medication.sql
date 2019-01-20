select ms.t1_medication_name, ms.t2_medication_name, count(*) qty 
from (
select t1.medication_name t1_medication_name,  t2.medication_name t2_medication_name
from tweets_medications_search ml, medications_tweets_fda t1, medications_tweets_fda t2 
where ml.medication_name = t1.medication_name and  t1.fda_drug_name = t2.fda_drug_name 
group by t1.medication_name, t2.medication_name
order by t1.medication_name) 
ms , tweets_medications tm
where ms.t2_medication_name = tm.medication_name and 
tm.adr_label = '1'  and  to_char (tweet_date, 'YYYY-MM') = '2015-01'  
group by ms.t1_medication_name, ms.t2_medication_name
order by ms.t1_medication_name;