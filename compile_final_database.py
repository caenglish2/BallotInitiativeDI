#!/bin/python
import pandas as pd

questiondata=pd.read_csv('ballot_questions/ballot_issues.csv')
data2016=pd.read_csv('county_votes/2016_votes.dat',sep=',')
per_cap_inc=pd.read_csv('avg_income/per_capita_income.csv',sep=',')

print(questiondata.head())
print(data2016.head())
print(per_cap_inc.head())

new_df = pd.merge(questiondata, data2016,  how='left', on='STATE_COUNTY')
new_df2 = pd.merge(new_df, per_cap_inc,  how='left', on='STATE_COUNTY')
new_df2.to_csv('data_train.csv')

new_df = pd.merge(data2016, per_cap_inc,  how='left', on='STATE_COUNTY')
new_df.to_csv('data_county_lookup.csv')
