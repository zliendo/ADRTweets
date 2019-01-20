select 'FDA' source, ml.medication_name, mtf.fda_drug_name,  count(*) 
from fda_report_drugs ld, medications_tweets_fda mtf , tweets_medications_search ml
where  mtf.medication_name= ml.medication_name and  mtf.fda_drug_name  = ld.drug_name 
and  substring(report_date from 1 for 6) = '201501' 
group by  ml.medication_name, mtf.fda_drug_name 
order by  ml.medication_name, mtf.fda_drug_name;