#!/bin/python
import pandas as pd

questiondata=pd.read_csv('ballot_questions/all.dat')
data2016=pd.read_csv('county_votes/2016_votes.dat',sep=',')
per_cap_inc=pd.read_csv('avg_income/per_capita_income.csv',sep=',')
uninsured_rate=pd.read_csv('avg_income/uninsured_rate3.dat',sep=',')
some_college=pd.read_csv('avg_income/some_college.dat',sep=',')
afamer_per=pd.read_csv('race/afamer_per.dat',sep=',')
white_per=pd.read_csv('race/white_per.dat',sep=',')
asian_per=pd.read_csv('race/asian_per.dat',sep=',')
hispanic_per=pd.read_csv('race/hispanic_per.dat',sep=',')

#print(questiondata.head())
#print(data2016.head())
#print(per_cap_inc.head())
#print(uninsured_rate.head())
#print(some_college.head())

new_df = pd.merge(questiondata, data2016,  how='left', on='STATE_COUNTY')
new_df2 = pd.merge(new_df, per_cap_inc,  how='left', on='STATE_COUNTY')
new_df3 = pd.merge(new_df2, uninsured_rate,  how='left', on='STATE_COUNTY')
new_df4 = pd.merge(new_df3, some_college,  how='left', on='STATE_COUNTY')
new_df5 = pd.merge(new_df4, afamer_per,  how='left', on='STATE_COUNTY')
new_df6 = pd.merge(new_df5, white_per,  how='left', on='STATE_COUNTY')
new_df7 = pd.merge(new_df6, asian_per,  how='left', on='STATE_COUNTY')
new_df8 = pd.merge(new_df7, hispanic_per,  how='left', on='STATE_COUNTY')

new_df8.drop(['Issue2','Issue3'],inplace=True,axis=1)
new_df8.dropna(inplace=True)
new_df8.to_csv('data_train.csv')

#new_df = pd.merge(data2016, per_cap_inc,  how='left', on='STATE_COUNTY')
#new_df.to_csv('data_county_lookup.csv')


new_df2 = pd.merge(data2016, per_cap_inc,  how='left', on='STATE_COUNTY')
new_df3 = pd.merge(new_df2, uninsured_rate,  how='left', on='STATE_COUNTY')
new_df4 = pd.merge(new_df3, some_college,  how='left', on='STATE_COUNTY')
new_df5 = pd.merge(new_df4, afamer_per,  how='left', on='STATE_COUNTY')
new_df6 = pd.merge(new_df5, white_per,  how='left', on='STATE_COUNTY')
new_df7 = pd.merge(new_df6, asian_per,  how='left', on='STATE_COUNTY')
new_df8 = pd.merge(new_df7, hispanic_per,  how='left', on='STATE_COUNTY')
new_df8.dropna(inplace=True)
new_df8.to_csv('data_county_lookup.csv')
