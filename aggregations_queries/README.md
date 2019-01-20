the following script executes the aggregation updates
```
aggregration.sh
```

for now, we have the following aggregations:
* creates and populates the tweets_medications_search table (lookup table), grouping information from the tweets_medications table
* creates and populates the medications_tweets_fda (lookup table), joining information from tweets_medication_search, fda_brands and fda_generics table 

This directory also has *.sql files with query samples for getting information about number of ADRs in the fda and tweets tables
For example:

'adr events reported in January 2015 for tamiflu'
```
source  | count
--------+-------
 fda    |  116
 Tweets |  111
(2 rows)
```

what are the number of adr reports in twitter and fda for January 2015?
(considering the family of drug-names: brand and generic names)

```

medicationname  | source  |                             medication_group                      | qty
----------------+---------+--------------------------------------------------------------------------+-----
actonel         | FDA     | {ACTONEL,"RISEDRONATE SODIUM."}                                   |  17
albuterol       | FDA     | {ALBUTEROL.,"ALBUTEROL SULFATE."}                                 | 260
albuterol       | Twitter | {albuterol}                                                       |  11
alendronate     | FDA     | {ALENDRONATE}                                                     |  39
apixaban        | FDA     | {APIXABAN,ELIQUIS}                                                | 343
apixaban        | Twitter | {apixaban,eliquis}                                                |   3
avelox          | FDA     | {AVELOX,"MOXIFLOXACIN HYDROCHLORIDE."}                            |  33
avelox          | Twitter | {avelox}                                                          |   1
baclofen        | FDA     | {BACLOFEN.,GABLOFEN,LIORESAL}                                     | 345
baclofen        | Twitter | {baclofen}                                                        |   2
boniva          | FDA     | {BONIVA,"IBANDRONATE SODIUM."}                                    |  17
bystolic        | FDA     | {BYSTOLIC,"NEBIVOLOL HYDROCHLORIDE"}                              |  55
canagliflozin   | Twitter | {canagliflozin}                                                   |   1
cipro           | FDA     | {CIPRO,"CIPROFLOXACIN HYDROCHLORIDE."}                            |  52
cipro           | Twitter | {cipro}                                                           |  15
denosumab       | FDA     | {DENOSUMAB,PROLIA,XGEVA}                                          | 571
dronedarone     | FDA     | {DRONEDARONE,MULTAQ}                                              |  27
duloxetine      | FDA     | {DULOXETINE,"DULOXETINE HYDROCHLORIDE.","DULOXETINEHYDROCHLORIDE 60 MG"} | 143
effient         | FDA     | {EFFIENT,"PRASUGREL HYDROCHLORIDE"}                               |  45
effient         | Twitter | {effient}                                                         |   1
eliquis         | FDA     | {APIXABAN,ELIQUIS}                                                | 343
eliquis         | Twitter | {apixaban,eliquis}                                                |   3
fluoxetine      | FDA     | {FLUOXETINE,"FLUOXETINE HYDROCHLORIDE."}                          | 324
fluoxetine      | Twitter | {fluoxetine}                                                      |   8
fosamax         | FDA     | {FOSAMAX}                                                         |  44
fycompa         | FDA     | {FYCOMPA,PERAMPANEL}                                              |  25
geodon          | FDA     | {GEODON,"ZIPRASIDONE HYDROCHLORIDE."}                             |  24
geodon          | Twitter | {geodon}                                                          |   3
invokana        | Twitter | {canagliflozin}                                                   |   1
lamictal        | FDA     | {LAMICTAL}                                                        | 196
lamictal        | Twitter | {lamictal,lamotrigine}                                            |   6
lamotrigine     | FDA     | {LAMICTAL,"LAMICTAL XR"}                                          | 215
lamotrigine     | Twitter | {lamictal,lamotrigine}                                            |   6
latuda          | FDA     | {LATUDA}                                                          |  51
latuda          | Twitter | {latuda}                                                          |   2
levaquin        | FDA     | {LEVAQUIN}                                                        |  50
levaquin        | Twitter | {levaquin}                                                        |   1
linagliptin     | FDA     | {LINAGLIPTIN,TRADJENTA}                                           |  32
liraglutide     | FDA     | {LIRAGLUTIDE,VICTOZA}                                             |  53
liraglutide     | Twitter | {liraglutide,victoza}                                             |  10
livalo          | FDA     | {LIVALO,"PITAVASTATIN CALCIUM"}                                   |  18
memantine       | FDA     | {MEMANTINE,"MEMANTINE HYDROCHLORIDE"}                             |  49
metoprolol      | FDA     | {METOPROLOL}                                                      | 680
metoprolol      | Twitter | {metoprolol}                                                      |   1
namenda         | FDA     | {"MEMANTINE HYDROCHLORIDE",NAMENDA}                               |  12
nasonex         | FDA     | {NASONEX}                                                         |  64
nasonex         | Twitter | {nasonex}                                                         |   2
nesina          | FDA     | {ALOGLIPTIN,NESINA}                                               |   6
nexium          | FDA     | {"ESOMEPRAZOLE MAGNESIUM.",NEXIUM}                                | 348
nexium          | Twitter | {nexium}                                                          |   5
ofloxacin       | FDA     | {OFLOXACIN.}                                                      |   6
olanzapine      | Twitter | {olanzapine}                                                      |   6
onglyza         | FDA     | {ONGLYZA,SAXAGLIPTIN}                                             |  48
paroxetine      | FDA     | {BRISDELLE,PAROXETINE}                                            | 254
paroxetine      | Twitter | {paroxetine}                                                      |   7
pradaxa         | FDA     | {PRADAXA}                                                         | 228
pradaxa         | Twitter | {pradaxa}                                                         |   2
pregabalin      | FDA     | {LYRICA,(LYRICA),PREGABALIN.}                                     | 933
pregabalin      | Twitter | {pregabalin}                                                      |   5
quetiapine      | FDA     | {QUETIAPINE,"QUETIAPINE FUMARATE."}                               | 347
quetiapine      | Twitter | {quetiapine,seroquel}                                             |  36
rivaroxaban     | FDA     | {RIVAROXABAN,XARELTO}                                             | 788
rivaroxaban     | Twitter | {xarelto}                                                         |  16
sabril          | FDA     | {SABRIL}                                                          | 165
sabril          | Twitter | {sabril}                                                          |  12
saphris         | FDA     | {SAPHRIS}                                                         |   6
seroquel        | FDA     | {"QUETIAPINE FUMARATE.",SEROQUEL}                                 | 203
seroquel        | Twitter | {quetiapine,seroquel}                                             |  36
spiriva         | FDA     | {SPIRIVA,"TIOTROPIUM BROMIDE"}                                    | 789
synthroid       | FDA     | {"LEVOTHYROXINE SODIUM.",SYNTHROID}                               | 275
synthroid       | Twitter | {synthroid}                                                       |   5
tamiflu         | FDA     | {"OSELTAMIVIR PHOSPHATE",TAMIFLU}                                 | 116
tamiflu         | Twitter | {tamiflu}                                                         | 111
tysabri         | FDA     | {TYSABRI}                                                         | 675
tysabri         | Twitter | {tysabri}                                                         |   2
valsartan       | FDA     | {DIOVAN,VALSARTAN.}                                               | 187
valsartan       | Twitter | {valsartan}                                                       |   1
venlafaxine     | Twitter | {venlafaxine}                                                     |  12
victoza         | FDA     | {LIRAGLUTIDE,VICTOZA}                                             |  53
victoza         | Twitter | {liraglutide,victoza}                                             |  10
vimpat          | FDA     | {LACOSAMIDE,VIMPAT}                                               |  61
vyvanse         | FDA     | {VYVANSE}                                                         | 150
vyvanse         | Twitter | {vyvanse}                                                         | 106
xarelto         | FDA     | {RIVAROXABAN,XARELTO}                                             | 788
xarelto         | Twitter | {xarelto}                                                         |  16
ziprasidone     | FDA     | {ZIPRASIDONE,"ZIPRASIDONE HYDROCHLORIDE."}                        |   6
ziprasidone     | Twitter | {geodon}                                                          |   3
zoledronic acid | FDA     | {RECLAST,"ZOLEDRONIC ACID","ZOLEDRONIC ACID.",ZOMET}              | 173
zoledronic acid | Twitter | {zometa}                                                          |   1
zometa          | FDA     | {"ZOLEDRONIC ACID","ZOLEDRONIC ACID.",ZOMETA}                     | 142
zometa          | Twitter | {zometa}                                                          |   1
91 rows)
```